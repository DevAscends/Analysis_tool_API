import os
import openai
from fastapi import FastAPI, File, UploadFile
import pandas as pd
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
    allow_origins=origins,  # Allow your React frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow only POST requests
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
async def read_root():
    return {"message": "Welcome to Analysis Tool API"}

@app.post("/analyze-csv")  # Ensure this is a POST route
async def analyze_csv(file: UploadFile = File(...)):
    # Validate file type
    if file.content_type != "text/csv":
        return {"error": "File must be a CSV"}

    try:
        # Read the uploaded CSV file
        df = pd.read_csv(file.file)

        # Calculate total rows
        total_rows = len(df)

        # Calculate summary statistics for numeric columns
        summary = df.describe().to_dict()

        # Get the top 5 rows
        top_5_rows = df.head().to_dict(orient="records")

        return {
            "total_rows": total_rows,
            #"summary": summary,
            "top_5_rows": top_5_rows,
        }
    except pd.errors.EmptyDataError:
        return {"error": "The file is empty"}
    except pd.errors.ParserError:
        return {"error": "The file is not a valid CSV"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}
    
# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)