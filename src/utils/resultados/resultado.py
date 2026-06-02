import time

class Resultado:
    def __init__(self):
        self.sucesso = False
        self.custo = 0
        self.passos = 0
        self.expandidos = 0
        self.fronteira = 0
        self.tempo = 0
        
        self.inicio = 0
        self.fim = 0
    
    def addCusto(self, increment = 1):
        self.custo += increment
    
    def addPassos(self, increment = 1):
        self.passos += increment
    
    def addExpandidos(self, increment = 1):
        self.expandidos += increment
    
    def addfronteira(self, increment = 1):
        self.fronteira += increment

    def start(self):
        self.inicio = time.perf_counter()
    
    def finish(self):
        self.fim = time.perf_counter()
        self.tempo = self.fim - self.inicio
