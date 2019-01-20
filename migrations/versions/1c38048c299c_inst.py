"""inst

Revision ID: 1c38048c299c
Revises: f824289dc09e
Create Date: 2017-12-30 18:11:37.953000

"""

# revision identifiers, used by Alembic.
revision = '1c38048c299c'
down_revision = 'f824289dc09e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('classes', sa.Column('instructor_username', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_classes_instructor_username'), 'classes', ['instructor_username'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_classes_instructor_username'), table_name='classes')
    op.drop_column('classes', 'instructor_username')
    # ### end Alembic commands ###