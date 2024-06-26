"""guests not unique

Revision ID: 94e945e8c6bb
Revises: b59700387cec
Create Date: 2024-06-19 22:22:12.044762

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '94e945e8c6bb'
down_revision = 'b59700387cec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('couples', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=4294967295),
               existing_nullable=False)

    with op.batch_alter_table('guests', schema=None) as batch_op:
        batch_op.drop_index('phone')

    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=4294967295),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('images', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.LargeBinary(length=4294967295),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)

    with op.batch_alter_table('guests', schema=None) as batch_op:
        batch_op.create_index('phone', ['phone'], unique=True)

    with op.batch_alter_table('couples', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=sa.LargeBinary(length=4294967295),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)

    # ### end Alembic commands ###
