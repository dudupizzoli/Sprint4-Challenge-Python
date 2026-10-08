from conexaoOracle.conexaodb import Conexaodb
from models.usuario import Usuario
from dao.usuario_dao import UsuarioDAO

user_dao = UsuarioDAO()

def validar_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        else:
            print("O campo não pode ficar em branco.")
            
usuario_atual = None
login = False
opcao_login = -1

while not login:
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
                if len(senha) < 4 or " " in senha:
                    raise ValueError("Sua senha precisa ter ao menos 4 caracteres e nenhum espaço.")
                if "@" not in email or len(email) < 8:
                    raise ValueError("O email precisa ter @ e não pode ter menos de 8 caracteres.")
                novo_usuario = Usuario(username, senha, email)
                user_dao.cadastrar_usuario(novo_usuario)

                usuario_atual = novo_usuario
                print("Agora você está logado com: ", usuario_atual._username)     
                login = True          
            except ValueError as erro:
                print("Ocorreu um erro: ", erro)

        case 2:
                try:
                    email = validar_texto("Digite seu email: ")
                    senha = validar_texto("Sua senha precisa conter ao menos 4 caracteres e não pode ter espaços. Digite sua senha: ")
                    if len(senha) < 4 or " " in senha:
                        raise ValueError("Sua senha precisa ter ao menos 4 caracteres e nenhum espaço.")
                    if "@" not in email or len(email) < 8:
                        raise ValueError("O email precisa ter @ e não pode ter menos de 8 caracteres.")
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

        case 0:
            print("Encerrando sistema...")
            break
        
        case _:
            print("Opção inválida. Digite uma opção válida do menu.")


opcao = -1
opcao_geral = -1
opcao_bu = -1
opcao_posts = -1
opca_user = -1

while opcao != 0:
    print("\n===== Menu SoulUp Society =====")
    print("1 - Geral.") #Submenu geral
    print("2 - Carregar o bilhete único.") #Submenu do bilhete único
    print("3 - Postar.") #Submenu de postagens
    print("4 - Usuário.") #Submenu do usuário
    print("5 - Criar JSON.")
    print("6 - Criar HTML.")
    print("0 - Sair.") #Saída do sistema
    try:
        opcao = int(input("Digite o número da opção que você deseja: "))
    except ValueError:
        print("Opção inválida. Digite apenas números.")
        continue
    match opcao:

        case 1:
            print("EM PROCESSO DE DESENVOLVIMENTO")

        case 2:
            print("EM PROCESSO DE DESENVOLVIMENTO")

        case 3:
            print("EM PROCESSO DE DESENVOLVIMENTO")

        case 4:
            while True:    #Submenu do sistema - trata sobre as contas do usuário | Aqui se encontra um CRUD
                print("\n======= Menu SoulUp Society - Usuário =======")
                print("1 - Cadastrar nova conta.") #Create
                print("2 - Ver contas cadastradas.") #Read
                print("3 - Procurar conta pelo nome de usuário.")
                print("4 - Editar nome de usuário.") #Update
                print("5 - Remover conta.") #Delete
                print("6 - Voltar.") #Voltar ao menu principal
                try:
                    opcao_user = int(input("Digite o número da opção que você deseja: "))
                except ValueError:
                    print("Opção inválida. Digite apenas números.")
                    continue
                match opcao_user:
                    case 1:
                        try:
                            username = validar_texto("Digite seu nome de usuário: ")
                            email = validar_texto("Digite seu email: ")
                            senha = validar_texto("Sua senha precisa conter ao menos 4 caracteres e não pode ter espaços. Digite sua senha: ")
                            if len(senha) < 4 or " " in senha:
                                raise ValueError("Sua senha precisa ter ao menos 4 caracteres e nenhum espaço.")
                            if "@" not in email or len(email) < 8:
                                raise ValueError("O email precisa ter @ e não pode ter menos de 8 caracteres.")
                            novo_usuario = Usuario(username, senha, email)
                            user_dao.cadastrar_usuario(novo_usuario)
                        except ValueError as erro:
                            print("Ocorreu um erro: ", erro)

                    case 2:
                        usuarios = user_dao.listar_usuarios()
                        if len(usuarios) == 0:
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

                    case 3:
                        print("")

                    case 4:
                        print("")
                    
                    case 5:
                        print("")

                    case 6:
                        print("Voltando ao menu anterior...")
                        break
                    
                    case _:
                        print("Opção inválida. Digite uma opção válida do menu.")

        case 5:
            print("EM PROCESSO DE DESENVOLVIMENTO")

        case 6:
            print("EM PROCESSO DE DESENVOLVIMENTO")

        case 0:
            print("Encerrando sistema...")
            break
        
        case _:
            print("Opção inválida. Digite uma opção válida do menu.")
    