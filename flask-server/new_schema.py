import psycopg2

conn = psycopg2.connect(database="sever_db",
                        host="localhost",
                        user="postgres",
                        password="password",
                        port="5432")

cur = conn.cursor()

cur.execute("""INSERT INTO types_t (name) VALUES ('Other');
""")

conn.commit()
cur.close()
conn.close()
