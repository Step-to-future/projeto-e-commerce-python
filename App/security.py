import os
import time
count = 0
# Chave de autenticação

autentication_key = "0000"


def authenticate():
    for count in range(1,4):
        print("Voce tem 3 tentativas de login")
        print(f"Tentativa numero {count}")
        key = input("Digite a chave de autenticação: ")
        if key == autentication_key: 
                print("Acesso liberado!")
                time.sleep(1)
                print("Entrando no sistema...")
                time.sleep(1)
                print("[20%]")
                time.sleep(1)
                print("[60%]")
                time.sleep(1)
                print("[100%]")
                time.sleep(1)
                os.system("cls")
                return True

        elif count == 3:
                print("Voce errou as 3 tentativas. Acabaram suas chances")
                exit()
        elif key != autentication_key:
                print("Chave inválida!")
                print("tente novamente")
                os.system("cls")
        else:
            break

