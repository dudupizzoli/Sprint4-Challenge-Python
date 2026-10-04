from conexaoOracle.conexaodb import Conexaodb
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
            return "Erro ao conectar ao Oracle."

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
            return "Erro ao conectar ao Oracle." 

        cursor = conn.cursor()
        sql = """select * from usuarios_soulup order by id_usuario"""

        try:
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            if len(usuarios) == 0:
                print("Nenhum usuário foi cadastrado.")
            else:
                for usuario in usuarios:
                    print("\n========================")
                    print("ID do usuário: ", usuario[0])
                    print("Username: ", usuario[1])
                    print("Email: ", usuario[3])
                    print("Qntd. de pontos: ", usuario[4])
                    print("Qntd. de passagens: ", usuario[5])
                    print("Qntd. de vales: ", usuario[6])
                    print("Saldo: ", usuario[7])
                    print("Limite: ", usuario[8])

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
            usuarios = []
                
        finally:
            cursor.close()
            conn.close()            

    def buscar_id_usuario(self, id_usuario):
        conn = self.conexao.conectar()
        if conn is None:
            return "Erro ao conectar ao Oracle." 
        
        cursor = conn.cursor()
        sql = """select * from usuarios_soulup where id_usuario = :id_usuario"""

        try:
            cursor.execute(sql, id_usuario = id_usuario)
            usuario = cursor.fetchone()
            if usuario is None:
                print("Nenhum usuário foi encontrado.")
            else:
                print("\n========================")
                print("ID do usuário: ", usuario[0])
                print("Username: ", usuario[1])
                print("Email: ", usuario[3])
                print("Qntd. de pontos: ", usuario[4])
                print("Qntd. de passagens: ", usuario[5])
                print("Qntd. de vales: ", usuario[6])
                print("Saldo: ", usuario[7])
                print("Limite: ", usuario[8])        

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
                        
        finally:
            cursor.close()
            conn.close()

    def editar_usuario(self):    
        conn = self.conexao.conectar()
        if conn is None:
            return "Erro ao conectar ao Oracle." 

        id_usuario = int(input("Digite o ID do usuário que você deseja editar: "))
        if id_usuario < 0:
            return "O ID precisa ser um número positivo. Digite um ID válido."

        cursor = conn.cursor()
        sql = """select * from usuarios_soulup where id_usuario = :id_usuario"""

        try:
            cursor.execute(sql, id_usuario=id_usuario)
            usuario = cursor.fetchone()

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
        
        finally:
            cursor.close()
            conn.close() 

        if usuario is None:
            return "Nenhum usuário foi encontrado."

        senha = input("Digite a senha da conta a ser editada: ").strip()

        if senha == usuario[2]:
            conn = self.conexao.conectar()
            if conn is None:
                return "Erro ao conectar ao Oracle."

            username = input(f"Seu nome de usuário atual é: {usuario[1]}, caso não queira mudá-lo, apenas digite seu nome de usuário atual novamente. Digite seu novo nome de usuário: ").strip()
            email = input(f"Seu email atual é: {usuario[3]}, caso não queira mudá-lo, apenas digite seu email atual novamente. Digite seu novo email: ").strip()

            if username == '' or email == '':
                return "Não foi possível realizar nenhuma alteração pois nenhum texto foi inserido em um ou mais campos."

            cursor = conn.cursor()
            sql = """update usuarios_soulup 
                    set username = :username, 
                        email = :email 
                    where id_usuario = :id_usuario 
                    """

            try:
                cursor.execute(sql, username=username, email=email, id_usuario=id_usuario)
                conn.commit()
            except oracledb.Error as erro:
                conn.rollback()
                return f"Erro ao alterar: {erro}"
            finally:
                cursor.close()
                conn.close()

        else:
            print("Senha incorreta. Não foi possível editar o usuário.")

    def excluir_usuario(self):
        conn = self.conexao.conectar()
        if conn is None:
            return "Erro ao conectar ao Oracle." 

        id_usuario = int(input("Digite o ID do usuário que você deseja excluir: "))
        if id_usuario < 0:
            return "O ID precisa ser um número positivo. Digite um ID válido."

        cursor = conn.cursor()
        sql = """select * from usuarios_soulup where id_usuario = :id_usuario"""

        try:
            cursor.execute(sql, id_usuario=id_usuario)
            usuario = cursor.fetchone()
            if usuario is None:
                return "Nenhum usuário foi encontrado."
            else:
                print("\n========================")
                print("ID do usuário: ", usuario[0])
                print("Nome de usuário: ", usuario[1])
                print("Email: ", usuario[3])
                print("Qntd. de pontos: ", usuario[4])
                print("Qntd. de passagens: ", usuario[5])
                print("Qntd. de vales: ", usuario[6])
                print("Saldo: ", usuario[7])
                print("Limite: ", usuario[8]) 

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
        
        finally:
            cursor.close()
            conn.close() 

        confirmacao = input("A exclusão de uma conta é uma ação perigosa e potencialmente irreversível. Você realmente deseja excluir esta conta? (S para Sim/N para Não)").upper().strip()
        if confirmacao == "S":
            senha = input("Digite a senha da conta a ser excluída: ").strip()

            if senha == usuario[2]:
                conn = self.conexao.conectar()
                if conn is None:
                    return "Erro ao conectar ao Oracle."

                cursor = conn.cursor()
                sql = """delete from usuarios_soulup where id_usuario = :id_usuario"""

                try:
                    cursor.execute(sql, id_usuario=id_usuario)
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

