"""empty message

Revision ID: 5b84554aff1d
Revises: 1916dd669c1d
Create Date: 2023-02-05 21:05:04.777924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b84554aff1d'
down_revision = '1916dd669c1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'asilo', ['id_usuario'])
    op.create_foreign_key(None, 'asilo', 'usuario', ['id_usuario'], ['id'])
    op.add_column('visita', sa.Column('id_asilo', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'visita', ['id_usuario'])
    op.create_unique_constraint(None, 'visita', ['id_asilo'])
    op.create_foreign_key(None, 'visita', 'asilo', ['id_asilo'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'visita', type_='foreignkey')
    op.drop_constraint(None, 'visita', type_='unique')
    op.drop_constraint(None, 'visita', type_='unique')
    op.drop_column('visita', 'id_asilo')
    op.drop_constraint(None, 'asilo', type_='foreignkey')
    op.drop_constraint(None, 'asilo', type_='unique')
    # ### end Alembic commands ###
