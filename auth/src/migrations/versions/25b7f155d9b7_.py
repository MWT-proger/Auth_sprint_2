"""empty message

Revision ID: 25b7f155d9b7
Revises: 1ca39e68df12
Create Date: 2022-05-14 16:26:13.930048

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '25b7f155d9b7'
down_revision = '1ca39e68df12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='content'
    )
    op.create_table('users',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('login', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login'),
    schema='content'
    )
    op.create_table('auth_history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('ip', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['content.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='content'
    )
    op.create_table('auth_token',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('refresh_token', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['content.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='content'
    )
    op.create_table('mf_authentication',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('secret', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['content.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='content'
    )
    op.create_table('roles_users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('role_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['content.roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['content.users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    schema='content'
    )
    op.create_table('social_accounts',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('social_id', sa.String(length=255), nullable=False),
    sa.Column('social_name', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['content.users.id'], ),
    sa.PrimaryKeyConstraint('id', 'social_name'),
    sa.UniqueConstraint('id', 'social_name'),
    sa.UniqueConstraint('social_id', 'social_name', name='social_uc'),
    schema='content',
    postgresql_partition_by='LIST (social_name)'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('social_accounts', schema='content')
    op.drop_table('roles_users', schema='content')
    op.drop_table('mf_authentication', schema='content')
    op.drop_table('auth_token', schema='content')
    op.drop_table('auth_history', schema='content')
    op.drop_table('users', schema='content')
    op.drop_table('roles', schema='content')
    # ### end Alembic commands ###
