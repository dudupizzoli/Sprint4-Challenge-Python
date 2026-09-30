import oracledb

class UsuarioDAO:
    def __init__(self, conexao):
        self.conexao = conexao

    def cadastrar_usuario(self, usuario):
        conn = self.conexao.conectar()
        if conn is None:
            return "Erro ao conectar ao Oracle."

        cursor = conn.cursor()
        sql = """insert into usuarios_soulup (username, senha, email) 
        values (:username, :senha, :email)"""

        try:
            cursor.execute(sql,
                           username = usuario.username,
                           senha = usuario.senha,
                           email = usuario.email)
            conn.commit()
            print("Cadastro realizado com sucesso!")
        except oracledb.Error as erro:
            conn.rollback()
            print("\nFalha ao cadastrar no banco:", erro)
    
        finally:
            cursor.close()
            conn.close() 

        