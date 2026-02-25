from fastapi import FastAPI
from routes import analysis, sequences

# This 'app' variable is what uvicorn is looking for!
app = FastAPI(title="DNA Sequence Toolkit API")

# Including your routers
app.include_router(analysis.router, prefix="/analysis", tags=["DNA Tasks"])
app.include_router(sequences.router, prefix="/sequences", tags=["Sequence Management"])

@app.get("/")
def read_root():
    return {
        "message": "System Online",
        "status": "Ready for DNA Analysis"
    }