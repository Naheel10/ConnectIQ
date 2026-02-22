from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

    @field_validator('email', 'password')
    @classmethod
    def validate_required_fields(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError('Email and password are required')
        return value.strip()


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
