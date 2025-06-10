# Pizza Order API

A simple FastAPI application for managing pizza orders.

## Features

- Create pizza orders
- User authentication
- Order management
- Multiple pizza sizes and flavors

## Tech Stack

- **FastAPI** - Web framework
- **SQLAlchemy** - Database ORM
- **Pydantic** - Data validation
- **SQLite/PostgreSQL** - Database

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pizza-order-api.git
cd pizza-order-api

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```

## API Endpoints

- `POST /orders/` - Create a new pizza order
- `GET /orders/` - Get all orders
- `GET /orders/{id}` - Get order by ID
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

## Usage

```bash
# Create an order
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 2,
    "pizza_size": "large",
    "flavour": "pepperoni"
  }'
```

## Development

```bash
# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest
```

## License

MIT
