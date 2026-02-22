from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ChatRequest(BaseModel):
    message: str


class Citation(BaseModel):
    source_type: str
    source_sf_id: str
    display: str
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieved: list[dict]
