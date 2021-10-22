"""modificação do telefone

Revision ID: 7e1891442502
Revises: 123e52b41940
Create Date: 2021-10-21 20:16:14.802359

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7e1891442502'
down_revision = '123e52b41940'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('membro', schema=None) as batch_op:
        batch_op.alter_column('telefone',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('membro', schema=None) as batch_op:
        batch_op.alter_column('telefone',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    # ### end Alembic commands ###
