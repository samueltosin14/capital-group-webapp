from sqlalchemy.orm import Session

from app.models import Customer, Enquiry, NewsletterSubscriber, QuoteRequest
from app.schemas import EnquiryCreate, QuoteRequestCreate


def get_or_create_customer(db: Session, payload: EnquiryCreate | QuoteRequestCreate) -> Customer:
    customer = db.query(Customer).filter(Customer.email == payload.email).first()
    if customer:
        customer.full_name = payload.full_name
        customer.phone = payload.phone
        customer.company_name = payload.company_name
        customer.city = payload.city
        return customer
    customer = Customer(
        full_name=payload.full_name,
        email=str(payload.email),
        phone=payload.phone,
        company_name=payload.company_name,
        city=payload.city,
    )
    db.add(customer)
    db.flush()
    return customer


def create_enquiry(db: Session, payload: EnquiryCreate) -> Enquiry:
    customer = get_or_create_customer(db, payload)
    enquiry = Enquiry(customer_id=customer.id, subject=payload.subject, message=payload.message)
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    return enquiry


def create_quote_request(db: Session, payload: QuoteRequestCreate, document_path: str | None = None) -> QuoteRequest:
    customer = get_or_create_customer(db, payload)
    quote = QuoteRequest(
        customer_id=customer.id,
        service_id=payload.service_id,
        project_location=payload.project_location,
        budget_range=payload.budget_range,
        desired_start_date=payload.desired_start_date,
        details=payload.details,
        document_path=document_path,
    )
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote


def subscribe_newsletter(db: Session, email: str) -> NewsletterSubscriber:
    subscriber = db.query(NewsletterSubscriber).filter(NewsletterSubscriber.email == email).first()
    if subscriber:
        subscriber.is_active = True
    else:
        subscriber = NewsletterSubscriber(email=email)
        db.add(subscriber)
    db.commit()
    db.refresh(subscriber)
    return subscriber
