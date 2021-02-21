"""create cat_breeds table

Revision ID: 1a6f11e32e5e
Revises: 
Create Date: 2021-02-21 16:04:40.128983

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '1a6f11e32e5e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "cat_breeds",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("public_id", UUID(as_uuid=True), nullable=False),
        sa.Column("breed", sa.String, nullable=False),
        sa.Column("location_origin", sa.String),
        sa.Column("coat_length", sa.Float),
        sa.Column("body_type", sa.String),
        sa.Column("pattern", sa.String),
    )


def downgrade():
    op.drop_table("cat_breeds")
