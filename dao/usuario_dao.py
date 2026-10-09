from conexaoOracle.conexaodb import Conexaodb
from models.usuario import Usuario
import oracledb

#O QUE FAZER AGORA: cuidar da exportação dos dados para JSON, fazer o menu e toda a solução funcionar de fato, fazer o html, testar
class UsuarioDAO:
    def __init__(self):
        self.conexao = Conexaodb(
            usuario="user",
            senha="senha",
            host="host",
            porta=1521,
            service_name="ORCL"
        )

    def cadastrar_usuario(self, usuario):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")

        username = usuario.username
        senha = usuario.senha
        email = usuario.email

        cursor = conn.cursor()
        sql = """insert into usuarios_soulup (username, senha, email) 
        values (:username, :senha, :email)"""

        try:
            cursor.execute(sql,
                           username = username,
                           senha = senha,
                           email = email)
            conn.commit()
            print("Cadastro realizado com sucesso!")

        except oracledb.Error as erro:
            conn.rollback()
            print("\nFalha ao cadastrar no banco:", erro)
    
        finally:
            cursor.close()
            conn.close() 

    def listar_usuarios(self):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.") 

        cursor = conn.cursor()
        sql = """select id_usuario, username, senha, email, pontos, passagens, vales, saldo, limite from usuarios_soulup order by id_usuario"""

        try:
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            if len(usuarios) == 0:
                return None
            else:
                return usuarios

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
            usuarios = []
                
        finally:
            cursor.close()
            conn.close()            

    def buscar_nome_usuario(self, username):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.") 
        
        cursor = conn.cursor()
        sql = """select id_usuario, username, senha, email, pontos, passagens, vales, saldo, limite from usuarios_soulup where username = :username"""

        try:
            cursor.execute(sql, username =username)
            usuario = cursor.fetchone()
            if usuario is None:
                return None
            else:
                return usuario              

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
                        
        finally:
            cursor.close()
            conn.close()

    #troquei o parâmetro do método acima. avaliar se vou trocar dos de baixo tbm
    def editar_usuario(self, nome_usuario):    
        usuario = self.buscar_nome_usuario(nome_usuario)

        if usuario is None:
            return None

        else:

            senha = input("Digite a senha da conta a ser editada: ").strip()

            if senha == usuario[2]:
                conn = self.conexao.conectar()
                if conn is None:
                    print("Erro ao conectar ao Oracle.")

                username = input(f"Seu nome de usuário atual é: {usuario[1]}, caso não queira mudá-lo, aperte enter. Digite seu novo nome de usuário: ").strip()
                email = input(f"Seu email atual é: {usuario[3]}, caso não queira mudá-lo, aperte enter. Digite seu novo email: ").strip()

                if username == '':
                    username = usuario[1]
                
                if email == '':
                    email = usuario[3]

                if email != '' and "@" not in email or len(email) < 8:
                    print("O email precisa ter @ e não pode ter menos de 8 caracteres.")

                cursor = conn.cursor()
                sql = """update usuarios_soulup 
                        set username = :username, 
                            email = :email 
                        where username = :nome_usuario 
                        """

                try:
                    cursor.execute(sql, username=username, email=email, nome_usuario=nome_usuario)
                    conn.commit()
                    print("Usuário editado com sucesso!")
                    return usuario
                except oracledb.Error as erro:
                    conn.rollback()
                    return f"Erro ao alterar: {erro}"
                finally:
                    cursor.close()
                    conn.close()

            else:
                print("Senha incorreta. Não foi possível editar o usuário.")

    def excluir_usuario(self, username):
        usuario = self.buscar_nome_usuario(username)

        confirmacao = input("A exclusão de uma conta é uma ação perigosa e potencialmente irreversível. Você realmente deseja excluir esta conta? (S para Sim/N para Não)").upper().strip()
        if confirmacao == "N":
            return "A exclusão foi cancelada com sucesso!"
        elif confirmacao == "S":
            senha = input("Digite a senha da conta a ser excluída: ").strip()

            if senha == usuario[2]:
                conn = self.conexao.conectar()
                if conn is None:
                    print("Erro ao conectar ao Oracle.")

                cursor = conn.cursor()
                sql = """delete from usuarios_soulup where username = :username"""

                try:
                    cursor.execute(sql, username=username)
                    conn.commit()
                    print("A conta foi excluída com sucesso!")
                except oracledb.Error as erro:
                    conn.rollback()
                    return f"Erro ao alterar: {erro}"
                finally:
                    cursor.close()
                    conn.close()

            else:
                print("Senha incorreta. Não foi possível excluir o usuário.")
        else:
            print("A exclusão foi cancelada com sucesso!")

    def validar_login(self, email, senha):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
        
        cursor = conn.cursor()
        sql = """
            select id_usuario, username, senha, email, pontos, passagens, vales, saldo, limite from usuarios_soulup
            where email = :email and senha = :senha
            """

        try:
            cursor.execute(sql, {
                "email": email,
                "senha": senha
            })
            usuario_validado = cursor.fetchone()

            usuario = Usuario(usuario_validado[1], usuario_validado[2], usuario_validado[3], usuario_validado[4], usuario_validado[5], 
                              usuario_validado[6], usuario_validado[7], usuario_validado[8], usuario_validado[0])

            return usuario

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
        
        finally:
            cursor.close()
            conn.close()     

