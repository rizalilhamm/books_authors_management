-- Drop existing tables if they exist
DROP TABLE IF EXISTS "BooksAuthors" CASCADE;
DROP TABLE IF EXISTS "FavoriteBook" CASCADE;
DROP TABLE IF EXISTS "Books" CASCADE;
DROP TABLE IF EXISTS "Authors" CASCADE;
DROP TABLE IF EXISTS "User" CASCADE;

-- Create User table
CREATE TABLE "User" (
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    PRIMARY KEY (username)
);

-- Create Authors table
CREATE TABLE "Authors" (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    gender VARCHAR(50),
    ratings_count INTEGER NOT NULL,
    average_rating FLOAT NOT NULL,
    text_reviews_count INTEGER NOT NULL,
    works_count INTEGER NOT NULL,
    book_ids JSONB,
    work_ids JSONB,
    image_url VARCHAR(200),
    about TEXT,
    fans_count INTEGER NOT NULL
);

-- Create Books table
CREATE TABLE "Books" (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    work_id VARCHAR(255) NOT NULL,
    isbn VARCHAR(20),
    isbn13 VARCHAR(20),
    asin VARCHAR(20),
    language VARCHAR(50) NOT NULL,
    average_rating FLOAT NOT NULL,
    rating_dist TEXT NOT NULL,
    ratings_count INTEGER NOT NULL,
    text_reviews_count INTEGER NOT NULL,
    publication_date VARCHAR(255),
    original_publication_date VARCHAR(255),
    format VARCHAR(50),
    edition_information VARCHAR(100),
    image_url VARCHAR(200),
    publisher VARCHAR(100),
    num_pages INTEGER,
    series_id VARCHAR(255),
    series_name VARCHAR(255),
    series_position VARCHAR(10),
    shelves JSONB,
    description TEXT NOT NULL
);

-- Create FavoriteBook table
CREATE TABLE "FavoriteBook" (
    id SERIAL PRIMARY KEY,
    user_username VARCHAR(150) NOT NULL,
    book_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_username, book_id),
    FOREIGN KEY (user_username) REFERENCES "User"(username) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES "Books"(id) ON DELETE CASCADE
);

-- Create BooksAuthors table
CREATE TABLE "Books_authors" (
    book_id VARCHAR(255) NOT NULL,
    author_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES "Books"(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES "Authors"(id) ON DELETE CASCADE
);

-- Create indices for optimization

-- User table index
CREATE INDEX idx_user_username ON "User" (username);

-- Authors table indices
CREATE INDEX idx_authors_name ON "Authors" (name);
CREATE INDEX idx_authors_ratings_count ON "Authors" (ratings_count);
CREATE INDEX idx_authors_average_rating ON "Authors" (average_rating);

-- Books table indices
CREATE INDEX idx_books_title ON "Books" (title);
CREATE INDEX idx_books_language ON "Books" (language);
CREATE INDEX idx_books_average_rating ON "Books" (average_rating);
CREATE INDEX idx_books_ratings_count ON "Books" (ratings_count);
CREATE INDEX idx_books_authors ON "Books" USING btree (id);

-- FavoriteBook table indices
CREATE INDEX idx_favoritebook_user ON "FavoriteBook" (user_username);
CREATE INDEX idx_favoritebook_book ON "FavoriteBook" (book_id);
CREATE INDEX idx_favoritebook_created_at ON "FavoriteBook" (created_at);

-- BooksAuthors table indices
CREATE INDEX idx_books_authors_book ON "Books_authors" (book_id);
CREATE INDEX idx_books_authors_author ON "Books_authors" (author_id);