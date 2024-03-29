"""empty message

Revision ID: 65d62b661617
Revises: 26c8f031f541
Create Date: 2023-01-17 17:02:01.173215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65d62b661617'
down_revision = '26c8f031f541'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('visita',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome_voluntario', sa.String(length=100), nullable=True),
    sa.Column('nome_asilo', sa.String(length=100), nullable=True),
    sa.Column('data', sa.Date(), nullable=True),
    sa.Column('hora', sa.Time(), nullable=True),
    sa.Column('motivo', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('asilo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('cep', sa.String(length=100), nullable=True),
    sa.Column('cnpj', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('voluntario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('cpf_cnpj', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('voluntario')
    op.drop_table('asilo')
    op.drop_table('visita')
    # ### end Alembic commands ###
