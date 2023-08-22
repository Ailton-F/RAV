"""Change Asylum or Asilo for Lar

Revision ID: 135ca262de79
Revises: 6b9d68e43ab9
Create Date: 2023-08-16 15:58:58.829621

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '135ca262de79'
down_revision = '6b9d68e43ab9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lar_de_idosos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=True),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('pix', sa.String(length=100), nullable=True),
    sa.Column('cep', sa.String(length=100), nullable=True),
    sa.Column('cnpj', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_usuario')
    )
    op.drop_index('id_usuario', table_name='asilo')
    op.drop_table('asilo')
    op.add_column('doacao', sa.Column('larNome', sa.String(length=100), nullable=True))
    op.drop_column('doacao', 'asiloName')
    op.add_column('visita', sa.Column('id_lar', sa.Integer(), nullable=True))
    op.add_column('visita', sa.Column('nome_lar', sa.String(length=100), nullable=True))
    op.drop_constraint('visita_ibfk_1', 'visita', type_='foreignkey')
    op.create_foreign_key(None, 'visita', 'lar_de_idosos', ['id_lar'], ['id'])
    op.drop_column('visita', 'id_asilo')
    op.drop_column('visita', 'nome_asilo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('visita', sa.Column('nome_asilo', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('visita', sa.Column('id_asilo', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'visita', type_='foreignkey')
    op.create_foreign_key('visita_ibfk_1', 'visita', 'asilo', ['id_asilo'], ['id'])
    op.drop_column('visita', 'nome_lar')
    op.drop_column('visita', 'id_lar')
    op.add_column('doacao', sa.Column('asiloName', mysql.VARCHAR(length=100), nullable=True))
    op.drop_column('doacao', 'larNome')
    op.create_table('asilo',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('id_usuario', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('nome', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('cnpj', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('pix', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('cep', mysql.VARCHAR(length=100), nullable=True),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], name='asilo_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('id_usuario', 'asilo', ['id_usuario'], unique=False)
    op.drop_table('lar_de_idosos')
    # ### end Alembic commands ###
