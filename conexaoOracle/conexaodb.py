import oracledb

class Conexaodb:

    try:
        dsnStr = oracledb.makedsn(
            "oracle.fiap.com.br",
            "1521",
            "ORCL"
        )

        #Conectando-se ao banco de dados
        conn = oracledb.connect(     
            user="USUARIO",
            password="SENHA",
            dsn=dsnStr
        )

        #Criando o cursor para realizar as operações do CRUD
        cursor = conn.cursor()
    except Exception as e:
        print("Ocorreu um erro: ", e)

     



