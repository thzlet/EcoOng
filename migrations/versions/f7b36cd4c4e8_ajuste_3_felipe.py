"""ajuste 3 - Felipe

Revision ID: f7b36cd4c4e8
Revises: cf21ade20ae4
Create Date: 2021-10-22 17:52:12.724615

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f7b36cd4c4e8'
down_revision = 'cf21ade20ae4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('membro', schema=None) as batch_op:
        batch_op.add_column(sa.Column('membro_telefone', sa.String(length=20), nullable=False))
        batch_op.drop_column('telefone')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('membro', schema=None) as batch_op:
        batch_op.add_column(sa.Column('telefone', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
        batch_op.drop_column('membro_telefone')

    # ### end Alembic commands ###