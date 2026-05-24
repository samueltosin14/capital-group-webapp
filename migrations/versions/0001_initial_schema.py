"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-24
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.String(36), primary_key=True), sa.Column("email", sa.String(255), nullable=False), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("full_name", sa.String(150), nullable=False), sa.Column("role", sa.String(50), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_role", "users", ["role"])
    op.create_table("customers", sa.Column("id", sa.String(36), primary_key=True), sa.Column("full_name", sa.String(150), nullable=False), sa.Column("email", sa.String(255), nullable=False), sa.Column("phone", sa.String(40)), sa.Column("company_name", sa.String(150)), sa.Column("city", sa.String(120)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_customers_email", "customers", ["email"])
    op.create_index("ix_customers_city", "customers", ["city"])
    op.create_table("services", sa.Column("id", sa.String(36), primary_key=True), sa.Column("name", sa.String(120), nullable=False, unique=True), sa.Column("slug", sa.String(140), nullable=False, unique=True), sa.Column("description", sa.Text(), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_services_slug", "services", ["slug"], unique=True)
    op.create_table("newsletter_subscribers", sa.Column("id", sa.String(36), primary_key=True), sa.Column("email", sa.String(255), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("email", name="uq_newsletter_email"))
    op.create_index("ix_newsletter_subscribers_email", "newsletter_subscribers", ["email"])
    op.create_table("testimonials", sa.Column("id", sa.String(36), primary_key=True), sa.Column("client_name", sa.String(150), nullable=False), sa.Column("client_title", sa.String(150)), sa.Column("content", sa.Text(), nullable=False), sa.Column("rating", sa.Integer(), nullable=False), sa.Column("is_published", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_testimonials_is_published", "testimonials", ["is_published"])
    op.create_table("projects", sa.Column("id", sa.String(36), primary_key=True), sa.Column("service_id", sa.String(36), sa.ForeignKey("services.id", ondelete="SET NULL")), sa.Column("title", sa.String(180), nullable=False), sa.Column("slug", sa.String(200), nullable=False, unique=True), sa.Column("location", sa.String(150), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("client_name", sa.String(150)), sa.Column("year_completed", sa.Integer()), sa.Column("is_featured", sa.Boolean(), nullable=False), sa.Column("is_published", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_projects_service_id", "projects", ["service_id"])
    op.create_index("ix_projects_slug", "projects", ["slug"], unique=True)
    op.create_index("ix_projects_location", "projects", ["location"])
    op.create_index("ix_projects_is_featured", "projects", ["is_featured"])
    op.create_index("ix_projects_is_published", "projects", ["is_published"])
    op.create_table("project_images", sa.Column("id", sa.String(36), primary_key=True), sa.Column("project_id", sa.String(36), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False), sa.Column("file_path", sa.String(500), nullable=False), sa.Column("alt_text", sa.String(255)), sa.Column("sort_order", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_project_images_project_id", "project_images", ["project_id"])
    op.create_table("enquiries", sa.Column("id", sa.String(36), primary_key=True), sa.Column("customer_id", sa.String(36), sa.ForeignKey("customers.id", ondelete="CASCADE"), nullable=False), sa.Column("subject", sa.String(200), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("status", sa.Enum("new", "in_progress", "closed", name="enquirystatus"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_enquiries_customer_id", "enquiries", ["customer_id"])
    op.create_index("ix_enquiries_status", "enquiries", ["status"])
    op.create_table("quote_requests", sa.Column("id", sa.String(36), primary_key=True), sa.Column("customer_id", sa.String(36), sa.ForeignKey("customers.id", ondelete="CASCADE"), nullable=False), sa.Column("service_id", sa.String(36), sa.ForeignKey("services.id", ondelete="SET NULL")), sa.Column("project_location", sa.String(150), nullable=False), sa.Column("budget_range", sa.String(80)), sa.Column("desired_start_date", sa.String(40)), sa.Column("details", sa.Text(), nullable=False), sa.Column("document_path", sa.String(500)), sa.Column("status", sa.Enum("requested", "reviewing", "quoted", "declined", name="quotestatus"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_quote_requests_customer_id", "quote_requests", ["customer_id"])
    op.create_index("ix_quote_requests_service_id", "quote_requests", ["service_id"])
    op.create_index("ix_quote_requests_project_location", "quote_requests", ["project_location"])
    op.create_index("ix_quote_requests_status", "quote_requests", ["status"])
    op.create_table("audit_logs", sa.Column("id", sa.String(36), primary_key=True), sa.Column("actor_user_id", sa.String(36), sa.ForeignKey("users.id", ondelete="SET NULL")), sa.Column("action", sa.String(120), nullable=False), sa.Column("entity_type", sa.String(120), nullable=False), sa.Column("entity_id", sa.String(36)), sa.Column("ip_address", sa.String(64)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_audit_logs_actor_user_id", "audit_logs", ["actor_user_id"])
    op.create_index("ix_audit_logs_entity_id", "audit_logs", ["entity_id"])
    op.create_index("ix_audit_actor_action", "audit_logs", ["actor_user_id", "action"])


def downgrade() -> None:
    for table in ["audit_logs", "quote_requests", "enquiries", "project_images", "projects", "testimonials", "newsletter_subscribers", "services", "customers", "users"]:
        op.drop_table(table)
