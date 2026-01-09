# Bajaj Broking Trading SDK

A simplified Trading API platform built with Python FastAPI that simulates core trading workflows for online stock broking applications.

## Features

- **Instrument Management**: View available financial instruments
- **Order Management**: Place buy/sell orders with market/limit types
- **Trade Tracking**: View executed trades
- **Portfolio Management**: Check current holdings and positions
- **Real-time Simulation**: Immediate execution for market orders

## Technology Stack

- **Backend**: Python 3.8+ with FastAPI
- **Data Storage**: In-memory storage
- **API Format**: JSON REST APIs
- **Documentation**: Auto-generated Swagger/OpenAPI docs

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd bajaj_broking
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive Documentation: `http://localhost:8000/docs`
   - Alternative Docs: `http://localhost:8000/redoc`

## API Documentation

### 1. Instruments API

#### Get All Instruments
```http
GET /api/v1/instruments
```

**Response:**
```json
[
  {
    "symbol": "RELIANCE",
    "exchange": "NSE",
    "instrumentType": "EQUITY",
    "lastTradedPrice": 2450.50
  }
]
```

### 2. Order Management APIs

#### Place New Order
```http
POST /api/v1/orders
```

**Request Body:**
```json
{
  "symbol": "RELIANCE",
  "orderType": "BUY",
  "orderStyle": "MARKET",
  "quantity": 10,
  "price": null
}
```

**Response:**
```json
{
  "orderId": "uuid-string",
  "symbol": "RELIANCE",
  "orderType": "BUY",
  "orderStyle": "MARKET",
  "quantity": 10,
  "price": null,
  "status": "EXECUTED",
  "timestamp": "2024-01-01T10:00:00"
}
```

#### Get Order Status
```http
GET /api/v1/orders/{orderId}
```

### 3. Trades API

#### Get All Trades
```http
GET /api/v1/trades
```

**Response:**
```json
[
  {
    "tradeId": "uuid-string",
    "orderId": "uuid-string",
    "symbol": "RELIANCE",
    "quantity": 10,
    "price": 2450.50,
    "timestamp": "2024-01-01T10:00:00"
  }
]
```

### 4. Portfolio API

#### Get Portfolio Holdings
```http
GET /api/v1/portfolio
```

**Response:**
```json
[
  {
    "symbol": "RELIANCE",
    "quantity": 10,
    "averagePrice": 2450.50,
    "currentValue": 24505.00
  }
]
```

## Sample Usage Examples

### Using curl

1. **Get Instruments:**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/instruments"
   ```

2. **Place Market Buy Order:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/orders" \
        -H "Content-Type: application/json" \
        -d '{
          "symbol": "TCS",
          "orderType": "BUY",
          "orderStyle": "MARKET",
          "quantity": 5
        }'
   ```

3. **Place Limit Sell Order:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/orders" \
        -H "Content-Type: application/json" \
        -d '{
          "symbol": "INFY",
          "orderType": "SELL",
          "orderStyle": "LIMIT",
          "quantity": 3,
          "price": 1500.00
        }'
   ```

4. **Check Order Status:**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/orders/{order-id}"
   ```

5. **View Portfolio:**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/portfolio"
   ```

## Business Logic & Assumptions

### Order Execution
- **Market Orders**: Execute immediately at current market price
- **Limit Orders**: Placed but not automatically executed (status remains "PLACED")

### Portfolio Management
- **Buy Orders**: Add to holdings, calculate weighted average price
- **Sell Orders**: Reduce holdings, remove if quantity becomes zero
- **Current Value**: Updated in real-time based on last traded price

### Data Storage
- All data stored in-memory (resets on application restart)
- Pre-loaded with 5 sample instruments (RELIANCE, TCS, INFY, HDFC, ICICIBANK)

### Validations
- Quantity must be greater than 0
- Price mandatory for LIMIT orders
- Symbol must exist in instruments list
- Proper HTTP status codes for errors

### Order States
- **NEW**: Initial state (not used in current implementation)
- **PLACED**: Order accepted but not executed
- **EXECUTED**: Order completed successfully
- **CANCELLED**: Order cancelled (not implemented)

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `404`: Resource not found (invalid order ID or symbol)
- `422`: Validation error (invalid request data)
- `500`: Internal server error

## Testing the API

1. Start the server: `python main.py`
2. Open browser: `http://localhost:8000/docs`
3. Use the interactive Swagger UI to test all endpoints
4. Try the sample curl commands above

## Project Structure

```
bajaj_broking/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

## Future Enhancements

- Persistent database storage
- User authentication and authorization
- Real-time market data integration
- Advanced order types (stop-loss, bracket orders)
- Risk management and position limits
- Comprehensive logging and monitoring