
# Fitness Appointment System - Backend

A RESTful API backend for managing fitness appointments, built with FastAPI and MongoDB. Provides CRUD operations for appointments with separate employee and trainer functionalities.

## Deployment Link
**Backend API**: [https://vibecopilot-fitness-backend.onrender.com/docs](https://vibecopilot-fitness-backend.onrender.com/docs)  


## Features

- **Appointment Management**: Create, read, update, and delete appointments
- **Role-based Access**:
  - Employees can book/manage appointments
  - Trainers can approve/update appointment statuses
- **Status Tracking**: Pending → Approved → Completed/Cancelled
- **MongoDB Integration**: Flexible NoSQL database storage
- **Validation**: Strong data validation using Pydantic models
- **Security**: CORS configured for frontend integration

## Technology Stack

- **Framework**: FastAPI
- **Database**: MongoDB
- **Python Libraries**:
  - Motor (Async MongoDB driver)
  - Pydantic (Data validation)
  - Uvicorn (ASGI server)
- **Tools**: MongoDB Atlas

## Prerequisites

- Python 3.10+
- MongoDB (Local or Atlas)
- pip package manager
- Basic understanding of REST APIs

## Installation

1. **Clone Repository**
```bash
git clone https://github.com/yourusername/fitness-appointment-backend.git
cd fitness-appointment-backend
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Setup**
Create `.env` file:
```bash
MONGODB_URL=mongodb://localhost:27017  # For local MongoDB
DB_NAME=fitness_db
```

## Configuration

1. **Database Setup**
- Local MongoDB: Ensure service is running
- MongoDB Atlas: Use connection string:
  ```bash
  MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/db_name
  ```

2. **Run Application**
```bash
uvicorn app.main:app --reload
```

3. **Access API Docs**
- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## API Endpoints

### Employee Routes (`/api/employees`)
| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| POST   | /appointments         | Create new appointment     |
| GET    | /appointments         | Get all appointments       |
| GET    | /appointments/{id}    | Get single appointment     |
| PUT    | /appointments/{id}    | Update appointment         |
| DELETE | /appointments/{id}    | Delete appointment         |

### Trainer Routes (`/api/trainers`)
| Method | Endpoint              | Description                |
|--------|-----------------------|----------------------------|
| GET    | /appointments         | View all appointments      |
| PATCH  | /appointments/{id}/status | Update appointment status |

## Deployment

1. **Services**
   - Vercel.com

2. **Environment Variables**  
   Set in hosting platform:
   - `MONGODB_URI`

3. **Build Command**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Frontend Integration

Sample React API call:
```javascript
// Create appointment
const createAppointment = async (data) => {
  const response = await fetch('http://your-api-url/api/employees/appointments', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  return await response.json();
};
```
