from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_current_admin, verify_password
from app.db.session import get_db
from app.models import Enquiry, Project, ProjectImage, QuoteRequest, Testimonial, User
from app.schemas import EnquiryCreate, LoginRequest, ProjectCreate, QuoteRequestCreate, TestimonialCreate
from app.services.crud import create_enquiry, create_quote_request
from app.services.storage import save_upload

router = APIRouter(tags=["api"])


@router.post("/auth/login")
def api_login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email, User.is_active.is_(True)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": create_access_token(user.id, user.role), "token_type": "bearer"}


@router.get("/enquiries", dependencies=[Depends(get_current_admin)])
def list_enquiries(db: Session = Depends(get_db)):
    return db.query(Enquiry).order_by(Enquiry.created_at.desc()).all()


@router.post("/enquiries", status_code=201)
def create_enquiry_api(payload: EnquiryCreate, db: Session = Depends(get_db)):
    return create_enquiry(db, payload)


@router.get("/quote-requests", dependencies=[Depends(get_current_admin)])
def list_quote_requests(db: Session = Depends(get_db)):
    return db.query(QuoteRequest).order_by(QuoteRequest.created_at.desc()).all()


@router.post("/quote-requests", status_code=201)
def create_quote_request_api(payload: QuoteRequestCreate, db: Session = Depends(get_db)):
    return create_quote_request(db, payload)


@router.get("/projects")
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).filter(Project.is_published.is_(True)).order_by(Project.created_at.desc()).all()


@router.post("/projects", status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.put("/projects/{project_id}")
def update_project(project_id: str, payload: ProjectCreate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    for key, value in payload.model_dump().items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}", dependencies=[Depends(get_current_admin)])
def delete_project(project_id: str, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if project:
        db.delete(project)
        db.commit()
    return {"deleted": bool(project)}


@router.post("/projects/{project_id}/images", status_code=201)
async def upload_project_image(project_id: str, file: UploadFile = File(...), db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    path = await save_upload(file, "project-images")
    image = ProjectImage(project_id=project_id, file_path=path, alt_text=file.filename)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


@router.get("/testimonials")
def list_testimonials(db: Session = Depends(get_db)):
    return db.query(Testimonial).filter(Testimonial.is_published.is_(True)).all()


@router.post("/testimonials", status_code=201)
def create_testimonial(payload: TestimonialCreate, db: Session = Depends(get_db), _: User = Depends(get_current_admin)):
    testimonial = Testimonial(**payload.model_dump())
    db.add(testimonial)
    db.commit()
    db.refresh(testimonial)
    return testimonial
