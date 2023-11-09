import mysql.connector

# CONEXÃO COM BD LOCAL MYSQL
# conexao = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='Mack#2351',
#     database='bdferias'
# )
# cursor = conexao.cursor()

# CONEXÃO COM BD MY SQL NA NUVEM SERVIDOR RAILWAY - FERIAS

# conexao = mysql.connector.connect(
#     host='containers-us-west-87.railway.app',
#     user='root',
#     password='945bo1bQFfqgqWY3NtLH',
#     database='railway',
#     port='6810'
# )

# Banco de Dados AWS
try:

    conexao = mysql.connector.connect(
        host='dbferias.ccftvaia78r3.us-east-1.rds.amazonaws.com',
        user='admin',
        password='15b6688e71b5def74f934ded82bddc76',
        database='bdferias',
        port='3306'
    )

    cursor = conexao.cursor()

    cursor.close()
    conexao.close()

except mysql.connector.Error as err:
    print(f"Erro ao conectar ao banco de dados: {err}")
