from conexaoOracle.conexaodb import Conexaodb
from models.usuario import Usuario
import oracledb

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

        username = usuario._username
        senha = usuario._senha_user
        email = usuario._email_user

        cursor = conn.cursor()
        sql = """insert into usuarios_soulup (username, senha, email) 
        values (:username, :senha, :email)"""

        try:
            cursor.execute(sql,
                           username = username,
                           senha = senha,
                           email = email)
            conn.commit()

            cursor.execute("select id_usuario from usuarios_soulup where email = :email", email = email)
            linha = cursor.fetchone()
            if linha is not None:
                usuario._id_usuario = linha[0]

            print("Cadastro realizado com sucesso!")

        except oracledb.Error as erro:
            conn.rollback()
            print("\nHouve um erro: ", erro)
    
        finally:
            cursor.close()
            conn.close() 

    def listar_usuarios(self):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

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
                
        finally:
            cursor.close()
            conn.close()            

    def buscar_nome_usuario(self, username):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False
        
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

    def editar_usuario(self, nome_usuario):    
        usuario = self.buscar_nome_usuario(nome_usuario)

        if usuario is None:
            return None

        else:

            senha = input("Digite a senha da conta a ser editada: ").strip()

            if senha == usuario[2]:

                username = input(f"Seu nome de usuário atual é: {usuario[1]}, caso não queira mudá-lo, aperte enter. Digite seu novo nome de usuário: ").strip()
                email = input(f"Seu email atual é: {usuario[3]}, caso não queira mudá-lo, aperte enter. Digite seu novo email: ").strip()

                if username == '':
                    username = usuario[1]
                
                if email == '':
                    email = usuario[3]

                if "@" not in email or len(email) < 8:
                    print("O email precisa ter @ e não pode ter menos de 8 caracteres.")
                    return False

                conn = self.conexao.conectar()
                if conn is None:
                    print("Erro ao conectar ao Oracle.")
                    return False

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

                    return self.buscar_nome_usuario(username)
                except oracledb.Error as erro:
                    conn.rollback()
                    print("Houve um erro: ", erro)
                finally:
                    cursor.close()
                    conn.close()

            else:
                print("Senha incorreta. Não foi possível editar o usuário.")
                return False

    def excluir_usuario(self, username):
        usuario = self.buscar_nome_usuario(username)
        if usuario is None:
            print("Nenhum usuário foi encontrado.")
            return False
        
        confirmacao = input("A exclusão de uma conta é uma ação perigosa e potencialmente irreversível. Você realmente deseja excluir esta conta? (S para Sim/N para Não)").upper().strip()
        if confirmacao == "N":
            print("A exclusão foi cancelada com sucesso!")
            return False
        
        elif confirmacao == "S":
            senha = input("Digite a senha da conta a ser excluída: ").strip()

            if senha == usuario[2]:
                conn = self.conexao.conectar()
                if conn is None:
                    print("Erro ao conectar ao Oracle.")
                    return False

                cursor = conn.cursor()
                sql = """delete from usuarios_soulup where username = :username"""
                sql_missoes = """delete from missoes_usuario where id_usuario = :id_usuario"""
                sql_postagens = """delete from posts_soulup where id_usuario = :id_usuario"""

                try:
                    cursor.execute(sql_missoes, id_usuario=usuario[0])
                    cursor.execute(sql_postagens, id_usuario=usuario[0])
                    cursor.execute(sql, username=username)
                    conn.commit()
                    print("A conta foi excluída com sucesso!")
                    return True
                except oracledb.Error as erro:
                    conn.rollback()
                    print("Houve um erro: ", erro)
                finally:
                    cursor.close()
                    conn.close()

            else:
                print("Senha incorreta. Não foi possível excluir o usuário.")
                return False
        else:
            print("Digite apenas S ou N.")
            return False

    def validar_login(self, email, senha):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False
        
        cursor = conn.cursor()
        sql = """
            select id_usuario, username, senha, email, pontos, passagens, saldo, vales, limite from usuarios_soulup
            where email = :email and senha = :senha
            """

        try:
            cursor.execute(sql, {"email": email, "senha": senha})
            usuario_validado = cursor.fetchone()

            usuario = Usuario(username=usuario_validado[1], senha_user=usuario_validado[2], email_user=usuario_validado[3], pontos=usuario_validado[4],
                              passagens=usuario_validado[5], saldo=usuario_validado[6], vales=usuario_validado[7], limite=usuario_validado[8], id_usuario=usuario_validado[0])

            return usuario

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
            return None
        
        finally:
            cursor.close()
            conn.close()     

    def adicionar_missoes(self, id_usuario, missoes):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        cursor = conn.cursor()

        sql = """
            insert into missoes_usuario (id_usuario, missao)
            values (:id_usuario, :missao)
        """

        try:
            for missao in missoes:
                cursor.execute(sql, id_usuario=id_usuario, missao=missao)

            conn.commit()
            return "Missões adicionadas com sucesso."

        except oracledb.Error as erro:
            conn.rollback()
            print("Houve um erro: ", erro)
        
        finally:
            cursor.close()
            conn.close() 


    def listar_missoes(self, id_usuario):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        cursor = conn.cursor()

        sql = """
            select missao
            from missoes_usuario
            where id_usuario = :id_usuario
            order by id_missao
        """

        try:
            cursor.execute(sql, id_usuario=id_usuario)

            missoes = [linha[0] for linha in cursor.fetchall()]

            if len(missoes) == 0:
                return None
            else:
                return missoes

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
        
        finally:
            cursor.close()
            conn.close() 

    def atualizar_qtd_pontos(self, id_usuario, nova_qtd_pontos):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False
        
        cursor = conn.cursor()
        
        sql = """
            update usuarios_soulup 
            set pontos = :nova_qtd_pontos 
            where id_usuario = :id_usuario 
            """

        try:
            cursor.execute(sql, nova_qtd_pontos=nova_qtd_pontos, id_usuario=id_usuario)
            conn.commit()

        except oracledb.Error as erro:
            conn.rollback()
            print("Houve um erro: ", erro)
        
        finally:
            cursor.close()
            conn.close() 

    def atualizar_saldo(self, id_usuario, novo_saldo):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False
        
        cursor = conn.cursor()
        
        sql = """
            update usuarios_soulup 
            set saldo = :novo_saldo 
            where id_usuario = :id_usuario 
            """

        try:
            cursor.execute(sql, novo_saldo=novo_saldo, id_usuario=id_usuario)
            conn.commit()

        except oracledb.Error as erro:
            conn.rollback()
            print("Houve um erro: ", erro)
        
        finally:
            cursor.close()
            conn.close() 
    
    def atualizar_passagens(self, id_usuario, novas_passagens):
        conn = self.conexao.conectar()
        if conn is None:
               print("Erro ao conectar ao Oracle.")
               return False
        
        cursor = conn.cursor()
        
        sql = """
            update usuarios_soulup 
            set passagens = :novas_passagens 
            where id_usuario = :id_usuario 
            """

        try:
            cursor.execute(sql, novas_passagens=novas_passagens, id_usuario=id_usuario)
            conn.commit()

        except oracledb.Error as erro:
            conn.rollback()
            print("Houve um erro: ", erro)
        
        finally:
            cursor.close()
            conn.close() 
    
    def atualizar_vales(self, id_usuario, novos_vales):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False
        
        cursor = conn.cursor()
        
        sql = """
            update usuarios_soulup 
            set vales = :novos_vales 
            where id_usuario = :id_usuario 
            """

        try:
            cursor.execute(sql, novos_vales=novos_vales, id_usuario=id_usuario)
            conn.commit()

        except oracledb.Error as erro:
            conn.rollback()
            print("Houve um erro: ", erro)
        
        finally:
            cursor.close()
            conn.close() 

    def atualizar_limite(self, id_usuario, novo_limite):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        cursor = conn.cursor()

        sql = """
            update usuarios_soulup
            set limite = :novo_limite
            where id_usuario = :id_usuario
            """

        try:
            cursor.execute(sql, novo_limite=novo_limite, id_usuario=id_usuario)
            conn.commit()

        except oracledb.Error as erro:
            conn.rollback()
            print("Houve um erro: ", erro)

        finally:
            cursor.close()
            conn.close()