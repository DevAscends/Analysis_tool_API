# FastAPI Project: Analysis Tool

## Setup Instructions

### 1. Install Requirements

First, ensure you have Python 3.8+ installed. Then, install the required dependencies:

### Clone the Repository:

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/Analysis_tool_API.git
```

Next 
```bash
cd Analysis_tool_API
```

Then
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables and install **python-dotenv**

```
pip install python-dotenv
```

Create a `.env` file in the root directory of the project with the necessary environment variables. Example:

```env
BASE_URL=http://localhost:8000
API_KEY=your_api_key
```

### 3. Run the Application

To start the FastAPI server, use the following command:

```bash
uvicorn main:app --reload
```

This will run the application locally and make it accessible at `http://127.0.0.1:8000`.

---

This simplified README covers the basic setup your team needs to get started quickly.
