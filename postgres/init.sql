CREATE TABLE IF NOT EXISTS crypto_current (
    coin_id VARCHAR(50) PRIMARY KEY,
    symbol VARCHAR(10),
    name VARCHAR(100),
    price NUMERIC,
    market_cap BIGINT,
    volume BIGINT,
    retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS crypto_historical (
    coin_id VARCHAR(50),
    date DATE,
    price NUMERIC,
    market_cap BIGINT,
    volume BIGINT,
    PRIMARY KEY (coin_id, date)
);
