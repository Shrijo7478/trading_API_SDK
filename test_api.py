#!/usr/bin/env python3
"""
Simple test script to demonstrate Bajaj Broking Trading SDK functionality
Run this after starting the main server (python main.py)
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("🚀 Testing Bajaj Broking Trading SDK")
    print("=" * 50)
    
    # Test 1: Get Instruments
    print("\n1. Fetching available instruments...")
    response = requests.get(f"{BASE_URL}/api/v1/instruments")
    if response.status_code == 200:
        instruments = response.json()
        print(f"✅ Found {len(instruments)} instruments")
        for inst in instruments[:3]:
            print(f"   {inst['symbol']}: ₹{inst['lastTradedPrice']}")
    else:
        print("❌ Failed to fetch instruments")
        return
    
    # Test 2: Place Market Buy Order
    print("\n2. Placing market buy order for RELIANCE...")
    order_data = {
        "symbol": "RELIANCE",
        "orderType": "BUY",
        "orderStyle": "MARKET",
        "quantity": 10
    }
    response = requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)
    if response.status_code == 200:
        order = response.json()
        print(f"✅ Order placed: {order['orderId']}")
        print(f"   Status: {order['status']}")
        order_id = order['orderId']
    else:
        print("❌ Failed to place order")
        return
    
    # Test 3: Check Order Status
    print("\n3. Checking order status...")
    response = requests.get(f"{BASE_URL}/api/v1/orders/{order_id}")
    if response.status_code == 200:
        order = response.json()
        print(f"✅ Order {order_id[:8]}... is {order['status']}")
    else:
        print("❌ Failed to get order status")
    
    # Test 4: Place Limit Sell Order
    print("\n4. Placing limit sell order for TCS...")
    order_data = {
        "symbol": "TCS",
        "orderType": "BUY",
        "orderStyle": "LIMIT",
        "quantity": 5,
        "price": 3900.00
    }
    response = requests.post(f"{BASE_URL}/api/v1/orders", json=order_data)
    if response.status_code == 200:
        order = response.json()
        print(f"✅ Limit order placed: {order['orderId']}")
        print(f"   Status: {order['status']} at ₹{order['price']}")
    else:
        print("❌ Failed to place limit order")
    
    # Test 5: View Trades
    print("\n5. Fetching executed trades...")
    response = requests.get(f"{BASE_URL}/api/v1/trades")
    if response.status_code == 200:
        trades = response.json()
        print(f"✅ Found {len(trades)} executed trades")
        for trade in trades:
            print(f"   {trade['symbol']}: {trade['quantity']} @ ₹{trade['price']}")
    else:
        print("❌ Failed to fetch trades")
    
    # Test 6: View Portfolio
    print("\n6. Checking portfolio holdings...")
    response = requests.get(f"{BASE_URL}/api/v1/portfolio")
    if response.status_code == 200:
        portfolio = response.json()
        print(f"✅ Portfolio has {len(portfolio)} holdings")
        total_value = 0
        for holding in portfolio:
            print(f"   {holding['symbol']}: {holding['quantity']} shares @ ₹{holding['averagePrice']:.2f}")
            print(f"      Current Value: ₹{holding['currentValue']:.2f}")
            total_value += holding['currentValue']
        print(f"\n💰 Total Portfolio Value: ₹{total_value:.2f}")
    else:
        print("❌ Failed to fetch portfolio")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("Visit http://localhost:8000/docs for interactive API documentation")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure to run 'python main.py' first!")
    except Exception as e:
        print(f"❌ Error: {e}")