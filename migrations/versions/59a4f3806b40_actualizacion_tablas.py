"""Actualizacion Tablas

Revision ID: 59a4f3806b40
Revises: 7116ec235ccc
Create Date: 2024-07-27 16:29:50.408698

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '59a4f3806b40'
down_revision = '7116ec235ccc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock')
    with op.batch_alter_table('accesorios', schema=None) as batch_op:
        batch_op.drop_constraint('accesorios_ibfk_1', type_='foreignkey')
        batch_op.drop_column('stock_id')

    with op.batch_alter_table('inventario', schema=None) as batch_op:
        batch_op.alter_column('tipo',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.String(length=50),
               nullable=True)
        batch_op.alter_column('producto',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.String(length=100),
               nullable=True)
        batch_op.alter_column('cantidadDisponible',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
        batch_op.alter_column('ubicacionAlmacen',
               existing_type=mysql.VARCHAR(length=10),
               type_=sa.String(length=100),
               nullable=True)

    with op.batch_alter_table('marca', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fabricante_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'fabricante', ['fabricante_id'], ['id'])

    with op.batch_alter_table('modelo', schema=None) as batch_op:
        batch_op.drop_constraint('modelo_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'categoria', ['categoria_id'], ['id'])
        batch_op.drop_column('fabricante_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('modelo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fabricante_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('modelo_ibfk_1', 'fabricante', ['fabricante_id'], ['id'])

    with op.batch_alter_table('marca', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('fabricante_id')

    with op.batch_alter_table('inventario', schema=None) as batch_op:
        batch_op.alter_column('ubicacionAlmacen',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=10),
               nullable=False)
        batch_op.alter_column('cantidadDisponible',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.alter_column('producto',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=10),
               nullable=False)
        batch_op.alter_column('tipo',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=10),
               nullable=False)

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
    # ### end Alembic commands ###