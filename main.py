from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import httpx
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Stage 0 Profile API",
    description="RESTful API endpoint that returns profile information with dynamic cat facts",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration from environment variables
USER_EMAIL = os.getenv("USER_EMAIL", "muibiyusuf@hotmail.com")
USER_NAME = os.getenv("USER_NAME", "Yusuf Muibi")
USER_STACK = os.getenv("USER_STACK", "Python/FastAPI")
CAT_FACT_API_URL = "https://catfact.ninja/fact"
CAT_FACT_TIMEOUT = float(os.getenv("CAT_FACT_TIMEOUT", "5.0"))

async def fetch_cat_fact() -> str:
    """
    Fetch a random cat fact from the Cat Facts API.
    
    Returns:
        str: A random cat fact or fallback message if API fails
    """
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Fetching cat fact from {CAT_FACT_API_URL}")
            response = await client.get(
                CAT_FACT_API_URL,
                timeout=CAT_FACT_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            fact = data.get("fact", "No cat fact available")
            logger.info("Successfully fetched cat fact")
            return fact
    except httpx.TimeoutException:
        logger.error("Cat Facts API request timed out")
        return "Cat fact unavailable: API timeout"
    except httpx.HTTPStatusError as e:
        logger.error(f"Cat Facts API returned error status: {e.response.status_code}")
        return "Cat fact unavailable: API error"
    except Exception as e:
        logger.error(f"Error fetching cat fact: {str(e)}")
        return "Cat fact unavailable: Network error"

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Stage 0 Profile API",
        "endpoints": {
            "/me": "GET - Returns profile information with cat fact",
            "/health": "GET - Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/me")
async def get_profile():
    """
    GET /me endpoint that returns profile information with a dynamic cat fact.
    
    Returns:
        JSONResponse: Profile data with status, user info, timestamp, and cat fact
    """
    try:
        # Fetch cat fact
        cat_fact = await fetch_cat_fact()
        
        # Get current UTC timestamp in ISO 8601 format
        current_timestamp = datetime.now(timezone.utc).isoformat()
        
        # Construct response
        response_data = {
            "status": "success",
            "user": {
                "email": USER_EMAIL,
                "name": USER_NAME,
                "stack": USER_STACK
            },
            "timestamp": current_timestamp,
            "fact": cat_fact
        }
        
        logger.info(f"Successfully processed /me request at {current_timestamp}")
        
        return JSONResponse(
            content=response_data,
            status_code=200,
            media_type="application/json"
        )
    
    except Exception as e:
        logger.error(f"Error processing /me request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )