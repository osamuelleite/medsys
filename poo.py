#Essa é a Classe Carro, um modelo de projeto de carro

from mailbox import NotEmptyError


class carro:
    def __init__(self, marca, modelo, cor, ano):
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.ano = ano
        self.velocidade = 0

    def acelerar(self, valor):
        self.velocidade += valor
        print(f"O {self.marca, self.modelo} acelerou para {self.velocidade} km/h.")

    def frear(self):
        self.velocidade = 0
        print(f"O {self.marca, self.modelo} freiou e parou.")

# Criando meu objeto e instanciando a classe Carro.
meu_carro = carro("Toyota", "Corolla", "vermelho", "2022")
carro_vizinho = carro("Fiat", "uno", "azul", "2003")

#acessando atributos e chamando os métodos

print(f"meu carro é um {meu_carro.marca}, com modelo {meu_carro.modelo} e ano {meu_carro.ano}, com a cor {meu_carro.cor}. ")
meu_carro.acelerar(50)
carro_vizinho.acelerar(60)
print(f"meu carro vizinho é um {carro_vizinho.marca}, com modelo {carro_vizinho.modelo} e ano {carro_vizinho.ano}, com a cor {carro_vizinho.cor}. ")

#-----------------------------------

class Eletronico:
    def __init__(self, tipo, fabricante, modelo, preco):
        self.tipo = tipo
        self.fabricante = fabricante
        self.modelo = modelo
        self.preco = preco

    def ligar(self):
        print(f" O aparelho {self.tipo} do fabricante {self.fabricante} foi ligado")    

    def desligar(self):
        print(f" O aparelho {self.tipo} do fabricante {self.fabricante} foi desligado")    
    
    def especificacoes(self):
        print(f"O aparelho {self.tipo} do fabricante {self.fabricante} tem o modelo {self.modelo} está custando {self.preco:.2f} reais")

celular = Eletronico("Smartphone", "Samsung", "Galaxy S23", 1500)
celular.ligar()
celular.desligar()
celular.especificacoes()
print("-" * 50)

maquina_lavar = Eletronico("Maquina de Lavar", "LG", "Modelo 1200", 1500)
maquina_lavar.ligar()
maquina_lavar.desligar()
maquina_lavar.especificacoes()
print("-" * 50)

drone = Eletronico("Drone", "DJI", "Modelo Mavic 3", 1500)
drone.ligar()
drone.desligar()
drone.especificacoes()
print("-" * 50)

#-----------------------------------
class ContaBancaria:
    def __init__(self, titular, saldo_inicial):
        self.titular = titular
        self.__saldo = saldo_inicial

    def sacar(self, valor):
        if valor<=0:
            print("valorde saque inválido.")

        elif valor > self.__saldo:
            print (f"saldo insuficiente! Saldo atual: R$ {self.__saldo:.2f}")
        else:
            self.__saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado. Seu novo saldo é {self.__saldo:.2f}")

    def meu_saldo_atual(self):
        return self.__saldo

minhaConta = ContaBancaria("Samuel", 1000)
minhaConta.sacar(500)
print(f"Meu saldo atual é: R$ {minhaConta.meu_saldo_atual():.2f}")


#-----------------------------------------------------------


#Desafio de projeto: Mídia Streaming

from abc import ABC, abstractmethod

class Midia(ABC):
    def __init__(self, nome):
        self._nome = nome
        self.__likes = 0
        print(f"A Mídia {self._nome} foi criada com sucesso.")

    def dar_likes(self):
        self.__likes += 1
        print(f"O like foi adicionado na mídia {self._nome}. Total de Likes: {self.__likes}")

    def get_likes(self):
        return self.__likes

    @abstractmethod
    def play(self):
        pass

class Filme(Midia):
    def __init__(self, nome, duracao_minutos):
        super().__init__(nome)
        self.duracao_minutos = duracao_minutos

    def play(self):
        print(f"O filme {self._nome} está sendo reproduzido. Duracao: {self.duracao_minutos} minutos")

class Serie(Midia):
    def __init__(self, nome, numero_temporadas):
        super().__init__(nome)
        self.numero_temporadas = numero_temporadas
    def play(self):
        print(f"A serie {self._nome} está sendo reproduzida. Numero de temporadas: {self.numero_temporadas}")


Prison_Break = Serie("Prison Break", 10)
Woman_scent = Filme("Woman_scent", 120)

print("-" * 30)

minha_playlist = [Prison_Break, Woman_scent]

def processar_playlist(minha_playlist):
    for midia in minha_playlist:
        midia.play()
        midia.dar_likes()
        print("+" * 30) 

processar_playlist(minha_playlist)
        
print(midia.get_likes())


