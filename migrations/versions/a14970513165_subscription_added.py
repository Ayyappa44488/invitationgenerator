"""subscription added

Revision ID: a14970513165
Revises: 32c5d36947e8
Create Date: 2024-07-26 17:32:15.962040

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a14970513165'
down_revision = '32c5d36947e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('couples', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=4294967295),
               existing_nullable=False)

    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=4294967295),
               existing_nullable=False)

    with op.batch_alter_table('relatives', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=4294967295),
               existing_nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subscription', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('subscription')

    with op.batch_alter_table('relatives', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.LargeBinary(length=4294967295),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)

    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.LargeBinary(length=4294967295),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)

    with op.batch_alter_table('couples', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.LargeBinary(length=4294967295),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)

    # ### end Alembic commands ###
