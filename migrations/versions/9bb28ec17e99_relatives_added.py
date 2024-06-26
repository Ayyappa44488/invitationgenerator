"""relatives added

Revision ID: 9bb28ec17e99
Revises: 94e945e8c6bb
Create Date: 2024-06-26 11:03:56.162992

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9bb28ec17e99'
down_revision = '94e945e8c6bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('relatives',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('couple_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('relation', sa.String(length=80), nullable=False),
    sa.Column('image', sa.LargeBinary(length=4294967295), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['couple_id'], ['couples.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('couples', schema=None) as batch_op:
        batch_op.alter_column('image',
               existing_type=mysql.LONGBLOB(),
               type_=sa.LargeBinary(length=4294967295),
               existing_nullable=False)
        batch_op.drop_column('relative2')
        batch_op.drop_column('relation3')
        batch_op.drop_column('relative1')
        batch_op.drop_column('relation1')
        batch_op.drop_column('relation2')
        batch_op.drop_column('relative3')

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

    with op.batch_alter_table('couples', schema=None) as batch_op:
        batch_op.add_column(sa.Column('relative3', mysql.VARCHAR(length=80), nullable=False))
        batch_op.add_column(sa.Column('relation2', mysql.VARCHAR(length=80), nullable=False))
        batch_op.add_column(sa.Column('relation1', mysql.VARCHAR(length=80), nullable=False))
        batch_op.add_column(sa.Column('relative1', mysql.VARCHAR(length=80), nullable=False))
        batch_op.add_column(sa.Column('relation3', mysql.VARCHAR(length=80), nullable=False))
        batch_op.add_column(sa.Column('relative2', mysql.VARCHAR(length=80), nullable=False))
        batch_op.alter_column('image',
               existing_type=sa.LargeBinary(length=4294967295),
               type_=mysql.LONGBLOB(),
               existing_nullable=False)

    op.drop_table('relatives')
    # ### end Alembic commands ###