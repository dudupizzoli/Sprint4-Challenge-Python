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


def ler_inteiro(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if valor <= 0:
                raise ValueError("O número não pode ser menor ou igual a 0.")
        except ValueError as erro:
            print("Ocorreu um erro: ", erro, ". Digite apenas números válidos.")

def conversao(pontos):  #Função responsável por converter pontos em dinheiro, tanto para a simulação quanto para o bilhete único em si
    #Recebe como parâmetro a quantidade de pontos inserida pelo usuário, verifica sua validade, e então retorna o valor em dinheiro
    if pontos > 0:
        valor_convertido = pontos * 0.0096
        return valor_convertido
    else:
        print("Não é possível converter 0 ou números negativos")

            
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
                Usuario.definir_missoes(novo_usuario)
                user_dao.cadastrar_usuario(novo_usuario)
                user_dao.adicionar_missoes(novo_usuario._id_usuario, novo_usuario._missoes)

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

        case 1: #Submenu do sistema - trata sobre opções gerais
            while True:
                print("\n======= Menu SoulUp Society - Geral =======")
                print("1 - Conferir missões.") 
                print("2 - Ver quantidade de pontos.") 
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
                        if missoes_usuario_atual == []:
                            print("Você não possui nenhuma missão")
                        else:
                            for missao in missoes_usuario_atual:
                                print(missao)
                
                    case 2:
                        print(f"Você possui um total de {usuario_atual._pontos} pontos.")
                        
                    case 3:
                        try:
                            simular_pontos = ler_inteiro("Insira a quantidade de pontos para fazer a simulação de uma conversão: ")
                            pontos_simulados = conversao(simular_pontos)
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
                print("1 - Converter pontos em dinheiro para o bilhete único.") 
                print("2 - Transferir o dinheiro para o bilhete único.") 
                print("3 - Conferir a carga do bilhete único.") 
                print("4 - Converter pontos em passagens do bilhete único (1 passagem = 580 pontos).") 
                print("5 - Transferir as passagens para o bilhete único.") 
                print("6 - Conferir a quantidade de passagens do bilhete único.") 
                print("7 - Converter pontos em vales de desconto para a passagem (cada vale garante '20%' de desconto. Esta função apenas ficará disponível após atingir o limite de compra de passagens).")
                print("8 - Transferir os vales de desconto para o bilhete único.") 
                print("9 - Conferir a quantidade de vales de desconto.")
                print("10 - Voltar.")
                try:
                    opcao_bu = int(input("Digite o número da opção que você deseja: "))
                except ValueError:
                    print("Opção inválida. Digite apenas números.")
                    continue
                #FAZER OS CASES


        case 3:
            print("EM PROCESSO DE DESENVOLVIMENTO")

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
                                if len(senha) < 4 or " " in senha:
                                    raise ValueError("Sua senha precisa ter ao menos 4 caracteres e nenhum espaço.")
                                if "@" not in email or len(email) < 8:
                                    raise ValueError("O email precisa ter @ e não pode ter menos de 8 caracteres.")
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

                            if len(senha) < 4 or " " in senha:
                                raise ValueError("Sua senha precisa ter ao menos 4 caracteres e nenhum espaço.")
                            if "@" not in email or len(email) < 8:
                                raise ValueError("O email precisa ter @ e não pode ter menos de 8 caracteres.")
                            
                            novo_usuario = Usuario(username, senha, email)
                            user_dao.cadastrar_usuario(novo_usuario)
                        except ValueError as erro:
                            print("Ocorreu um erro: ", erro)

                    case 4:
                        usuarios = user_dao.listar_usuarios()
                        if usuarios == None:
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
                        username_procurado = validar_texto("Digite o Username da conta que você deseja buscar.")
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

                            user_dao.excluir_usuario(usuario_excluido)                           

                    case 8:
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
    