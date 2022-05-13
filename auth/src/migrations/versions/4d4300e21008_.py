"""empty message

Revision ID: 4d4300e21008
Revises: 
Create Date: 2022-05-12 11:58:25.307129

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4d4300e21008'
down_revision = None
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
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('social_id', 'social_name', name='social_uc'),
    schema='content'
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