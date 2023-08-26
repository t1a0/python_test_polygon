from alembic import op
import sqlalchemy as sa
revision = '1_create_books_table'
def upgrade() :
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('author', sa.String(), nullable=False),
    sa.Column('date_of_release', sa.Date(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('genre', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('books')
