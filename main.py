from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO
from dao.postagem_dao import PostagemDAO
import json
from pathlib import Path
import webbrowser
from html import escape
import sys

user_dao = UsuarioDAO()
post_dao = PostagemDAO()

def validar_texto(mensagem): #Função para ler texto
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        else:
            print("O campo não pode ficar em branco.")


def ler_inteiro(mensagem): #Função para ler números inteiros
    while True:
        try:
            valor = int(input(mensagem))
            if valor <= 0:
                raise ValueError("O número não pode ser menor ou igual a 0.")
            else:
                return valor
        except ValueError as erro:
            print("Ocorreu um erro: ", erro, ". Digite apenas números válidos.")

def validar_credenciais(email, senha): #Função para validar email e senha colocados pelo usuário
    if len(senha) < 4 or " " in senha:
        raise ValueError("Sua senha precisa ter ao menos 4 caracteres e nenhum espaço.")
    if "@" not in email or len(email) < 8:
        raise ValueError("O email precisa ter @ e não pode ter menos de 8 caracteres.")


def conversao_dinheiro(pontos):  #Função responsável por converter pontos em dinheiro, tanto para a simulação quanto para o bilhete único em si
    #Recebe como parâmetro a quantidade de pontos inserida pelo usuário, verifica sua validade, e então retorna o valor em dinheiro
    if pontos > 0:
        valor_convertido = pontos * 0.0096
        return valor_convertido
    else:
        print("Não é possível converter 0 ou números negativos")

def conversao_passagem(passagens):  #Função responsável por converter pontos em passagens para o bilhete único
    #Recebe como parâmetro a quantidade de passagens que o usuário deseja adquirir com seus pontos
    if passagens > 0:
        pontos_necessarios = passagens * 580
        return pontos_necessarios
    else:
        print("Não é possível converter 0 ou números negativos")

def conversao_vales(vales):  #Função responsável por converter pontos em desconto para passagens no bilhete único
    #Recebe como parâmetro a quantidade de vales de desconto que o usuário deseja adquirir com seus pontos
    if vales > 0:
        pontos_necessarios = vales * 113
        return pontos_necessarios
    else:
        print("Não é possível converter 0 ou números negativos")

def exportar_json(): #Função para gerar o relatório de usuários em JSON
    try:
        usuarios = user_dao.listar_usuarios()
        if usuarios is None:
            raise OSError("Nenhum usuário foi encontrado para a exportação.")
        else:
            lista_usuarios = []
            for usuario in usuarios:
                dados_usuario = {
                    "id_usuario": usuario[0],
                    "username": usuario[1],
                    "email": usuario[3],
                    "quantidade_pontos": usuario[4],
                    "quantidade_passagens": usuario[5],
                    "quantidade_vales": usuario[6],
                    "saldo": usuario[7],
                    "limite": usuario[8]
                    }
                lista_usuarios.append(dados_usuario)
            with open("usuarios_soulup_society.json","w",encoding="utf-8") as arquivo:
                json.dump(lista_usuarios, arquivo, ensure_ascii=False, indent=4)
            print("\nO arquivo 'usuarios_soulup_society.json' foi gerado com sucesso!")
            print(f"Foram exportados {len(lista_usuarios)} usuários.")

    except OSError as erro:
                    print("Ocorreu um erro durante a criação do arquivo: ", erro)
                    
def exportar_html(): #Função para gerar o relatório de usuários em HTML
    try:
        usuarios = user_dao.listar_usuarios() or []
        num_usuarios = 0
        usuarios_encontrados = ""

        for usuario in usuarios:
            id_usuario = usuario[0]
            username = escape(str(usuario[1]))
            email = escape(str(usuario[3]))
            quantidade_pontos = usuario[4]
            quantidade_passagens = usuario[5]
            quantidade_vales = usuario[6]
            saldo = usuario[7]
            limite = usuario[8]
            missoes = user_dao.listar_missoes(id_usuario) or []
            if missoes:
                missoes_html = "".join(f"<p>{escape(str(m))}</p>" for m in missoes[:3])
            else: 
                missoes_html = "<p>Este usuário não possui missões.</p>"
                    
            num_usuarios += 1
            usuarios_encontrados += f"""
            <div class="card__usuario">
                <h2>Nome de usuário: {username}</h2>
                <p>Id do usuário: {id_usuario}</p>
                <p>Email: {email}</p>
                <div class="carteira">
                    <h3>Carteira</h3>
                    <p>Quantidade de pontos: {quantidade_pontos}</p>
                    <p>Quantidade de passagens: {quantidade_passagens}</p>
                    <p>Quantidade de vales: {quantidade_vales}</p>
                    <p>Saldo: R${saldo:.2f}</p>
                    <p>Limite de passagens: {limite}/10</p>
                </div>
                <div>
                    <h3>Missões</h3>
                    {missoes_html}
                </div>
            </div>                      
            """
        if num_usuarios == 0:
            usuarios_encontrados = """
            <h2 class="sem__usuarios">Nenhum usuário encontrado.</h2>
            """

        html = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Usuários | SoulUp Society</title>
            <style>
                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}

                body {{
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    background: #f5f7fa;
                    color: #2d3748;
                    font-family: Arial, Helvetica, sans-serif;
                    line-height: 1.6;
                }}

                header {{
                    background: #2b3544;
                    color: #e2e8f0;
                    text-align: center;
                    padding: 32px 16px;
                }}

                header h1 {{
                    color: #ffffff;
                    margin-bottom: 12px;
                }}

                header p {{
                    max-width: 640px;
                    margin: 0 auto 8px;
                }}

                main {{
                    flex: 1;
                    width: 100%;
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 24px 16px 40px;
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    align-items: flex-start;
                    gap: 24px;
                }}

                .sem__usuarios {{
                    margin: auto;
                    text-align: center;
                    color: #718096;
                    font-size: 1.3rem;
                    font-weight: normal;
                }}

                .card__usuario {{
                    background: #ffffff;
                    border: 1px solid #e2e8f0;
                    border-radius: 10px;
                    padding: 20px;
                    flex: 0 1 calc(50% - 12px); /* 2 por linha, descontando metade do gap */
                    margin-top: 0;
                    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
                }}

                .card__usuario h2 {{
                    font-size: 1.2rem;
                    color: #4c51bf;
                    margin-bottom: 8px;
                }}

                .card__usuario h3 {{
                    font-size: 1rem;
                    margin-bottom: 6px;
                }}

                .card__usuario > div {{
                    margin-top: 16px;
                    padding: 12px 16px;
                    background: #f7fafc;
                    border-radius: 8px;
                }}

                .carteira {{
                    border-left: 4px solid #48bb78;
                }}

                .card__usuario > div:not(.carteira) {{
                    border-left: 4px solid #667eea;
                }}

                .rodape {{
                    text-align: center;
                    padding: 16px;
                    font-size: 0.85rem;
                    color: #cbd5e0;
                    background: #2b3544;
                }}

                @media (max-width: 700px) {{
                    .card__usuario {{
                    flex-basis: 100%;
                }}
            }}
            </style>
        </head>
        <body>
            <header>

                <h1>SoulUp Society - Usuários</h1>
                <p>Abaixo você poderá conferir cards com os dados de todos os usuários cadastrados até o momento na SoulUp Society!</p>
                <p>Atualmente existem {num_usuarios} usuários cadastrados!</p>
            
            </header>
            <main>
                {usuarios_encontrados}

            </main>
            <footer class="rodape">
                <p>Todos os direitos reservados - SoulUp Society - &copy; - 2026</p>
            </footer>
        </body>
        </html>
        """

        with open("usuarios_soulup_society.html", "w",encoding="utf-8") as arquivo:
            arquivo.write(html)

        arquivo_html = Path("usuarios_soulup_society.html").resolve()
        endereco = arquivo_html.as_uri()
        webbrowser.open(endereco)
        print("\nO arquivo 'usuarios_soulup_society.html' foi gerado com sucesso!")
        print("Abrindo a página no navegador...")

    except OSError as erro:
        print("Ocorreu um erro durante a criação do arquivo: ", erro)

usuario_atual = None
login = False
opcao_login = -1

while not login: #Menu de login, permite a criação de uma conta e o login caso o usuário já possua uma conta
    print("\n=======================================")
    print("Bem-vindo à SoulUp Society!!")
    print("Ainda não possui uma conta? Cadastre-se!")
    print("1 - Realizar cadastro.")
    print("Já possui uma conta? Faça o login!")
    print("2 - Login.")
    print("3 - Sair.")
    try:
        opcao_login = int(input("Digite o número da opção que você deseja: "))
    except ValueError:
        print("Opção inválida. Digite apenas números.")
        continue
    match opcao_login:
        case 1:
            try:
                username = validar_texto("Digite seu nome de usuário: ")
                email = validar_texto("Digite seu email: ")
                senha = validar_texto("Sua senha precisa conter ao menos 4 caracteres e não pode ter espaços. Digite sua senha: ")
                validar_credenciais(email, senha)
                novo_usuario = Usuario(username, senha, email)
                Usuario.definir_missoes(novo_usuario)

                if user_dao.cadastrar_usuario(novo_usuario):
                    user_dao.adicionar_missoes(novo_usuario._id_usuario, novo_usuario._missoes)

                    usuario_atual = user_dao.validar_login(email, senha)
                    if usuario_atual is not None:
                        print("Agora você está logado com: ", usuario_atual._username)     
                        login = True  
            except ValueError as erro:
                print("Ocorreu um erro: ", erro)

        case 2:
                try:
                    email = validar_texto("Digite seu email: ")
                    senha = validar_texto("Sua senha precisa conter ao menos 4 caracteres e não pode ter espaços. Digite sua senha: ")
                    validar_credenciais(email, senha)
                    usuario_validado = user_dao.validar_login(email, senha)

                    if usuario_validado is None:
                        raise ValueError("Email ou senha incorretos.")        
                    else: 
                        usuario_atual = usuario_validado
                        login = True
                        print("O login foi efetuado com sucesso!")
                        print("Agora você está logado com: ", usuario_atual._username)  

                except ValueError as erro:
                    print("Ocorreu um erro: ", erro)

        case 3:
            print("Encerrando sistema...")
            sys.exit()
        
        case _:
            print("Opção inválida. Digite uma opção válida do menu.")

opcao = -1

while opcao != 0:
    print("\n===== Menu SoulUp Society =====")
    print("1 - Geral.") #Submenu geral
    print("2 - Carregar o bilhete único.") #Submenu do bilhete único
    print("3 - Postar.") #Submenu de postagens
    print("4 - Usuário.") #Submenu do usuário
    print("5 - Criar JSON.") #Opção para criar um relatório de usuários em JSON
    print("6 - Criar HTML.") #Opção para criar um relatório de usuários em HTML
    print("0 - Sair.") #Saída do sistema
    try:
        opcao = int(input("Digite o número da opção que você deseja: "))
    except ValueError:
        print("Opção inválida. Digite apenas números.")
        continue
    match opcao:

        case 1: #Submenu do sistema - trata sobre opções gerais
            while True:
                print("\n======= Menu SoulUp Society - Geral =======")
                print("1 - Conferir missões.") 
                print("2 - Ver relatório do bilhete único.") 
                print("3 - Simular conversão de pontos em dinheiro.")
                print("4 - Conferir limite de pontos transformados em passagens.")
                print("5 - Voltar.")
                try:
                    opcao_geral = int(input("Digite o número da opção que você deseja: "))
                except ValueError:
                    print("Opção inválida. Digite apenas números.")
                    continue

                match opcao_geral:
                    case 1:
                        missoes_usuario_atual = user_dao.listar_missoes(usuario_atual._id_usuario)
                        if missoes_usuario_atual is None:
                            print("Você não possui nenhuma missão")
                        else:
                            for missao in missoes_usuario_atual:
                                print(missao)
                
                    case 2:
                        usuario_atual.relatorio_bu()
                        
                    case 3:
                        try:
                            simular_pontos = ler_inteiro("Insira a quantidade de pontos para fazer a simulação de uma conversão: ")
                            pontos_simulados = conversao_dinheiro(simular_pontos)
                            print(f"{simular_pontos} pontos são iguais a R$ {pontos_simulados:.2f}.")
                        except ValueError:
                            print("Ocorreu um erro. Digite apenas números.")

                    case 4:
                        print(f"Seu limite atual é de {usuario_atual._limite}/10 passagens.")
 
                    case 5:
                        print("Voltando ao menu anterior...")
                        break

                    case _:
                        print("Opção inválida. Digite uma opção válida do menu.")

        case 2:
            while True: #Submenu do sistema - trata sobre as funções voltadas ao bilhete único
                print("\n======= Menu SoulUp Society - Bilhete Único =======") 
                print("1 - Ver quantidade de pontos.")
                print("2 - Converter pontos em dinheiro para o bilhete único.") 
                print("3 - Conferir o saldo do bilhete único.") 
                print("4 - Converter pontos em passagens do bilhete único (1 passagem = 580 pontos).") 
                print("5 - Conferir a quantidade de passagens no bilhete único.") 
                print("6 - Converter pontos em vales de desconto para a passagem (cada vale garante '20%' de desconto. Esta função apenas ficará disponível após atingir o limite de compra de passagens).")
                print("7 - Conferir a quantidade de vales de desconto.")
                print("8 - Voltar.")
                try:
                    opcao_bu = int(input("Digite o número da opção que você deseja: "))
                except ValueError:
                    print("Opção inválida. Digite apenas números.")
                    continue
                match opcao_bu:

                    case 1:
                        print(f"Você possui um total de {usuario_atual._pontos} pontos atualmente.")

                    case 2:
                        pontos_para_conversao = ler_inteiro("Insira a quantidade de pontos que você deseja converter em dinheiro para o bilhete único: ")
                        if pontos_para_conversao > usuario_atual._pontos:
                            print("Não foi possível realizar a conversão pois o valor de pontos inserido foi maior do que a quantidade que a conta possui.")
                        else:
                            usuario_atual._pontos -= pontos_para_conversao
                            saldo_ganho = conversao_dinheiro(pontos_para_conversao)
                            usuario_atual._saldo = round(usuario_atual._saldo + saldo_ganho, 2)
                            user_dao.atualizar_qtd_pontos(usuario_atual._id_usuario, usuario_atual._pontos)
                            user_dao.atualizar_saldo(usuario_atual._id_usuario, usuario_atual._saldo)
                            print(f"Você converteu {pontos_para_conversao} pontos em R$ {saldo_ganho:.2f} com sucesso!")

                    case 3:
                        print(f"Atualmente, o saldo de seu bilhete é de R$ {usuario_atual._saldo:.2f}.")

                    case 4:
                        passagens_desejadas = ler_inteiro("Insira a quantidade de passagens que você deseja adquirir para o bilhete único: ")
                        custo_em_pontos = conversao_passagem(passagens_desejadas)
                        if passagens_desejadas > usuario_atual._limite or usuario_atual._pontos < custo_em_pontos:
                            print("Não foi possível realizar a conversão. Confira seu limite ou sua quantidade de pontos.")
                        else: 
                            usuario_atual._pontos -= custo_em_pontos
                            usuario_atual._passagens += passagens_desejadas
                            usuario_atual._limite -= passagens_desejadas
                            user_dao.atualizar_qtd_pontos(usuario_atual._id_usuario, usuario_atual._pontos)
                            user_dao.atualizar_passagens(usuario_atual._id_usuario, usuario_atual._passagens)
                            user_dao.atualizar_limite(usuario_atual._id_usuario, usuario_atual._limite)
                            print(f"Você converteu {custo_em_pontos} pontos em {passagens_desejadas} passagens com sucesso!")

                    case 5:
                        print(f"Atualmente, você possui {usuario_atual._passagens} passagem(ns) no bilhete único.")

                    case 6:
                        if usuario_atual._limite != 0:
                            print("Não foi possível prosseguir pois seu limite de passagens ainda não chegou a 0.")
                        else:
                            vales_desejados = ler_inteiro("Insira a quantidade de vales que você deseja adquirir para o bilhete único: ") 
                            custo_em_pontos = conversao_vales(vales_desejados)
                            if usuario_atual._pontos < custo_em_pontos:
                                print("Não foi possível realizar a conversão. Confira sua quantidade de pontos.") 
                            else:
                                usuario_atual._pontos -= custo_em_pontos
                                usuario_atual._vales += vales_desejados
                                user_dao.atualizar_qtd_pontos(usuario_atual._id_usuario, usuario_atual._pontos)
                                user_dao.atualizar_vales(usuario_atual._id_usuario, usuario_atual._vales)
                                print(f"Você converteu {custo_em_pontos} pontos em {vales_desejados} vales com sucesso!")

                    case 7:
                        print(f"Atualmente você possui {usuario_atual._vales} vale(s) no bilhete único.")

                    case 8:
                        print("Voltando ao menu anterior...")
                        break

                    case _:
                        print("Opção inválida. Digite uma opção válida do menu.")


        case 3:
            while True:  #Submenu do sistema - trata sobre as postagens do usuário | Aqui se encontra um CRUD
                print("\n======= Menu SoulUp Society - Postagens =======") 
                print("1 - Escrever nova postagem.") #Create   
                print("2 - Ver minhas postagens.") #Read
                print("3 - Procurar postagem pelo ID.") #Read    
                print("4 - Editar uma postagem.") #Update  
                print("5 - Excluir uma postagem.") #Delete
                print("6 - Voltar.") 
                try:
                    opcao_post = int(input("Digite o número da opção que você deseja: "))
                except ValueError:
                    print("Opção inválida. Digite apenas números.")
                    continue

                match opcao_post:
                    case 1: 
                        try: 
                            texto_postagem = validar_texto("O que deseja escrever? ")
                            if len(texto_postagem) > 350:
                                raise ValueError("A postagem não pode conter mais do que 350 caracteres.")

                            post_dao.fazer_postagem(usuario_atual._id_usuario, texto_postagem)

                        except ValueError as erro:
                            print("Ocorreu um erro: ", erro)     

                    case 2:
                        postagens = post_dao.listar_postagens(usuario_atual._id_usuario)
                        if postagens is None:
                            print("Esta conta não possui nenhuma postagem.")  
                        else:
                            for post in postagens:
                                print("\n========================")
                                print("ID da postagem: ", post[0])
                                print("ID do usuário: ", post[1])
                                print("Post: ", post[2]) 

                    case 3:
                        postagem_procurada = ler_inteiro("Digite o ID da postagem que você deseja buscar: ")
                        postagem = post_dao.buscar_id_postagem(postagem_procurada)
                        if postagem is None:
                            print("Nenhuma postagem foi encontrada.")
                        else:
                            print("\n========================")
                            print("ID da postagem: ", postagem[0])
                            print("ID do usuário: ", postagem[1])
                            print("Post: ", postagem[2])      

                    case 4:
                        postagem_editada = ler_inteiro("Digite o ID da postagem que você deseja editar: ")
                        postagem_encontrada = post_dao.buscar_id_postagem(postagem_editada)
                        if postagem_encontrada is None:
                            print("Nenhuma postagem foi encontrada.")

                        elif postagem_encontrada[1] != usuario_atual._id_usuario:
                            print("Não é possível editar as postagens de outros usuários.")

                        else:
                            postagem = post_dao.editar_postagem(postagem_editada)
                            if postagem is not None:
                                print("\n========================")
                                print("ID da postagem: ", postagem[0])
                                print("ID do usuário: ", postagem[1])
                                print("Post: ", postagem[2])    

                    case 5:
                        postagem_excluida = ler_inteiro("Digite o ID da postagem que você deseja excluir: ")
                        postagem = post_dao.buscar_id_postagem(postagem_excluida)
                        if postagem is None:
                            print("Nenhuma postagem foi encontrada.")

                        elif postagem[1] != usuario_atual._id_usuario:
                            print("Não é possível excluir as postagens de outros usuários.")

                        else:
                            print("\n========================")
                            print("ID da postagem: ", postagem[0])
                            print("ID do usuário: ", postagem[1])
                            print("Post: ", postagem[2])  

                            post_dao.excluir_postagem(postagem_excluida)                               

                    case 6:
                        print("Voltando ao menu anterior...")
                        break

                    case _:
                        print("Opção inválida. Digite uma opção válida do menu.")


        case 4:
            while True:    #Submenu do sistema - trata sobre as contas do usuário | Aqui se encontra um CRUD
                print("\n======= Menu SoulUp Society - Usuário =======")
                print("1 - Conferir conta atual.") #Confere a conta logada atualmente
                print("2 - Logar em outra conta.") #Faz o login em outra conta
                print("3 - Cadastrar nova conta.") #Create
                print("4 - Ver contas cadastradas.") #Read
                print("5 - Procurar conta pelo nome de usuário.")#Read
                print("6 - Editar nome de usuário e email.") #Update
                print("7 - Remover conta.") #Delete
                print("8 - Voltar.") #Voltar ao menu principal
                try:
                    opcao_user = int(input("Digite o número da opção que você deseja: "))
                except ValueError:
                    print("Opção inválida. Digite apenas números.")
                    continue
                match opcao_user:
                    case 1:
                        print("\n=== Conta Logada Atualmente ===")
                        print(usuario_atual)

                    case 2:
                            try:
                                email = validar_texto("Digite seu email: ")
                                senha = validar_texto("Sua senha precisa conter ao menos 4 caracteres e não pode ter espaços. Digite sua senha: ")
                                validar_credenciais(email, senha)

                                usuario_validado = user_dao.validar_login(email, senha)

                                if usuario_validado is None:
                                    raise ValueError("Email ou senha incorretos.")        
                                else: 
                                    usuario_atual = usuario_validado
                                    print("O login foi efetuado com sucesso!")
                                    print("Agora você está logado com: ", usuario_atual._username)  

                            except ValueError as erro:
                                print("Ocorreu um erro: ", erro)
                    

                    case 3:
                        try:
                            username = validar_texto("Digite seu nome de usuário: ")
                            email = validar_texto("Digite seu email: ")
                            senha = validar_texto("Sua senha precisa conter ao menos 4 caracteres e não pode ter espaços. Digite sua senha: ")
                            validar_credenciais(email, senha)

                            novo_usuario = Usuario(username, senha, email)
                            Usuario.definir_missoes(novo_usuario)
                            if user_dao.cadastrar_usuario(novo_usuario):
                                user_dao.adicionar_missoes(novo_usuario._id_usuario, novo_usuario._missoes)
                        except ValueError as erro:
                            print("Ocorreu um erro: ", erro)

                    case 4:
                        usuarios = user_dao.listar_usuarios()
                        if usuarios is None:
                            print("Nenhum usuário cadastrado.")
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

                    case 5:
                        username_procurado = validar_texto("Digite o Username da conta que você deseja buscar: ")
                        usuario = user_dao.buscar_nome_usuario(username_procurado)
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

                    case 6:
                        usuario_editado = validar_texto("Digite o nome do usuário que você deseja editar: ")
                        usuario = user_dao.editar_usuario(usuario_editado)
                        if usuario is None:
                            print("Não foi possível editar o usuário.")
                        else:
                            if usuario[0] == usuario_atual._id_usuario:
                                usuario_atual._username = usuario[1]
                                usuario_atual._email_user = usuario[3]

                            print("\n========================")
                            print("ID do usuário: ", usuario[0])
                            print("Username: ", usuario[1])
                            print("Email: ", usuario[3])
                            print("Qntd. de pontos: ", usuario[4])
                            print("Qntd. de passagens: ", usuario[5])
                            print("Qntd. de vales: ", usuario[6])
                            print("Saldo: ", usuario[7])
                            print("Limite: ", usuario[8])        

                    case 7:
                        usuario_excluido = validar_texto("Digite o nome do usuário que você deseja excluir: ")
                        usuario = user_dao.buscar_nome_usuario(usuario_excluido)
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

                            conta_excluida = user_dao.excluir_usuario(usuario_excluido)
                            if conta_excluida and usuario[0] == usuario_atual._id_usuario:
                                print("Sua conta foi excluída. Encerrando sistema...")
                                opcao = 0
                                break                      

                    case 8:
                        print("Voltando ao menu anterior...")
                        break
                    
                    case _:
                        print("Opção inválida. Digite uma opção válida do menu.")


        case 5:
            print("\nEsta opção irá gerar um relatório .json sobre os usuários já cadastrados na SoulUp Society.")
            print("Gerando relatório...")
            exportar_json()
            

        case 6:
            print("\nEsta opção irá gerar um relatório .html sobre os usuários já cadastrados na SoulUp Society.")
            print("Gerando relatório...")
            exportar_html()


        case 0:
            print("Encerrando sistema...")
            break
        
        case _:
            print("Opção inválida. Digite uma opção válida do menu.")
    