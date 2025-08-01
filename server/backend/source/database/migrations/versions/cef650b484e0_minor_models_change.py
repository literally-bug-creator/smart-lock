"""Minor models change

Revision ID: cef650b484e0
Revises: 2a4fece191b8
Create Date: 2024-12-24 12:43:47.081240

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = "cef650b484e0"
down_revision: Union[str, None] = "2a4fece191b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("employee_images", sa.Column("file_key", sa.String(), nullable=False))
    op.drop_column("employee_images", "full_name")
    op.drop_column("employee_images", "file_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "employee_images",
        sa.Column("file_id", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "employee_images",
        sa.Column("full_name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("employee_images", "file_key")
    # ### end Alembic commands ###
