from pydantic import BaseModel, Field

class TaskSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=25)
    description: str = Field(..., min_length=5, max_length=100)
    is_completed: bool = False


class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str 
    is_completed: bool
    user_id: int | None = 0

    