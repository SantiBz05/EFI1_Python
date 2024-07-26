"""Actualizacion Stock cambia por Inventario-Logica de Inventario)

Revision ID: 74785fca4cd3
Revises: 25b004cceb9d
Create Date: 2024-07-25 23:16:52.329051

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '74785fca4cd3'
down_revision = '25b004cceb9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('producto', sa.String(length=10), nullable=False),
    sa.Column('tipo', sa.String(length=10), nullable=False),
    sa.Column('cantidadDisponible', sa.Integer(), nullable=False),
    sa.Column('ubicacionAlmacen', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('stock')
    with op.batch_alter_table('accesorios', schema=None) as batch_op:
        batch_op.drop_constraint('accesorios_ibfk_1', type_='foreignkey')
        batch_op.drop_column('stock_id')

    with op.batch_alter_table('equipo', schema=None) as batch_op:
        batch_op.drop_constraint('equipo_ibfk_6', type_='foreignkey')
        batch_op.drop_column('stock_id')

    with op.batch_alter_table('modelo', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'categoria', ['categoria_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('modelo', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('equipo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stock_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('equipo_ibfk_6', 'stock', ['stock_id'], ['id'])

    with op.batch_alter_table('accesorios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stock_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('accesorios_ibfk_1', 'stock', ['stock_id'], ['id'])

    op.create_table('stock',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('cantidadDisponible', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('ubicacionAlmacen', mysql.VARCHAR(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('inventario')
    # ### end Alembic commands ###
