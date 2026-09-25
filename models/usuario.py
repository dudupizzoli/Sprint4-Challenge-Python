class Usuario:
    #Construtor da classe Usuario
    #Pontos possuem um valor alto apenas para fins de teste. No sistema real  a conta começaria com 0 pontos
    def __init__(self, id_usuario=0, username='', senha_user='', email_user='', pontos=15000, passagens=0, saldo=0, vales=0, limite=10):
        self._id_usuario = id_usuario,
        self._username = username,
        self._senha_user = senha_user,
        self._email_user = email_user,
        self._pontos = pontos, 
        self._passagens = passagens,
        self._vales = vales,
        self._saldo = saldo,
        self._limite = limite,
        self._missoes = []
        

    #Método para exibir o objeto Usuario
    def __str__(self):
        return f"\nID: {self._id_usuario} | Username: {self._nome_usuario} | Email: {self._email_user} | \nPontos: {self._pontos} | Passagens: {self._passagens} | Saldo: {self._saldo} | Vales: {self._vales} | Limite: {self._limite}/10"