def test_create_enquiry_api(client):
    response = client.post(
        "/api/enquiries",
        json={
            "full_name": "Marie Dubois",
            "email": "marie@example.com",
            "phone": "+33 6 00 00 00 00",
            "city": "Lyon",
            "subject": "Apartment renovation",
            "message": "We need a contractor for a full apartment renovation in Lyon.",
        },
    )

    assert response.status_code == 201
    assert response.json()["subject"] == "Apartment renovation"


def test_admin_login_and_create_project(client):
    login = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "ChangeMe123!"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    project = client.post(
        "/api/projects",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Nice Seafront Offices",
            "slug": "nice-seafront-offices",
            "location": "Nice",
            "description": "Commercial office refurbishment near the Promenade des Anglais.",
            "client_name": "Azur Holdings",
            "year_completed": 2026,
            "is_featured": True,
            "is_published": True,
        },
    )

    assert project.status_code == 201
    assert project.json()["location"] == "Nice"
