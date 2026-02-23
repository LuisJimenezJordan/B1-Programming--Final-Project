from fastapi import FastAPI
from routes import analysis, users

# This 'app' variable is what uvicorn is looking for!
app = FastAPI(title="DNA Toolkit API")

# Including your routers
app.include_router(analysis.router, prefix="/analysis", tags=["DNA Tasks"])
app.include_router(users.router, prefix="/users", tags=["User Management"])

@app.get("/")
def read_root():
    return {
        "message": "System Online",
        "status": "Ready for DNA Analysis"
    }