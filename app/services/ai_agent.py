import uuid
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.config import settings


class AIAgent:
    """AI Agent for handling telecom welcome kit customer interactions."""
    
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}
        self.service_plans = self._initialize_plans()
    
    def _initialize_plans(self) -> List[Dict]:
        """Initialize available service plans."""
        return [
            {
                "plan_id": "basic-01",
                "plan_name": "Basic Plan",
                "data_limit": "5GB",
                "call_minutes": "100 minutes",
                "sms_limit": "Unlimited",
                "price": 19.99,
                "description": "Perfect for light users who mainly use messaging"
            },
            {
                "plan_id": "standard-02",
                "plan_name": "Standard Plan",
                "data_limit": "20GB",
                "call_minutes": "500 minutes",
                "sms_limit": "Unlimited",
                "price": 39.99,
                "description": "Great for everyday use with social media and streaming"
            },
            {
                "plan_id": "premium-03",
                "plan_name": "Premium Plan",
                "data_limit": "Unlimited",
                "call_minutes": "Unlimited",
                "sms_limit": "Unlimited",
                "price": 59.99,
                "description": "Ultimate freedom with unlimited everything"
            }
        ]
    
    def get_service_plans(self) -> List[Dict]:
        """Get all available service plans."""
        return self.service_plans
    
    def get_plan_by_id(self, plan_id: str) -> Optional[Dict]:
        """Get a specific plan by ID."""
        for plan in self.service_plans:
            if plan["plan_id"] == plan_id:
                return plan
        return None
    
    def process_chat_message(self, message: str, session_id: Optional[str] = None) -> tuple[str, str, List[str]]:
        """
        Process a chat message and generate a response.
        
        Args:
            message: User's message
            session_id: Optional session ID for conversation continuity
            
        Returns:
            Tuple of (response, session_id, suggestions)
        """
        # Create or retrieve session
        if not session_id:
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = []
        
        # Store user message in session
        self.sessions[session_id].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate response based on message content
        response, suggestions = self._generate_response(message.lower(), session_id)
        
        # Store assistant response in session
        self.sessions[session_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response, session_id, suggestions
    
    def _generate_response(self, message: str, session_id: str) -> tuple[str, List[str]]:
        """Generate contextual response based on user message."""
        suggestions = []
        
        # Welcome and general greetings
        if any(word in message for word in ["hello", "hi", "hey", "greetings"]):
            response = ("Hello! Welcome to our Telecom Welcome Kit Service. I'm here to help you get started with your new service. "
                       "I can assist you with:\n"
                       "• Choosing the right service plan\n"
                       "• Ordering your welcome kit\n"
                       "• SIM card activation\n"
                       "• Answering questions about our services\n\n"
                       "What would you like to know?")
            suggestions = ["Show me available plans", "How do I activate my SIM?", "Order a welcome kit"]
        
        # Plan inquiries
        elif any(word in message for word in ["plan", "plans", "price", "pricing", "packages"]):
            plans_info = "\n\n".join([
                f"**{plan['plan_name']}** (${plan['price']}/month)\n"
                f"  • Data: {plan['data_limit']}\n"
                f"  • Calls: {plan['call_minutes']}\n"
                f"  • SMS: {plan['sms_limit']}\n"
                f"  • {plan['description']}"
                for plan in self.service_plans
            ])
            response = f"Here are our available plans:\n\n{plans_info}\n\nWhich plan interests you?"
            suggestions = ["I want the Basic Plan", "Tell me more about Premium", "Order Standard Plan"]
        
        # Welcome kit ordering
        elif any(word in message for word in ["order", "kit", "welcome kit", "get started"]):
            response = ("Great! To order your welcome kit, I'll need some information:\n"
                       "1. Your preferred service plan\n"
                       "2. SIM card type (nano, micro, or standard)\n"
                       "3. Delivery address\n\n"
                       "Would you like to choose a plan first?")
            suggestions = ["Show me the plans", "I already know which plan I want"]
        
        # SIM activation
        elif any(word in message for word in ["activate", "activation", "sim"]):
            response = ("To activate your SIM card:\n\n"
                       "1. Insert the SIM card into your device\n"
                       "2. Power on your device\n"
                       "3. You'll receive a confirmation SMS within 5-10 minutes\n"
                       "4. Restart your device if needed\n\n"
                       "If you have any issues, our support team is here to help 24/7!")
            suggestions = ["I'm having activation issues", "What if I don't receive the SMS?"]
        
        # Support and help
        elif any(word in message for word in ["help", "support", "problem", "issue"]):
            response = ("I'm here to help! You can reach our support team:\n\n"
                       "📞 Phone: 1-800-TELECOM (24/7)\n"
                       "📧 Email: support@telecom.com\n"
                       "💬 Live Chat: Available on our website\n\n"
                       "You can also ask me about:\n"
                       "• Service plans and pricing\n"
                       "• Welcome kit ordering\n"
                       "• SIM activation\n"
                       "• General account questions")
            suggestions = ["Show me the plans", "How do I order?"]
        
        # Delivery and shipping
        elif any(word in message for word in ["delivery", "shipping", "ship", "when will"]):
            response = ("Our welcome kits are shipped via express delivery:\n\n"
                       "• Standard delivery: 3-5 business days\n"
                       "• Express delivery: 1-2 business days (additional fee)\n"
                       "• Free shipping on all orders!\n\n"
                       "You'll receive a tracking number once your kit is shipped.")
            suggestions = ["Order a welcome kit", "What's included in the kit?"]
        
        # Default response
        else:
            response = ("I'm not sure I understood that correctly. I can help you with:\n\n"
                       "• Viewing and selecting service plans\n"
                       "• Ordering your welcome kit\n"
                       "• SIM card activation instructions\n"
                       "• General support questions\n\n"
                       "What would you like to know more about?")
            suggestions = ["Show me plans", "Order a welcome kit", "Help with activation"]
        
        return response, suggestions
    
    def create_welcome_kit_order(self, customer_name: str, plan_id: str, delivery_address: str) -> Dict:
        """Create a welcome kit order."""
        order_id = f"WK-{uuid.uuid4().hex[:8].upper()}"
        estimated_delivery = (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d")
        
        plan = self.get_plan_by_id(plan_id)
        
        return {
            "order_id": order_id,
            "status": "Processing",
            "customer_name": customer_name,
            "plan_details": plan,
            "estimated_delivery": estimated_delivery,
            "message": f"Your welcome kit order has been confirmed! Order ID: {order_id}. "
                      f"Estimated delivery: {estimated_delivery}"
        }


# Singleton instance
ai_agent = AIAgent()
