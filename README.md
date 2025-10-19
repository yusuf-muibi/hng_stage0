# Stage 0 - Profile API with Cat Facts ���

A simple RESTful API built with FastAPI that returns profile information along with dynamic cat facts fetched from an external API.

## ��� Features

- **GET /me** - Returns profile information with a random cat fact
- **GET /health** - Health check endpoint
- **GET /** - API documentation and available endpoints
- Dynamic timestamp generation (UTC, ISO 8601 format)
- Graceful error handling for external API failures
- CORS enabled for cross-origin requests
- Comprehensive logging for debugging

## ��� Requirements

- Python 3.8+
- pip (Python package manager)

## ���️ Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - Lightning-fast ASGI server
- **httpx** - Async HTTP client for making external API calls
- **python-dotenv** - Environment variable management

## ��� Installation

### 1. Clone the repository
```bash
git clone https://github.com/yusuf-muibi/hng_stage0.git
cd hng_stage0
```

### 2. Create a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit the `.env` file with your information:
```env
USER_EMAIL=muibiyusuf@hotmail.com
USER_NAME=Yusuf Muibi
USER_STACK=Python/FastAPI
CAT_FACT_TIMEOUT=5.0
PORT=8000
```

## ��� Running Locally

### Development mode (with auto-reload)
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Local**: http://localhost:8000
- **Network**: http://0.0.0.0:8000

### Interactive API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## ��� API Endpoints

### GET /me

Returns profile information with a random cat fact.

**Response (200 OK):**
```json
{
  "status": "success",
  "user": {
    "email": "muibiyusuf@hotmail.com",
    "name": "Yusuf Muibi",
    "stack": "Python/FastAPI"
  },
  "timestamp": "2025-10-19T14:17:12.880779+00:00",
  "fact": "Cats spend 70% of their lives sleeping."
}
```

**Example Request:**
```bash
curl http://localhost:8000/me
```

### GET /health

Health check endpoint to verify the API is running.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-19T14:17:12.880779+00:00"
}
```

### GET /

Root endpoint with API information.

**Response (200 OK):**
```json
{
  "message": "Welcome to Stage 0 Profile API",
  "endpoints": {
    "/me": "GET - Returns profile information with cat fact",
    "/health": "GET - Health check endpoint"
  }
}
```

## ��� Testing

### Manual Testing
```bash
# Test the /me endpoint
curl http://localhost:8000/me

# Test with formatted output (requires jq)
curl http://localhost:8000/me | jq

# Test the health endpoint
curl http://localhost:8000/health
```

### Automated Testing

Run the test script:
```bash
python test_api.py
```

### Expected Behavior

- ✅ Each request to `/me` returns a new timestamp
- ✅ Each request fetches a new cat fact (not cached)
- ✅ If Cat Facts API is down, a fallback message is returned
- ✅ Response always includes all required fields
- ✅ Content-Type header is `application/json`

## ��� Deployment

This API is deployed on Railway at: [Your deployment URL]

### Deploy to Railway

1. **Login to Railway**
   - Go to [railway.app](https://railway.app)
   - Click "Login with GitHub"

2. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `yusuf-muibi/hng_stage0`

3. **Set Environment Variables**
   - Go to "Variables" tab and add:
     - `USER_EMAIL=muibiyusuf@hotmail.com`
     - `USER_NAME=Yusuf Muibi`
     - `USER_STACK=Python/FastAPI`

4. **Generate Domain**
   - Go to "Settings" → "Generate Domain"
   - Your API will be live!

## ��� Project Structure
```
hng_stage0/
│
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── test_api.py         # Automated test script
├── .env                 # Environment variables (not in git)
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
├── Procfile            # Deployment configuration
├── railway.json        # Railway configuration
└── README.md           # This file
```

## ��� Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `USER_EMAIL` | Your email address | muibiyusuf@hotmail.com | Yes |
| `USER_NAME` | Your full name | Yusuf Muibi | Yes |
| `USER_STACK` | Your backend stack | Python/FastAPI | Yes |
| `CAT_FACT_TIMEOUT` | Timeout for Cat Facts API (seconds) | 5.0 | No |
| `PORT` | Server port | 8000 | No |

## ��� Acceptance Criteria Checklist

- ✅ Working GET /me endpoint accessible and returns 200 OK
- ✅ Response structure strictly follows defined JSON schema
- ✅ All required fields present (status, user, timestamp, fact)
- ✅ User object contains email, name, and stack fields with valid strings
- ✅ Timestamp returns current UTC time in ISO 8601 format
- ✅ Timestamp updates dynamically with every request
- ✅ Fact field contains cat fact from Cat Facts API
- ✅ New cat fact fetched on every request (not cached)
- ✅ Response Content-Type header is application/json
- ✅ Code is well-structured and follows FastAPI best practices

## ��� Key Implementation Details

1. **Dynamic Timestamps**: Uses `datetime.now(timezone.utc).isoformat()` to generate ISO 8601 formatted timestamps
2. **Async HTTP Calls**: Uses `httpx.AsyncClient` for non-blocking external API calls
3. **Error Handling**: Gracefully handles timeouts, HTTP errors, and network failures
4. **CORS Enabled**: Allows cross-origin requests for frontend integration
5. **Logging**: Comprehensive logging for debugging and monitoring

## ��� Contact

- **Name**: Yusuf Muibi
- **Email**: muibiyusuf@hotmail.com
- **Stack**: Python/FastAPI
- **GitHub**: [@yusuf-muibi](https://github.com/yusuf-muibi)

## ��� License

This project is created for the HNG Stage 0 Backend Task.

---
