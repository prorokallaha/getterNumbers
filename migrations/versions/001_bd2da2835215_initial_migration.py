"""Initial migration

Revision ID: 001_bd2da2835215
Revises: 
Create Date: 2024-05-08 22:59:51.104722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_bd2da2835215'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commands',
    sa.Column('tag', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tag')
    )
    with op.batch_alter_table('commands', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_commands_id'), ['id'], unique=False)

    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('is_bot', sa.Boolean(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('number', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('language_code', sa.String(), nullable=True),
    sa.Column('is_premium', sa.Boolean(), nullable=True),
    sa.Column('added_to_attachment_menu', sa.Boolean(), nullable=True),
    sa.Column('can_join_groups', sa.Boolean(), nullable=True),
    sa.Column('can_read_all_group_messages', sa.Boolean(), nullable=True),
    sa.Column('supports_inline_queries', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_id'), ['id'], unique=False)

    op.create_table('messages',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('message', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_messages_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_messages_id'))

    op.drop_table('messages')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_id'))

    op.drop_table('users')
    with op.batch_alter_table('commands', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_commands_id'))

    op.drop_table('commands')
    # ### end Alembic commands ###
