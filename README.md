# Receipt Processor

A FastAPI-based web service for processing receipts and calculating points based on specific rules.

## Features

- Process receipts and generate unique IDs
- Calculate points based on receipt details
- Retrieve points for processed receipts
- In-memory storage (no database required)
- RESTful API endpoints
- Swagger UI documentation

## API Endpoints

### 1. Process Receipt
- **POST** `/receipts/process`
- Processes a receipt and returns an ID
- Request body: Receipt JSON
- Returns: `{ "id": "<uuid>" }`

### 2. Get Points
- **GET** `/receipts/{id}/points`
- Retrieves points for a processed receipt
- Returns: `{ "points": <points> }`

## Points Calculation Rules

1. One point for every alphanumeric character in the retailer name
2. 50 points if the total is a round dollar amount with no cents
3. 25 points if the total is a multiple of 0.25
4. 5 points for every two items on the receipt
5. If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer
6. 5 points if the total is greater than 10.00
7. 6 points if the day in the purchase date is odd
8. 10 points if the time of purchase is after 2:00pm and before 4:00pm

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sdshah09/fetch-backend.git
cd fetch-backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the server:
```bash
uvicorn app.main:app --reload
```

The server will start on http://0.0.0.0:8000

## API Documentation

Once the server is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Usage Examples

### 1. Process a Receipt

```bash
# Example 1: Simple receipt
curl -X POST "http://localhost:8000/receipts/process" \
     -H "Content-Type: application/json" \
     -d '{
           "retailer": "Target",
           "purchaseDate": "2022-01-01",
           "purchaseTime": "13:01",
           "items": [
             {
               "shortDescription": "Mountain Dew 12PK",
               "price": "6.49"
             }
           ],
           "total": "6.49"
         }'

# Example 2: Receipt with multiple items
curl -X POST "http://localhost:8000/receipts/process" \
     -H "Content-Type: application/json" \
     -d '{
           "retailer": "M&M Corner Market",
           "purchaseDate": "2022-03-20",
           "purchaseTime": "14:33",
           "items": [
             {
               "shortDescription": "Gatorade",
               "price": "2.25"
             },
             {
               "shortDescription": "Gatorade",
               "price": "2.25"
             }
           ],
           "total": "4.50"
         }'
```

### 2. Get Points for a Receipt

```bash
# Replace {id} with the actual receipt ID returned from the process endpoint
curl -X GET "http://localhost:8000/receipts/7fb1377b-b223-49d9-a31a-5a02701dd310/points"

# Example response:
# {
#   "points": 32
# }
```

### 3. Complete Workflow Example

```bash
# 1. Process a receipt
response=$(curl -X POST "http://localhost:8000/receipts/process" \
     -H "Content-Type: application/json" \
     -d '{
           "retailer": "Target",
           "purchaseDate": "2022-01-01",
           "purchaseTime": "13:01",
           "items": [
             {
               "shortDescription": "Mountain Dew 12PK",
               "price": "6.49"
             }
           ],
           "total": "6.49"
         }')

# 2. Extract the receipt ID from the response
receipt_id=$(echo $response | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

# 3. Get points for the processed receipt
curl -X GET "http://localhost:8000/receipts/$receipt_id/points"
```

## Project Structure

```
fetch-backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # Main application and API endpoints
│   ├── models.py        # Pydantic models
│   ├── calc.py          # Points calculation logic
│   └── store.py         # In-memory storage
├── utils/  
│   └── logging_module.py  # Logging logic
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Notes

- Data is stored in memory and will not persist after application restart
- The application uses FastAPI's automatic API documentation
- All endpoints are CORS-enabled
- Comprehensive logging is implemented
