"""create posts table

Revision ID: 1db3ae1e4cb2
Revises: 
Create Date: 2026-10-12 15:39:02.592824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1db3ae1e4cb2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id', sa.Integer(), primary_key=True,nullable = False, autoincrement=True), 
                    sa.Column('title', sa.String(length=255), nullable=False), sa.Column('content', sa.Text(), nullable=False), 
                    sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False), 
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
