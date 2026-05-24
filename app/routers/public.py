from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.security import generate_csrf_token, validate_csrf
from app.db.session import get_db
from app.models import Project, Service, Testimonial
from app.schemas import EnquiryCreate, QuoteRequestCreate
from app.services.crud import create_enquiry, create_quote_request, subscribe_newsletter
from app.services.storage import save_upload

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def context(request: Request, db: Session) -> dict:
    return {"request": request, "csrf_token": generate_csrf_token(request), "services": db.query(Service).filter(Service.is_active.is_(True)).all()}


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    data = context(request, db)
    data.update(
        projects=db.query(Project).filter(Project.is_featured.is_(True), Project.is_published.is_(True)).limit(3).all(),
        testimonials=db.query(Testimonial).filter(Testimonial.is_published.is_(True)).limit(3).all(),
    )
    return templates.TemplateResponse("public/home.html", data)


@router.get("/about", response_class=HTMLResponse)
def about(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("public/about.html", context(request, db))


@router.get("/services", response_class=HTMLResponse)
def services(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("public/services.html", context(request, db))


@router.get("/projects", response_class=HTMLResponse)
def projects(request: Request, db: Session = Depends(get_db)):
    data = context(request, db)
    data["projects"] = db.query(Project).filter(Project.is_published.is_(True)).order_by(Project.created_at.desc()).all()
    return templates.TemplateResponse("public/projects.html", data)


@router.get("/contact", response_class=HTMLResponse)
def contact(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("public/contact.html", context(request, db))


@router.post("/contact")
async def submit_contact(
    request: Request,
    csrf_token: str = Form(...),
    full_name: str = Form(...),
    email: EmailStr = Form(...),
    phone: str | None = Form(None),
    company_name: str | None = Form(None),
    city: str | None = Form(None),
    subject: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db),
):
    validate_csrf(request, csrf_token)
    create_enquiry(db, EnquiryCreate(full_name=full_name, email=email, phone=phone, company_name=company_name, city=city, subject=subject, message=message))
    return RedirectResponse("/contact?submitted=1", status_code=303)


@router.get("/quote-request", response_class=HTMLResponse)
def quote_request(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("public/quote_request.html", context(request, db))


@router.post("/quote-request")
async def submit_quote(
    request: Request,
    csrf_token: str = Form(...),
    full_name: str = Form(...),
    email: EmailStr = Form(...),
    phone: str | None = Form(None),
    company_name: str | None = Form(None),
    city: str | None = Form(None),
    service_id: str | None = Form(None),
    project_location: str = Form(...),
    budget_range: str | None = Form(None),
    desired_start_date: str | None = Form(None),
    details: str = Form(...),
    document: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    validate_csrf(request, csrf_token)
    document_path = await save_upload(document, "quote-documents") if document and document.filename else None
    payload = QuoteRequestCreate(full_name=full_name, email=email, phone=phone, company_name=company_name, city=city, service_id=service_id or None, project_location=project_location, budget_range=budget_range, desired_start_date=desired_start_date, details=details)
    create_quote_request(db, payload, document_path)
    return RedirectResponse("/quote-request?submitted=1", status_code=303)


@router.post("/newsletter")
def newsletter(request: Request, csrf_token: str = Form(...), email: EmailStr = Form(...), db: Session = Depends(get_db)):
    validate_csrf(request, csrf_token)
    subscribe_newsletter(db, str(email))
    return RedirectResponse(str(request.headers.get("referer", "/")) + "?newsletter=1", status_code=303)
