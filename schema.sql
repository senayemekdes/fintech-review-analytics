CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(100)
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INT REFERENCES banks(bank_id),
    review_text TEXT,
    rating INT,
    review_date DATE,
    transformer_sentiment_label VARCHAR(20),
    transformer_sentiment_score FLOAT,
    identified_theme VARCHAR(100),
    source VARCHAR(100)
);