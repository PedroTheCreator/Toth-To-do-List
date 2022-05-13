import os
from colorama import Fore, init, Style
from func import iris
import sqlite3
from sqlite3 import Error, IntegrityError
from getpass import getpass
import platform


if(platform.system() == 'Linux'):
    apagar = "clear"
    dormir = 'sleep 2'
elif(platform.system() == "Windows"):
    apagar = 'cls'
    dormir = 'timeout 2'

init(autoreset=True)

def limpar_tela():
  os.system(dormir + " 1") # Dá um delay antes de continuar;
  os.system(apagar) # Limpa o console.

def con(path):
    try:
        con=sqlite3.connect(path)   
        #print("Filé")
    except Error as er:
        print("Houve um erro ao conectar o banco de dados\n{}".format(er))
    return con




caminho = ".\\banco\\todo.db"
conexao=con(caminho)


def sql_create(con, sql):
    try:
        cursor=con.cursor()
        cursor.execute(sql)
        return True
    except Error as er:
        print(er)
        
def insert(con,sql):
    try:
        cursor=con.cursor()
        cursor.execute(sql)
        con.commit()
        return True
    except sqlite3.IntegrityError:
        print("Nome de usuário já está em uso, tente novamente.")
        
def select(con,sql):
    cursor=con.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


tabela_geral="""CREATE TABLE IF NOT EXISTS todo_usuarios(    
    ID       INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    nickname VARCHAR UNIQUE,
    senha    VARCHAR
);"""
sql_create(conexao,tabela_geral)
nome =0
while(nome != 3):
    seta = iris("--->",True,True)
    nome = int(input("======= Toth ======\n1 {} Entrar\n2 {} Registrar\n3 {} Sair\nInsira: ".format(seta,seta,seta)))
    if(nome == 1):
        os.system(apagar)
        nickname=str(input("======= Toth ======\nInsira seu nome de usuário: ")).lower()
        senha=getpass("Insira sua senha: ")
        usuarios = select(conexao,("SELECT * FROM todo_usuarios WHERE nickname LIKE '"+nickname+"'"))
        if(len(usuarios) > 0 and senha == usuarios[0][2]):
            print("Bem vindo, {}!".format(nickname))
            conectado=True
            nome=3
        else:
            print("Ops, falha na autenticação.")
            input("Pressione ENTER para continuar")
            os.system(apagar)
            nome=1
    elif(nome == 2):
        os.system(apagar)
        nickname=str(input("======= Toth ======\nInsira seu nome de usuário: ")).lower()
        senha=getpass("Insira sua senha: ")
        senha2=getpass("Insira novamente sua senha: ")

        tabela_usuario= """CREATE TABLE IF NOT EXISTS {} (
            nota_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            nota_texto VARCHAR
        );""".format(nickname+"_usuario")
        if(senha != senha2):
            print("As senhas divergem")
        else:
            criar_sql = "INSERT INTO todo_usuarios (nickname,senha) VALUES ('"+nickname+"','"+senha+"')"
            if(insert(conexao, criar_sql)):
                if(sql_create(conexao, tabela_usuario)):
                    print("Perfil criado com sucesso")
                    nome = 3
                    conectado = True
    elif(nome == 3):
        conectado = False
        print("Até a próxima")
    else:
        print("Opção Inválida")

if(conectado):
    menu = 0
    while(menu != 5):
        menu = int(input(("=====  Notas de {} =====\n1 {} Ver itens\n2 {} Inserir item\n3 {} Concluir item\n4 {} Apagar todos os itens da lista\n5 {} Sair\nInsira: ").format(nickname.title(),seta,seta,seta,seta,seta)))
        usuario_consulta = nickname+"_usuario"
        if(menu == 1):
            resultado = select(conexao,"SELECT * FROM '"+usuario_consulta+"'")
            if(len(resultado) == 0):
                print("Você ainda não tem itens")
            else:
                for i in resultado:
                    print("{}. {}".format(int(i[0]),i[1]))
                print("Você tem {} itens".format(len(resultado)))
            input("Pressione ENTER para continuar")
            os.system(apagar)
        if(menu == 2):
            resultado = select(conexao,"SELECT * FROM '"+usuario_consulta+"'")
            nota = str(input("Insira sua nota: "))
            for i in range(len(resultado)):
                insert(conexao,"UPDATE '"+usuario_consulta+"' SET nota_id='"+str(i+1)+"'WHERE nota_texto='"+resultado[i][1]+"'")
            id_nota = len(resultado)+1
            
            if(insert(conexao,"INSERT INTO '"+usuario_consulta+"' (nota_id, nota_texto) VALUES ('"+str(id_nota)+"','"+nota+"') ")):
                print("Nota inserida com sucesso!")
            else:
                print("Ocorreu um erro ao inserir a nota")
            os.system(dormir+" && "+apagar)
        if(menu == 3):
            resultado = select(conexao,"SELECT * FROM '"+usuario_consulta+"'")
            if(len(resultado) == 0):
                print("Você ainda não tem itens para concluir")
            else:
                for i in resultado:
                    print("{}. {}".format(int(i[0]),i[1]))
                print("Você tem {} itens".format(len(resultado)))
                deletar = (input("Insira o ID da nota que deseja apagar: "))
                if(insert(conexao,"DELETE FROM '"+usuario_consulta+"' WHERE nota_id='"+deletar+"'")):
                    print("O item foi removido")
                    resultado = select(conexao,"SELECT * FROM '"+usuario_consulta+"'")
                    for i in range(len(resultado)):
                        insert(conexao,"UPDATE '"+usuario_consulta+"' SET nota_id='"+str(i+1)+"'WHERE nota_texto='"+resultado[i][1]+"'")
                else:
                    print("Houve um erro ao apagar o item, tente novamente.")
            os.system(dormir+" &&"+apagar)
        if(menu == 4):
            confirmacao = input("Digite APAGAR para confirmar a ação\nInsira: ")
            if(confirmacao.lower() == "apagar"):
                if(insert(conexao,"DELETE FROM '"+usuario_consulta+"'")):
                        print("Todos os itens foram removidos")
            else:
                print("Seus dados estão a salvo")
                input("Pressione ENTER para continuar")
                os.system(apagar)
        if(menu == 5):
            print("Até a próxima")

conexao.close()
