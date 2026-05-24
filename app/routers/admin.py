from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, generate_csrf_token, get_current_admin, validate_csrf, verify_password
from app.db.session import get_db
from app.models import Customer, Enquiry, Project, ProjectImage, QuoteRequest, Service, Testimonial, User
from app.services.storage import save_upload

router = APIRouter(tags=["admin"])
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("admin/login.html", {"request": request, "csrf_token": generate_csrf_token(request)})


@router.post("/login")
def login(request: Request, csrf_token: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    validate_csrf(request, csrf_token)
    user = db.query(User).filter(User.email == email, User.is_active.is_(True)).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse("admin/login.html", {"request": request, "csrf_token": generate_csrf_token(request), "error": "Invalid email or password"}, status_code=401)
    response = RedirectResponse("/admin", status_code=303)
    response.set_cookie("capital_admin_token", create_access_token(user.id, user.role), httponly=True, secure=get_settings().session_cookie_secure, samesite="lax")
    return response


@router.post("/logout")
def logout(request: Request, csrf_token: str = Form(...)):
    validate_csrf(request, csrf_token)
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("capital_admin_token")
    return response


@router.get("", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "admin": admin,
            "csrf_token": generate_csrf_token(request),
            "project_count": db.query(Project).count(),
            "customer_count": db.query(Customer).count(),
            "enquiries": db.query(Enquiry).order_by(Enquiry.created_at.desc()).limit(10).all(),
            "quotes": db.query(QuoteRequest).order_by(QuoteRequest.created_at.desc()).limit(10).all(),
        },
    )


@router.get("/projects", response_class=HTMLResponse)
def admin_projects(request: Request, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return templates.TemplateResponse("admin/projects.html", {"request": request, "admin": admin, "csrf_token": generate_csrf_token(request), "projects": db.query(Project).order_by(Project.created_at.desc()).all(), "services": db.query(Service).all()})


@router.post("/projects")
async def create_project_form(
    request: Request,
    csrf_token: str = Form(...),
    title: str = Form(...),
    slug: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    service_id: str | None = Form(None),
    client_name: str | None = Form(None),
    year_completed: int | None = Form(None),
    is_featured: bool = Form(False),
    is_published: bool = Form(True),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    validate_csrf(request, csrf_token)
    project = Project(title=title, slug=slug, location=location, description=description, service_id=service_id or None, client_name=client_name, year_completed=year_completed, is_featured=is_featured, is_published=is_published)
    db.add(project)
    db.flush()
    if image and image.filename:
        db.add(ProjectImage(project_id=project.id, file_path=await save_upload(image, "project-images"), alt_text=title))
    db.commit()
    return RedirectResponse("/admin/projects", status_code=303)


@router.get("/enquiries", response_class=HTMLResponse)
def admin_enquiries(request: Request, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return templates.TemplateResponse("admin/enquiries.html", {"request": request, "admin": admin, "csrf_token": generate_csrf_token(request), "enquiries": db.query(Enquiry).order_by(Enquiry.created_at.desc()).all(), "quotes": db.query(QuoteRequest).order_by(QuoteRequest.created_at.desc()).all()})


@router.get("/testimonials", response_class=HTMLResponse)
def admin_testimonials(request: Request, db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    return templates.TemplateResponse("admin/testimonials.html", {"request": request, "admin": admin, "csrf_token": generate_csrf_token(request), "testimonials": db.query(Testimonial).order_by(Testimonial.created_at.desc()).all()})


@router.post("/testimonials")
def create_testimonial_form(request: Request, csrf_token: str = Form(...), client_name: str = Form(...), client_title: str | None = Form(None), content: str = Form(...), rating: int = Form(5), db: Session = Depends(get_db), admin: User = Depends(get_current_admin)):
    validate_csrf(request, csrf_token)
    db.add(Testimonial(client_name=client_name, client_title=client_title, content=content, rating=rating))
    db.commit()
    return RedirectResponse("/admin/testimonials", status_code=303)
