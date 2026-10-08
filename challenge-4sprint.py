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
                senha = validar_texto("Sua senha precisa conter ao menos 4 caracteres e não pode ter espaços. Digite sua senha: ")
                email = validar_texto("Digite seu email: ")
                if len(senha) < 4 or " " in senha:
                    raise ValueError("Sua senha precisa ter ao menos 4 caracteres e nenhum espaço.")
                if "@" not in email or len(email) < 8:
                    raise ValueError("O email precisa ter @ e não pode ter menos de 8 caracteres.")
                novo_usuario = Usuario(username, senha, email)
                user_dao.cadastrar_usuario(novo_usuario)               
            except ValueError as erro:
                print("Ocorreu um erro: ", erro)


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
    