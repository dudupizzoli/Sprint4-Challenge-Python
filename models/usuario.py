import random

class Usuario:
    #Construtor da classe Usuario
    #Pontos possuem um valor alto apenas para fins de teste. No sistema real  a conta começaria com 0 pontos
    def __init__(self, username, senha_user, email_user, pontos=15000, passagens=0, saldo=0, vales=0, limite=10, id_usuario=None, missoes=[]):
        self._id_usuario = id_usuario
        self._username = username
        self._senha_user = senha_user
        self._email_user = email_user
        self._pontos = pontos
        self._passagens = passagens
        self._vales = vales
        self._saldo = saldo
        self._limite = limite
        self._missoes = missoes
        

    #Método para exibir o objeto Usuario
    def __str__(self):
        return f"\nID: {self._id_usuario} | Username: {self._nome_usuario} | Email: {self._email_user} | \nPontos: {self._pontos} | Passagens: {self._passagens} | Saldo: {self._saldo} | Vales: {self._vales} | Limite: {self._limite}/10"

    def definir_missoes(self):
        missoes_possiveis = ["Missão: Faça 15 posts - Recompensa: 300 pontos.", "Missão: Entre em 3 comunidades - Recompensa: 150 pontos.", "Missão: Poste 5 fotos em diferentes linhas do metrô de São Paulo - Recompensa: Uma pelúcia do metrô de São Paulo.", "Missão: Faça 10 comentários - Recompensa: 150 pontos.", "Missão: Curta 25 posts - Recompensa: 125 pontos.", "Missão: Faça 5 posts - Recompensa: 100 pontos.", "Missão: Curta 5 posts - Recompensa: 50 pontos.", "Missão: Responda 8 comentários - Recompensa: 100 pontos."]
        for i in range(3):
            numero_missao = random.randint(0, 7)
            for missao in missoes_possiveis:
                if numero_missao == missoes_possiveis.index(missao):
                    self._missoes.append(missao)