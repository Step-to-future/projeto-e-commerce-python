import os
import time
from TextUtils import *
count = 0
# Chave de autenticação

autentication_key = "0000"


def authenticate():
    for count in range(1,4):
        os.system("cls")
        gotoxy(1, 1)
        drawBox(1, 1, 120, 5, YELLOW)
        gotoxy(40, 3)
        printColored("Voce tem 3 tentativas de login", GREEN, end="")
        drawBox(1, 6, 120, 8, LIGHT_GRAY)
        gotoxy(4, 8)
        printColored(f"Tentativa numero {count}", YELLOW, end="")
        gotoxy(4, 10)
        key = input("Digite a chave de autenticação: ")
        if key == autentication_key: 
                os.system('cls')
                drawBox(1, 1, 50, 7, GREEN)
                gotoxy(6, 4)
                print("#### Acesso liberado, entrando... ####")
                time.sleep(1)
                os.system('cls')
                gotoxy(6, 10)
                return True
        elif count == 3:
                os.system('cls')
                drawBox(1, 1, 50, 7, RED)
                gotoxy(3, 4)
                printColored("Número máximo de tentativas excedido.", RED, end="")
                gotoxy(3, 10)
                exit()
        elif key != autentication_key:
                gotoxy(2, 9)
                printColored("Chave inválida!", YELLOW, end="\n")
                printColored("tente novamente", YELLOW, end="")
                time.sleep(1)
                os.system("cls")
        else:
            break
