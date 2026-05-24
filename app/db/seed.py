from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.models import Project, Service, Testimonial, User


SERVICES = [
    ("Residential Construction", "residential-construction", "High-quality homes, extensions, and multi-unit residential developments."),
    ("Commercial Construction", "commercial-construction", "Commercial fit-outs, offices, retail spaces, and light industrial facilities."),
    ("Renovation", "renovation", "Sensitive renovation and energy-modernisation work for existing French properties."),
    ("Project Management", "project-management", "Planning, procurement, site coordination, reporting, and delivery governance."),
    ("Civil Engineering", "civil-engineering", "Groundworks, drainage, structural concrete, access roads, and public realm works."),
]


def seed_data(db: Session) -> None:
    settings = get_settings()
    if not db.query(User).filter(User.email == settings.admin_email).first():
        db.add(User(email=settings.admin_email, full_name="Capital Group Administrator", role="admin", password_hash=hash_password(settings.admin_password)))

    service_by_slug = {}
    for name, slug, description in SERVICES:
        service = db.query(Service).filter(Service.slug == slug).first()
        if not service:
            service = Service(name=name, slug=slug, description=description)
            db.add(service)
            db.flush()
        service_by_slug[slug] = service

    projects = [
        ("Lyon Riverside Apartments", "lyon-riverside-apartments", "Lyon", "A 42-unit residential scheme with low-carbon materials and coordinated riverfront logistics.", "residential-construction", 2025),
        ("Bordeaux Retail Renovation", "bordeaux-retail-renovation", "Bordeaux", "Full interior renovation and facade refresh for a premium retail unit in central Bordeaux.", "renovation", 2024),
        ("Marseille Logistics Yard", "marseille-logistics-yard", "Marseille", "Civil works package including drainage, reinforced slabs, and vehicle circulation routes.", "civil-engineering", 2025),
    ]
    for title, slug, location, description, service_slug, year in projects:
        if not db.query(Project).filter(Project.slug == slug).first():
            db.add(Project(title=title, slug=slug, location=location, description=description, service_id=service_by_slug[service_slug].id, year_completed=year, is_featured=True))

    if not db.query(Testimonial).first():
        db.add_all(
            [
                Testimonial(client_name="Claire Martin", client_title="Property Developer, Lyon", content="Capital Group kept a complex urban site moving with clear reporting and disciplined subcontractor coordination.", rating=5),
                Testimonial(client_name="Julien Moreau", client_title="Operations Director, Marseille", content="Their civil engineering team delivered the yard upgrade without disrupting our daily logistics schedule.", rating=5),
            ]
        )
    db.commit()
