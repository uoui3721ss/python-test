# Telecom Welcome Kit AI Agent Service

An AI-powered FastAPI application for managing telecom company's welcome kit service. This service provides an intelligent agent that helps customers choose service plans, order welcome kits, and get assistance with SIM card activation.

## Features

- 🤖 **AI-Powered Chat Agent**: Interactive chat interface for customer support
- 📦 **Welcome Kit Ordering**: Streamlined process for ordering welcome kits
- 📱 **Service Plans**: Multiple telecom plans with different pricing tiers
- 💳 **Plan Management**: Browse and select from Basic, Standard, and Premium plans
- 📍 **Order Tracking**: Track welcome kit orders with estimated delivery dates
- 🔌 **SIM Activation**: Step-by-step guidance for SIM card activation
- 📚 **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## Project Structure

```
python-test/
├── app/
│   ├── __init__.py
│   ├── config.py              # Application configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── chat.py            # Chat endpoints
│   │   └── welcome_kit.py     # Welcome kit endpoints
│   └── services/
│       ├── __init__.py
│       └── ai_agent.py        # AI agent logic
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/uoui3721ss/python-test.git
cd python-test
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create environment file:
```bash
cp .env.example .env
```

5. (Optional) Configure your OpenAI API key in `.env` if you want to integrate with OpenAI:
```
OPENAI_API_KEY=your_actual_api_key_here
```

## Running the Application

### Development Mode

Start the server with auto-reload:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## API Endpoints

### General

- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

### Chat Agent

- `POST /chat/` - Chat with the AI agent
  - Request body: `{"message": "Hello", "session_id": "optional"}`
  - Returns: AI response with suggestions and session ID

### Welcome Kit Service

- `GET /welcome-kit/plans` - Get all available service plans
- `GET /welcome-kit/plans/{plan_id}` - Get specific plan details
- `POST /welcome-kit/order` - Order a welcome kit
  - Request body includes customer info, selected plan, and delivery details

## Usage Examples

### 1. Chat with AI Agent

```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, I need help choosing a plan"}'
```

### 2. Get Service Plans

```bash
curl -X GET "http://localhost:8000/welcome-kit/plans"
```

### 3. Order a Welcome Kit

```bash
curl -X POST "http://localhost:8000/welcome-kit/order" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_info": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890"
    },
    "selected_plan": "standard-02",
    "sim_type": "nano",
    "delivery_address": "123 Main St, City, State 12345"
  }'
```

## Service Plans

### Basic Plan - $19.99/month
- 5GB Data
- 100 minutes calls
- Unlimited SMS
- Perfect for light users

### Standard Plan - $39.99/month
- 20GB Data
- 500 minutes calls
- Unlimited SMS
- Great for everyday use

### Premium Plan - $59.99/month
- Unlimited Data
- Unlimited calls
- Unlimited SMS
- Ultimate freedom

## AI Agent Capabilities

The AI agent can assist with:

1. **Plan Selection**: Helps customers choose the right service plan
2. **Welcome Kit Ordering**: Guides through the ordering process
3. **SIM Activation**: Provides step-by-step activation instructions
4. **General Support**: Answers questions about services and features
5. **Session Management**: Maintains conversation context across messages

## Development

### Adding New Features

1. **New Models**: Add Pydantic models in `app/models/schemas.py`
2. **New Services**: Add business logic in `app/services/`
3. **New Routes**: Add API endpoints in `app/routes/`
4. **Configuration**: Update `app/config.py` for new settings

### Testing

You can test the API using:
- Swagger UI at http://localhost:8000/docs
- ReDoc at http://localhost:8000/redoc
- curl commands
- Postman or similar API testing tools

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (optional) | "" |
| `APP_NAME` | Application name | "Telecom Welcome Kit AI Agent" |
| `APP_VERSION` | Application version | "1.0.0" |
| `DEBUG` | Debug mode | True |
| `HOST` | Server host | "0.0.0.0" |
| `PORT` | Server port | 8000 |

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support and questions, please open an issue in the GitHub repository.
