# import os
# import openai
# from fastapi import FastAPI, File, UploadFile
# import pandas as pd
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Read API keys from environment variables
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# DALL_E_API_KEY = os.getenv("DALL_E_API_KEY")

# # Check if the API keys are loaded correctly
# if not OPENAI_API_KEY or not DALL_E_API_KEY:
#     raise ValueError("API keys are not set in the .env file.")

# # Initialize FastAPI app
# app = FastAPI()

# # Set OpenAI API key
# openai.api_key = OPENAI_API_KEY

# # Add CORS middleware to allow requests from React frontend
# origins = [
#     "http://localhost:5173",  # React app's URL
#     "",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,  # Allow your React frontend's origin
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow only POST requests
#     allow_headers=["*"],  # Allow all headers
# )


# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to Analysis Tool API"}

# @app.post("/analyze-csv")  # Ensure this is a POST route
# async def analyze_csv(file: UploadFile = File(...)):
#     # Validate file type
#     if file.content_type != "text/csv":
#         return {"error": "File must be a CSV"}

#     try:
#         # Read the uploaded CSV file
#         df = pd.read_csv(file.file)

#         # Calculate total rows
#         total_rows = len(df)

#         # Calculate summary statistics for numeric columns
#         summary = df.describe().to_dict()

#         # Get the top 5 rows
#         top_5_rows = df.head().to_dict(orient="records")

#         return {
#             "total_rows": total_rows,
#             #"summary": summary,
#             "top_5_rows": top_5_rows,
#         }
#     except pd.errors.EmptyDataError:
#         return {"error": "The file is empty"}
#     except pd.errors.ParserError:
#         return {"error": "The file is not a valid CSV"}
#     except Exception as e:
#         return {"error": f"An error occurred: {str(e)}"}
    
# # Run the app
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=8000)

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import io
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Initialize FastAPI app
app = FastAPI()

# # Add CORS middleware to allow requests from React frontend
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

# In-memory storage for uploaded files
uploaded_files = {}

class ChatRequest(BaseModel):
    prompt: str
    file_id: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to Analysis Tool API"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    df = None
    
    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(contents))
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(contents))
    elif file.filename.endswith(".json"):
        df = pd.read_json(io.BytesIO(contents))
    else:
        return JSONResponse(content={"error": "Unsupported file format"}, status_code=400)
    
    file_id = file.filename  # Using filename as ID for now (can be improved)
    uploaded_files[file_id] = df
    
    return {"message": "File uploaded successfully", "file_id": file_id}

@app.post("/process/")
async def process_chat(request: ChatRequest):
    file_id = request.file_id
    prompt = request.prompt
    
    if file_id not in uploaded_files:
        return JSONResponse(content={"error": "File not found"}, status_code=404)
    
    df = uploaded_files[file_id]
    data_summary = df.head().to_json()
    
    # Generate AI response using Gemini
    response = model.generate_content(f"User prompt: {prompt}\nData: {data_summary}")
    
    #return {"response": response.text, "data_preview": df.head().to_dict()}
    return {"response": response.text}

@app.get("/files/")
async def list_files():
    return {"uploaded_files": list(uploaded_files.keys())}


# # Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)