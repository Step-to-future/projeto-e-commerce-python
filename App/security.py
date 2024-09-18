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
        drawBox(1, 1, 45, 10, YELLOW)
        gotoxy(3, 3)
        printColored("Voce tem 3 tentativas de login", GREEN, end="")
        gotoxy(3, 5)
        printColored(f"Tentativa numero {count}", YELLOW, end="")
        gotoxy(3, 7)
        key = input("Digite a chave de autenticação: ")
        if key == autentication_key: 
                os.system('cls')
                gotoxy(3, 3)
                print("#### Acesso liberado, entrando... ####")
                time.sleep(1)
                os.system('cls')
                return True

        elif count == 3:
                gotoxy(3, 9)
                printColored("Número máximo de tentativas excedido.", RED, end="")
                exit()
        elif key != autentication_key:
                gotoxy(3, 9)
                printColored("Chave inválida!", YELLOW, end="\n")
                printColored("tente novamente", YELLOW, end="")
                os.system("cls")
        else:
            break

