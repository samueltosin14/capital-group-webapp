from pydantic import BaseModel, EmailStr, Field


class CustomerIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=40)
    company_name: str | None = Field(default=None, max_length=150)
    city: str | None = Field(default=None, max_length=120)


class EnquiryCreate(CustomerIn):
    subject: str = Field(min_length=3, max_length=200)
    message: str = Field(min_length=10, max_length=5000)


class QuoteRequestCreate(CustomerIn):
    service_id: str | None = None
    project_location: str = Field(min_length=2, max_length=150)
    budget_range: str | None = Field(default=None, max_length=80)
    desired_start_date: str | None = Field(default=None, max_length=40)
    details: str = Field(min_length=20, max_length=8000)


class ProjectCreate(BaseModel):
    service_id: str | None = None
    title: str = Field(min_length=3, max_length=180)
    slug: str = Field(min_length=3, max_length=200)
    location: str = Field(min_length=2, max_length=150)
    description: str = Field(min_length=10)
    client_name: str | None = Field(default=None, max_length=150)
    year_completed: int | None = None
    is_featured: bool = False
    is_published: bool = True


class TestimonialCreate(BaseModel):
    client_name: str = Field(min_length=2, max_length=150)
    client_title: str | None = Field(default=None, max_length=150)
    content: str = Field(min_length=10, max_length=2000)
    rating: int = Field(default=5, ge=1, le=5)
    is_published: bool = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
