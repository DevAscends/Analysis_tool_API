import os
import openai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DALL_E_API_KEY = os.getenv("DALL_E_API_KEY")

# Check if the API keys are loaded correctly
if not OPENAI_API_KEY or not DALL_E_API_KEY:
    raise ValueError("API keys are not set in the .env file.")

# Initialize FastAPI app
app = FastAPI()

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Add CORS middleware to allow requests from React frontend
origins = [
    "http://localhost:5173",  # React app's URL
    "",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from React
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Analysis Tool API"}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
