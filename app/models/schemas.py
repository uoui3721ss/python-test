from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timezone


class CustomerInfo(BaseModel):
    """Customer information model."""
    customer_id: Optional[str] = None
    name: str
    email: str
    phone: str
    address: Optional[str] = None


class ServicePlan(BaseModel):
    """Telecom service plan model."""
    plan_id: str
    plan_name: str
    data_limit: str
    call_minutes: str
    sms_limit: str
    price: float
    description: str


class WelcomeKitRequest(BaseModel):
    """Welcome kit request model."""
    customer_info: CustomerInfo
    selected_plan: Optional[str] = None
    sim_type: str = Field(default="nano", description="SIM card type: nano, micro, or standard")
    delivery_address: str
    special_instructions: Optional[str] = None


class WelcomeKitResponse(BaseModel):
    """Welcome kit response model."""
    order_id: str
    status: str
    customer_name: str
    plan_details: Optional[ServicePlan] = None
    estimated_delivery: str
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatMessage(BaseModel):
    """Chat message model for AI agent interaction."""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model from AI agent."""
    response: str
    session_id: str
    suggestions: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
