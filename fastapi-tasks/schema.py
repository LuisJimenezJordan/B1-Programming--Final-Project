#PYDANTIC MODELS
from pydantic import BaseModel, Field

# 1. This is what the user sends in the request body
class DNATaskCreate(BaseModel):
    label: str = Field(..., description="A label for the DNA sequence")
    sequence: str = Field(..., description="The actual DNA sequence (A, T, C, G)")

# 2. This is what you save to tasks.txt and return to the user
class DNATask(BaseModel):
    id: int
    label: str
    sequence: str
    gc_content: float
    status: str = "completed"
