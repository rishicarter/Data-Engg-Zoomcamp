import pandas as pd
from sqlalchemy import create_engine
import click

base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
filename = "yellow_tripdata_2019-01.csv.gz"

dtypes = {'VendorID': 'int64',
 'passenger_count': 'int64',
 'trip_distance': 'float64',
 'RatecodeID': 'int64',
 'store_and_fwd_flag': 'string',
 'PULocationID': 'int64',
 'DOLocationID': 'int64',
 'payment_type': 'int64',
 'fare_amount': 'float64',
 'extra': 'float64',
 'mta_tax': 'float64',
 'tip_amount': 'float64',
 'tolls_amount': 'float64',
 'improvement_surcharge': 'float64',
 'total_amount': 'float64',
 'congestion_surcharge': 'float64'}

parse_dates = [
    'tpep_pickup_datetime',
    'tpep_dropoff_datetime'
]


@click.command()
@click.option('--pg-user', default='root', help='Postgres User')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
def main(pg_user,pg_pass, pg_host, pg_port, pg_db, target_table):
    print("Hello from data-engg-zoomcamp!")
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    df_iter = pd.read_csv(f"{base_url}+{filename}", dtype=dtypes, parse_dates=parse_dates, iterator=True, chunksize=10000)

    first = True

    for df_chunk in df_iter:

        if first:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists="replace"
            )
            first = False
            print("Table created")

        # Insert chunk
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))


if __name__ == "__main__":
    main()
