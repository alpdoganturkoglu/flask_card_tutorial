"""users table

Revision ID: 1e89489645f6
Revises: 
Create Date: 2021-02-09 14:09:18.043798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e89489645f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=160), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('topic', sa.String(length=80), nullable=False),
    sa.Column('question', sa.String(length=160), nullable=False),
    sa.Column('created_time', sa.DateTime(), nullable=False),
    sa.Column('updated_time', sa.DateTime(), nullable=False),
    sa.Column('auth_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['auth_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cards')
    op.drop_table('user')
    # ### end Alembic commands ###
