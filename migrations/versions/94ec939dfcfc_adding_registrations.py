"""adding registrations

Revision ID: 94ec939dfcfc
Revises: 1c38048c299c
Create Date: 2017-12-31 11:12:18.853000

"""

# revision identifiers, used by Alembic.
revision = '94ec939dfcfc'
down_revision = '1c38048c299c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registrations',
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('class.id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class.id'], ['classes.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('registrations')
    # ### end Alembic commands ###
