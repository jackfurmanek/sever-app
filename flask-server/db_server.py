import psycopg2

conn = psycopg2.connect(database="sever_db",
                        host="localhost",
                        user="postgres",
                        password="password",
                        port="5432")

cur = conn.cursor()

cur.execute("""INSERT INTO quits
            (name, time_added, rate)
            VALUES
            ('Disney Plus','2022-01-01 12:00:00+00',15.99),
            ('Max','2022-01-01 12:00:00+00',16.99),
            ('Chipotle','2022-01-01 12:00:00+00',48.00)
;""")

conn.commit()
cur.close()
conn.close()
