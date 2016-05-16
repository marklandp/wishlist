"""empty message

Revision ID: 6da83eec3f47
Revises: fc95b21a4fa7
Create Date: 2016-04-24 13:58:53.945360

"""

# revision identifiers, used by Alembic.
revision = '6da83eec3f47'
down_revision = 'fc95b21a4fa7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wishes', sa.Column('bought', sa.String(length=1), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('wishes', 'bought')
    ### end Alembic commands ###
