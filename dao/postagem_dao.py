from conexaoOracle.conexaodb import Conexaodb
import oracledb

class PostagemDAO:
    def __init__(self):
        self.conexao = Conexaodb(
            usuario="user",
            senha="senha",
            host="host",
            porta=1521,
            service_name="ORCL"
        )

    def fazer_postagem(self, id_usuario, postagem):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return False

        cursor = conn.cursor()
        sql = """insert into posts_soulup (id_usuario, texto) 
        values (:id_usuario, :texto)"""

        try:
            cursor.execute(sql,
                           id_usuario = id_usuario,
                           texto = postagem)
            conn.commit()
            print("Post publicado com sucesso!")

        except oracledb.Error as erro:
            conn.rollback()
            print("\nHouve um erro: ", erro)
    
        finally:
            cursor.close()
            conn.close() 

    def listar_postagens(self, id_usuario):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return None

        cursor = conn.cursor()

        sql = """
            select id_post, id_usuario, texto
            from posts_soulup
            where id_usuario = :id_usuario
            order by id_post
        """

        try:
            cursor.execute(sql, id_usuario=id_usuario)
            postagens = cursor.fetchall()

            if len(postagens) == 0:
                return None
            else:
                return postagens

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
        
        finally:
            cursor.close()
            conn.close() 

    def buscar_id_postagem(self, id_postagem):
        conn = self.conexao.conectar()
        if conn is None:
            print("Erro ao conectar ao Oracle.")
            return None
        
        cursor = conn.cursor()
        sql = """select id_post, id_usuario, texto from posts_soulup where id_post = :id_post"""

        try:
            cursor.execute(sql, id_post = id_postagem)
            postagem = cursor.fetchone()
            if postagem is None:
                return None
            else:
                return postagem              

        except oracledb.Error as erro:
            print("Houve um erro: ", erro)
                        
        finally:
            cursor.close()
            conn.close()

    def editar_postagem(self, id_postagem):    
        postagem = self.buscar_id_postagem(id_postagem)

        if postagem is None:
            return None

        else:

            texto = input("Digite o novo texto da postagem: ").strip()
            if texto == "":
                print("A postagem não pode ficar vazia.")
                return None
            if len(texto) > 350:
                print("A postagem não pode conter mais do que 350 caracteres.")
                return None
            
            conn = self.conexao.conectar()
            if conn is None:
                print("Erro ao conectar ao Oracle.")
                return None

            cursor = conn.cursor()
            sql = """update posts_soulup 
                    set texto = :texto 
                    where id_post = :id_post 
                    """

            try:
                cursor.execute(sql, texto=texto, id_post=id_postagem)
                conn.commit()
                print("Postagem editada com sucesso!")

                return self.buscar_id_postagem(id_postagem)
            
            except oracledb.Error as erro:
                conn.rollback()
                print("Houve um erro: ", erro)
            finally:
                cursor.close()
                conn.close()

    def excluir_postagem(self, id_postagem):
        postagem = self.buscar_id_postagem(id_postagem)

        if postagem is None:
            return None

        else:

            confirmacao = input("Você realmente deseja excluir esta postagem? (S para Sim/N para Não): ").upper().strip()
            if confirmacao == "N":
                print("A exclusão foi cancelada com sucesso!")
                return False
            elif confirmacao == "S":

                conn = self.conexao.conectar()
                if conn is None:
                    print("Erro ao conectar ao Oracle.")
                    return False

                cursor = conn.cursor()
                sql = """delete from posts_soulup where id_post = :id_post"""

                try:
                    cursor.execute(sql, id_post=id_postagem)
                    conn.commit()
                    print("A postagem foi excluída com sucesso!")
                except oracledb.Error as erro:
                    conn.rollback()
                    print("Houve um erro: ", erro)
                finally:
                    cursor.close()
                    conn.close()

            else:
                print("Digite apenas S ou N.")