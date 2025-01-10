import pandas, csv
import os
from io import StringIO
from sqlalchemy import create_engine

def psql_insert_copy(table, conn, keys, data_iter):
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)
        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name
        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)

engine = create_engine('postgresql://username:password@127.0.0.1:5432/sonarr-main')


def main():
    directory = os.getcwd()
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            with open(os.path.join(directory, filename), encoding="utf-8") as csv_file:
                df = pandas.read_csv(csv_file)
                df.set_index(df.columns[0], inplace=True)
                table_name = '"' + filename[:-4] + '"'
                print(table_name)
                if table_name == '"Episodes"':
                    df["AbsoluteEpisodeNumber"] = df["AbsoluteEpisodeNumber"].astype(pandas.Int64Dtype())
                    df["AiredAfterSeasonNumber"] = df["AiredAfterSeasonNumber"].astype(pandas.Int64Dtype())
                    df["AiredBeforeSeasonNumber"] = df["AiredBeforeSeasonNumber"].astype(pandas.Int64Dtype())
                    df["AiredBeforeEpisodeNumber"] = df["AiredBeforeEpisodeNumber"].astype(pandas.Int64Dtype())
                    df["SceneAbsoluteEpisodeNumber"] = df["SceneAbsoluteEpisodeNumber"].astype(pandas.Int64Dtype())
                    df["SceneSeasonNumber"] = df["SceneSeasonNumber"].astype(pandas.Int64Dtype())
                    df["SceneEpisodeNumber"] = df["SceneEpisodeNumber"].astype(pandas.Int64Dtype())
                if table_name == '"SceneMappings"':
                    df["SceneSeasonNumber"] = df["SceneSeasonNumber"].astype(pandas.Int64Dtype())
                    df["SeasonNumber"] = df["SeasonNumber"].astype(pandas.Int64Dtype())
                try:
                    df.to_sql(table_name, engine, schema='public', method=psql_insert_copy, if_exists='replace')
                except Exception as e:
                    print("The table ", table_name, "failed to update")
                    print(e)
                    break

if __name__ == "__main__":
    main()

