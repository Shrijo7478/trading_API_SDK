from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, validator
from typing import List, Optional, Dict
from enum import Enum
import uuid
from datetime import datetime

app = FastAPI(title="Bajaj Broking Trading SDK", version="1.0.0")

# Enums
class OrderType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStyle(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class OrderStatus(str, Enum):
    NEW = "NEW"
    PLACED = "PLACED"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"

class InstrumentType(str, Enum):
    EQUITY = "EQUITY"
    FUTURES = "FUTURES"
    OPTIONS = "OPTIONS"

# Models
class Instrument(BaseModel):
    symbol: str
    exchange: str
    instrumentType: InstrumentType
    lastTradedPrice: float

class OrderRequest(BaseModel):
    symbol: str
    orderType: OrderType
    orderStyle: OrderStyle
    quantity: int
    price: Optional[float] = None

    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than 0')
        return v

    @validator('price')
    def price_required_for_limit_orders(cls, v, values):
        if values.get('orderStyle') == OrderStyle.LIMIT and v is None:
            raise ValueError('Price is mandatory for LIMIT orders')
        return v

class Order(BaseModel):
    orderId: str
    symbol: str
    orderType: OrderType
    orderStyle: OrderStyle
    quantity: int
    price: Optional[float]
    status: OrderStatus
    timestamp: datetime

class Trade(BaseModel):
    tradeId: str
    orderId: str
    symbol: str
    quantity: int
    price: float
    timestamp: datetime

class Portfolio(BaseModel):
    symbol: str
    quantity: int
    averagePrice: float
    currentValue: float

# In-memory storage
instruments_db: List[Instrument] = [
    Instrument(symbol="RELIANCE", exchange="NSE", instrumentType=InstrumentType.EQUITY, lastTradedPrice=2450.50),
    Instrument(symbol="TCS", exchange="NSE", instrumentType=InstrumentType.EQUITY, lastTradedPrice=3890.75),
    Instrument(symbol="INFY", exchange="NSE", instrumentType=InstrumentType.EQUITY, lastTradedPrice=1456.20),
    Instrument(symbol="HDFC", exchange="NSE", instrumentType=InstrumentType.EQUITY, lastTradedPrice=1678.90),
    Instrument(symbol="ICICIBANK", exchange="NSE", instrumentType=InstrumentType.EQUITY, lastTradedPrice=945.30)
]

orders_db: Dict[str, Order] = {}
trades_db: List[Trade] = []
portfolio_db: Dict[str, Portfolio] = {}

# Helper functions
def get_instrument_price(symbol: str) -> float:
    for instrument in instruments_db:
        if instrument.symbol == symbol:
            return instrument.lastTradedPrice
    raise HTTPException(status_code=404, detail="Instrument not found")

def execute_order(order: Order):
    """Simulate order execution for market orders"""
    if order.orderStyle == OrderStyle.MARKET:
        execution_price = get_instrument_price(order.symbol)
        
        # Create trade
        trade = Trade(
            tradeId=str(uuid.uuid4()),
            orderId=order.orderId,
            symbol=order.symbol,
            quantity=order.quantity,
            price=execution_price,
            timestamp=datetime.now()
        )
        trades_db.append(trade)
        
        # Update portfolio
        if order.symbol in portfolio_db:
            portfolio = portfolio_db[order.symbol]
            if order.orderType == OrderType.BUY:
                total_value = (portfolio.quantity * portfolio.averagePrice) + (order.quantity * execution_price)
                portfolio.quantity += order.quantity
                portfolio.averagePrice = total_value / portfolio.quantity
            else:  # SELL
                portfolio.quantity -= order.quantity
                if portfolio.quantity <= 0:
                    del portfolio_db[order.symbol]
                    return
        else:
            if order.orderType == OrderType.BUY:
                portfolio_db[order.symbol] = Portfolio(
                    symbol=order.symbol,
                    quantity=order.quantity,
                    averagePrice=execution_price,
                    currentValue=0
                )
        
        # Update current value
        if order.symbol in portfolio_db:
            current_price = get_instrument_price(order.symbol)
            portfolio_db[order.symbol].currentValue = portfolio_db[order.symbol].quantity * current_price
        
        # Update order status
        order.status = OrderStatus.EXECUTED

# API Endpoints
@app.get("/api/v1/instruments", response_model=List[Instrument])
async def get_instruments():
    """Fetch list of tradable instruments"""
    return instruments_db

@app.post("/api/v1/orders", response_model=Order)
async def place_order(order_request: OrderRequest):
    """Place a new order"""
    # Validate instrument exists
    get_instrument_price(order_request.symbol)
    
    order = Order(
        orderId=str(uuid.uuid4()),
        symbol=order_request.symbol,
        orderType=order_request.orderType,
        orderStyle=order_request.orderStyle,
        quantity=order_request.quantity,
        price=order_request.price,
        status=OrderStatus.PLACED,
        timestamp=datetime.now()
    )
    
    orders_db[order.orderId] = order
    
    # Execute market orders immediately
    if order.orderStyle == OrderStyle.MARKET:
        execute_order(order)
    
    return order

@app.get("/api/v1/orders/{order_id}", response_model=Order)
async def get_order_status(order_id: str):
    """Fetch order status"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]

@app.get("/api/v1/trades", response_model=List[Trade])
async def get_trades():
    """Fetch list of executed trades"""
    return trades_db

@app.get("/api/v1/portfolio", response_model=List[Portfolio])
async def get_portfolio():
    """Fetch current portfolio holdings"""
    # Update current values before returning
    for portfolio in portfolio_db.values():
        current_price = get_instrument_price(portfolio.symbol)
        portfolio.currentValue = portfolio.quantity * current_price
    
    return list(portfolio_db.values())

@app.get("/")
async def root():
    return {"message": "Bajaj Broking Trading SDK", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)