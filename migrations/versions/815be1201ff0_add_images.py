"""add images

Revision ID: 815be1201ff0
Revises: 1256c2db6407
Create Date: 2024-06-16 00:16:25.064970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '815be1201ff0'
down_revision = '1256c2db6407'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invitation_id', sa.Integer(), nullable=False),
    sa.Column('image', sa.LargeBinary(length=4294967295), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['invitation_id'], ['invitations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###
