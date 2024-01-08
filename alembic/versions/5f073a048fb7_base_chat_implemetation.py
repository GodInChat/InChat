"""base_chat_implemetation

Revision ID: 5f073a048fb7
Revises: e18b23480cdf
Create Date: 2024-01-06 20:29:58.442571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f073a048fb7'
down_revision: Union[str, None] = 'e18b23480cdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.Column('crated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chats_id'), 'chats', ['id'], unique=True)
    op.create_table('messages',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('chat_id', sa.Uuid(), nullable=False),
    sa.Column('text', sa.String(length=300), nullable=False),
    sa.Column('owner_type', sa.Enum('HumanMessage', 'AIMessage', name='owner_type'), nullable=False),
    sa.Column('crated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=True)
    op.add_column('pdfs', sa.Column('pdf_name', sa.String(length=300), nullable=False))
    op.drop_column('pdfs', 'pdf_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pdfs', sa.Column('pdf_url', sa.VARCHAR(length=300), autoincrement=False, nullable=False))
    op.drop_column('pdfs', 'pdf_name')
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')
    op.drop_index(op.f('ix_chats_id'), table_name='chats')
    op.drop_table('chats')
    # ### end Alembic commands ###