# Capital Group Web Application

Production-style FastAPI application for Capital Group, a construction company operating mainly in France. The app is ready for local development now and structured for later deployment to Azure France Central with Azure SQL Database, VM Scale Sets, Application Gateway WAF, and Azure Storage.

## Stack

- FastAPI, Uvicorn, Gunicorn
- Jinja2 templates, Bootstrap 5, HTML/CSS/JavaScript
- SQLAlchemy ORM and Alembic migrations
- Azure SQL compatible database configuration through `DATABASE_URL`
- Session/JWT admin authentication, password hashing, CSRF protection, secure headers
- Structured JSON logging with `structlog`
- Pytest test suite
- Docker and Docker Compose

## Run Locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

Default local admin credentials come from `.env`:

```text
ADMIN_EMAIL=admin@capitalgroup.fr
ADMIN_PASSWORD=ChangeMe123!
```

Admin dashboard: `http://127.0.0.1:8000/admin/login`

## Tests

```powershell
pytest
```

## Docker

```powershell
Copy-Item .env.example .env
docker compose up --build
```

The container exposes port `8000` and persists local uploads through `./uploads`.

## Azure SQL Configuration

For Azure SQL Database, replace `DATABASE_URL` in `.env` or the App Service/VMSS environment with a SQLAlchemy `pyodbc` connection string:

```text
DATABASE_URL=mssql+pyodbc://USER:PASSWORD@SERVER.database.windows.net:1433/DBNAME?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no
```

Run migrations against the configured database:

```powershell
alembic upgrade head
```

The schema uses string UUID primary keys, explicit relationships, foreign keys, timestamps, and indexes compatible with Azure SQL. Production hosts need Microsoft ODBC Driver 18 for SQL Server installed before using the `mssql+pyodbc` URL.

## Important Folders

- `app/core`: settings, logging, and security helpers. Terraform should map Key Vault/App Gateway/VMSS secrets into these environment variables.
- `app/db`: SQLAlchemy session setup and seed data.
- `app/models.py`: database schema source of truth.
- `app/routers`: public pages, REST API, and admin routes.
- `app/services/storage.py`: local upload abstraction. This is the future integration point for Azure Blob Storage.
- `templates`: Jinja2 frontend and admin dashboard.
- `static`: CSS and JavaScript assets.
- `migrations`: Alembic environment and initial migration.
- `uploads`: local project image and document storage. In Azure, replace or mount this with Blob-backed storage.
- `.env.example`: required runtime configuration for Terraform variables, VMSS custom data, or Azure App Configuration.
- `Dockerfile` and `docker-compose.yml`: container entry points for VMSS image builds or registry deployment.

## Health Endpoints

- `/health`: process health
- `/ready`: database readiness probe

These are suitable for Azure Application Gateway probes or VMSS health extension wiring.

## Deployment Notes

For Azure France Central, provision these components with Terraform later:

- Azure SQL Database and firewall/private endpoint rules
- Azure Storage Account for uploads and static media
- Azure Container Registry or VM image build pipeline
- VM Scale Set running the Docker image or a systemd Gunicorn service
- Application Gateway WAF with TLS termination and probes for `/health` and `/ready`
- Key Vault secrets for `SECRET_KEY`, admin bootstrap credentials, and `DATABASE_URL`
