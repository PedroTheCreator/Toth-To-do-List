import os
def iris(texto,balanceado=False,retornar=False):
  from colorama import Fore
  class Cores():
    def __init__(self,cor):
      self.cor = cor
    def mudar_cor(self):
      if self.cor == "RED":
        return(Fore.RED)
      elif self.cor == "YELLOW":
        return(Fore.YELLOW)
      elif self.cor == "LIGHTYELLOW_EX":
        return(Fore.LIGHTYELLOW_EX)
      elif self.cor == "GREEN":
        return(Fore.GREEN)
      elif self.cor == "LIGHTBLUE_EX":
        return(Fore.LIGHTBLUE_EX)
      elif self.cor == "BLUE":
        return(Fore.BLUE)
      elif self.cor == "MAGENTA":
        return Fore.MAGENTA
      elif self.cor == "CYAN":
        return Fore.CYAN
  tamanho = len(texto)
  tamanho = round((tamanho/7))
  lista_cores = ["RED", "YELLOW", "LIGHTYELLOW_EX","GREEN","LIGHTBLUE_EX","CYAN","BLUE","MAGENTA"]
  
  contador = 0
  resultado = ""
  if balanceado == False:
    for i in range(0,len(texto)):
      Iris = Cores(lista_cores[contador])
      resultado = resultado +  Iris.mudar_cor() + str(texto[i])
      contador +=1
      if contador == 8:
        contador = 0  
  else:
    temporaria = tamanho
    for i in range(0,len(texto)):
      Iris = Cores(lista_cores[contador])
      resultado = resultado +  Iris.mudar_cor() + str(texto[i])
      if i > temporaria:
        contador+=1
        temporaria += tamanho
  resultado = resultado + Fore.RESET
  #print(type(retornar))
  #print((retornar))
  if retornar:
    return(resultado)
  else:
    print(resultado)
  
