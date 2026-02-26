# main.py
# Entry point for the DNA Sequence Toolkit API.
# Creates the FastAPI application instance and registers the two routers:
#   - sequences router: handles all sequence management (create, list, fetch, update, delete)
#   - analysis router: handles all biological analysis (nucleotide, amino acid, summary stats)

from fastapi import FastAPI
from routes import analysis, sequences

# The 'app' variable is what uvicorn looks for when starting the server
app = FastAPI(title="DNA Sequence Toolkit API")

# Register the sequences router under the /sequences prefix
app.include_router(sequences.router, prefix="/sequences", tags=["Sequence Management"])

# Register the analysis router under the /analysis prefix
app.include_router(analysis.router, prefix="/analysis", tags=["DNA Analysis"])


# --- Root Endpoint ---
# A simple health check endpoint to confirm the API is running.
# Also provides a brief description of what the toolkit does.
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the DNA Sequence Toolkit API 🧬",
        "status": "System Online — Ready for DNA Analysis",
        "description": "Submit DNA nucleotide sequences for storage, perform GC content and amino acid analyses, and retrieve summary statistics across your sequence library.",
        "docs": "Visit /docs for the full interactive API documentation."
    }