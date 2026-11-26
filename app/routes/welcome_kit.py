from fastapi import APIRouter, HTTPException
from typing import List
from app.models import WelcomeKitRequest, WelcomeKitResponse, ServicePlan
from app.services import ai_agent
from datetime import datetime

router = APIRouter(prefix="/welcome-kit", tags=["welcome-kit"])


@router.get("/plans", response_model=List[ServicePlan])
async def get_service_plans():
    """
    Get all available service plans.
    
    Returns a list of all telecom service plans with pricing and features.
    """
    try:
        plans = ai_agent.get_service_plans()
        return [ServicePlan(**plan) for plan in plans]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching plans: {str(e)}")


@router.get("/plans/{plan_id}", response_model=ServicePlan)
async def get_plan_by_id(plan_id: str):
    """
    Get details of a specific service plan by ID.
    """
    plan = ai_agent.get_plan_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail=f"Plan with ID '{plan_id}' not found")
    return ServicePlan(**plan)


@router.post("/order", response_model=WelcomeKitResponse)
async def order_welcome_kit(request: WelcomeKitRequest):
    """
    Order a welcome kit for a new customer.
    
    This endpoint creates a new welcome kit order with the selected plan,
    SIM card type, and delivery information.
    """
    try:
        # Validate plan exists if provided
        if request.selected_plan:
            plan = ai_agent.get_plan_by_id(request.selected_plan)
            if not plan:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid plan ID: {request.selected_plan}"
                )
        
        # Create the order
        order = ai_agent.create_welcome_kit_order(
            customer_name=request.customer_info.name,
            plan_id=request.selected_plan or "standard-02",  # Default to standard plan
            delivery_address=request.delivery_address
        )
        
        return WelcomeKitResponse(**order)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")


@router.get("/health")
async def welcome_kit_health():
    """Check if the welcome kit service is healthy."""
    return {"status": "healthy", "service": "welcome-kit"}
