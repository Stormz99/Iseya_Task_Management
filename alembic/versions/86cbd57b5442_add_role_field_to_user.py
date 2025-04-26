"""Add role field to user

Revision ID: 86cbd57b5442
Revises: 561045db199d
Create Date: 2025-03-15 13:58:11.715998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86cbd57b5442'
down_revision: Union[str, None] = '561045db199d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define the Enum type
role_enum = sa.Enum('admin', 'user', name='roleenum')

def upgrade() -> None:
    """Upgrade schema."""
    # Create the Enum type first
    role_enum.create(op.get_bind(), checkfirst=True)

    # Add 'role' column to 'users' table
    op.add_column('users', sa.Column('role', role_enum, nullable=False, server_default='user'))


def downgrade() -> None:
    """Downgrade schema."""
    # Drop 'role' column
    op.drop_column('users', 'role')

    # Drop Enum type
    role_enum.drop(op.get_bind(), checkfirst=True)
