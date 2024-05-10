"""check updates

Revision ID: 000000000006_097bc37a26a7
Revises: 000000000005_cf1c87611618
Create Date: 2024-05-09 12:14:48.389001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '000000000006_097bc37a26a7'
down_revision = '000000000005_cf1c87611618'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commands', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_item_id', sa.String(), nullable=True))
        batch_op.drop_column('image')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commands', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=True))
        batch_op.drop_column('image_item_id')

    # ### end Alembic commands ###