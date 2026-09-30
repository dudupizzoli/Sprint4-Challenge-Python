import oracledb

class Conexaodb:

    def __init__(self, usuario, senha, host, porta, service_name):
        self.usuario = usuario
        self.senha = senha
        self.host = host
        self.porta = porta
        self.service_name = service_name

        self.dsn = oracledb.makedsn(
            host,
            porta,
            service_name=service_name
        )

    def conectar(self):
        try:
            conn = oracledb.connect(
                user=self.usuario,
                password=self.senha,
                dsn=self.dsn
            )
            return conn

        except oracledb.Error as erro:
            print("Erro ao se conectar ao Oracle:", erro)
            return None


        


