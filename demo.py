#!/usr/bin/env python3
"""
Interactive demo script for Telecom Welcome Kit AI Agent
This script demonstrates the AI agent's capabilities through a conversation flow.
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"


def print_separator():
    print("\n" + "="*70 + "\n")


def chat(message, session_id=None):
    """Send a message to the AI agent."""
    payload = {"message": message}
    if session_id:
        payload["session_id"] = session_id
    
    response = requests.post(f"{BASE_URL}/chat/", json=payload)
    return response.json()


def get_plans():
    """Get all service plans."""
    response = requests.get(f"{BASE_URL}/welcome-kit/plans")
    return response.json()


def order_kit(customer_name, email, phone, plan_id, address):
    """Order a welcome kit."""
    payload = {
        "customer_info": {
            "name": customer_name,
            "email": email,
            "phone": phone
        },
        "selected_plan": plan_id,
        "sim_type": "nano",
        "delivery_address": address
    }
    response = requests.post(f"{BASE_URL}/welcome-kit/order", json=payload)
    return response.json()


def main():
    print("🤖 Telecom Welcome Kit AI Agent Demo")
    print_separator()
    
    # Demo 1: Initial greeting
    print("Demo 1: Customer starts a conversation")
    print("Customer: Hello!")
    result = chat("Hello!")
    print(f"Agent: {result['response']}")
    print(f"Suggestions: {result['suggestions']}")
    session_id = result['session_id']
    print_separator()
    
    sleep(1)
    
    # Demo 2: Ask about plans
    print("Demo 2: Customer asks about available plans")
    print("Customer: What plans do you have?")
    result = chat("What plans do you have?", session_id)
    print(f"Agent: {result['response']}")
    print(f"Suggestions: {result['suggestions']}")
    print_separator()
    
    sleep(1)
    
    # Demo 3: Get plans via API
    print("Demo 3: Retrieving plans through API")
    plans = get_plans()
    print("Available Plans:")
    for plan in plans:
        print(f"  - {plan['plan_name']}: ${plan['price']}/month")
        print(f"    Data: {plan['data_limit']}, Calls: {plan['call_minutes']}")
    print_separator()
    
    sleep(1)
    
    # Demo 4: Ask about SIM activation
    print("Demo 4: Customer asks about SIM activation")
    print("Customer: How do I activate my SIM?")
    result = chat("How do I activate my SIM?", session_id)
    print(f"Agent: {result['response']}")
    print_separator()
    
    sleep(1)
    
    # Demo 5: Order a welcome kit
    print("Demo 5: Placing a welcome kit order")
    print("Ordering for: Sarah Johnson")
    order = order_kit(
        customer_name="Sarah Johnson",
        email="sarah@example.com",
        phone="+1-555-0123",
        plan_id="premium-03",
        address="456 Oak Avenue, Springfield, IL 62701"
    )
    print(f"Order ID: {order['order_id']}")
    print(f"Status: {order['status']}")
    print(f"Plan: {order['plan_details']['plan_name']} - ${order['plan_details']['price']}/month")
    print(f"Estimated Delivery: {order['estimated_delivery']}")
    print(f"Message: {order['message']}")
    print_separator()
    
    sleep(1)
    
    # Demo 6: Ask about delivery
    print("Demo 6: Customer asks about delivery")
    print("Customer: When will my kit arrive?")
    result = chat("When will my kit arrive?", session_id)
    print(f"Agent: {result['response']}")
    print_separator()
    
    print("✅ Demo completed successfully!")
    print("\nThe AI agent successfully handled:")
    print("  ✓ Customer greetings and introductions")
    print("  ✓ Plan inquiries and recommendations")
    print("  ✓ SIM activation instructions")
    print("  ✓ Welcome kit ordering")
    print("  ✓ Delivery information")
    print("\nVisit http://localhost:8000/docs for interactive API documentation")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to the API server.")
        print("Make sure the server is running: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")
