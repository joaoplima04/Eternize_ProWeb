import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM alembic_version;")
result = cursor.fetchall()
print(result)  # Deve retornar uma lista vazia se a tabela estiver limpa
cursor.execute("DELETE FROM alembic_version;")
conn.commit()
conn.close()