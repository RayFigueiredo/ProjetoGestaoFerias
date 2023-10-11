import mysql.connector

# CONEXÃO COM BD LOCAL MYSQL
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Mack#2351',
    database='bdferias'
)
cursor = conexao.cursor()

# CONEXÃO COM BD MY SQL NA NUVEM SERVIDOR RAILWAY - FERIAS

# conexao = mysql.connector.connect(
#     host='containers-us-west-87.railway.app',
#     user='root',
#     password='945bo1bQFfqgqWY3NtLH',
#     database='railway',
#     port='6810'
# )
# cursor = conexao.cursor()

cursor.close()
conexao.close()
