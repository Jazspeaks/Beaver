"""title

Revision ID: ce5e984f5190
Revises: 
Create Date: 2024-08-27 19:12:04.178577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce5e984f5190'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cv', schema=None) as batch_op:
        batch_op.drop_column('date_of_birth')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('title')

    with op.batch_alter_table('cv', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_of_birth', sa.VARCHAR(length=10), nullable=True))

    # ### end Alembic commands ###
