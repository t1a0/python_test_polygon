from alembic import op

def upgrade():
    op.create_index('book_genre_index', 'books', ['genre'], unique=False)

def downgrade():
    op.drop_index('book_genre_index', table_name='books')
