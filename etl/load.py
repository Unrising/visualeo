from sqlalchemy import create_engine, text
import os

def load_data(df, table_name):

    db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@postgres:5432/dbname')
    engine = create_engine(db_url)

    with engine.begin() as connection:
        if table_name == 'crypto_current':
            df.to_sql(table_name, con=connection, if_exists='append', index=False)
        elif table_name == 'crypto_historical':
            insert_query = text(f"""
                INSERT INTO {table_name} (coin_id, date, price, market_cap, volume)
                VALUES (:coin_id, :date, :price, :market_cap, :volume)
                ON CONFLICT (coin_id, date) DO UPDATE
                SET price = EXCLUDED.price,
                    market_cap = EXCLUDED.market_cap,
                    volume = EXCLUDED.volume;
            """)
            data_dicts = df.to_dict(orient="records")
            connection.execute(insert_query, data_dicts)
        else:
            raise ValueError("Invalid table name. Use 'crypto_current' or 'crypto_historical'.")
