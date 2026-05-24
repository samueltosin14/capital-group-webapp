from app.db.seed import seed_data
from app.models import Project, Service


def test_seed_data_creates_services_and_projects(client):
    from app.db.session import SessionLocal

    with SessionLocal() as db:
        seed_data(db)
        assert db.query(Service).count() >= 5
        assert db.query(Project).count() >= 3
