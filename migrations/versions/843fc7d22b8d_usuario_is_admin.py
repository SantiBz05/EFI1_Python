"""Usuario - is_admin

Revision ID: 843fc7d22b8d
Revises: 411da5436183
Create Date: 2024-09-24 21:51:52.133890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '843fc7d22b8d'
down_revision = '411da5436183'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_admin', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        batch_op.drop_column('is_admin')

    # ### end Alembic commands ###
