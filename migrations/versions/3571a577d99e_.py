"""empty message

Revision ID: 3571a577d99e
Revises: 969ac1d63c59
Create Date: 2023-12-08 09:59:57.563898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3571a577d99e'
down_revision = '969ac1d63c59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notificacao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.Column('mensagem', sa.String(length=100), nullable=True),
    sa.Column('dt_hr', sa.DateTime(), nullable=True),
    sa.Column('eacao', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notificacao')
    # ### end Alembic commands ###
