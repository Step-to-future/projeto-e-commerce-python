import os
from security import *
import time
import re
from TextUtils import *

class Product:
    def __init__(self, code: int, name: str, description: str, buying_price: float, selling_price: float):
        # Definindo os atributos da instância
        self.code = code
        self.name = name
        self.description = description
        self.buying_price = buying_price
        self.selling_price = selling_price

    def __str__(self):
        return f"Código: {self.code}; Nome do produto: {self.name}; Descrição: {self.description}; Preço de compra: {self.buying_price}; Preço de venda: {self.selling_price}\n"
        
class Order:
    def __init__(self, order_id: int, product_id: int, product_ammount: int, order_price: float, order_date: str):
        self.order_id = order_id
        self.product_id = product_id
        self.product_ammount = product_ammount
        self.order_price = order_price
        self.order_date = order_date

    def __str__(self):
        return f"ID do pedido: {self.order_id}; ID do produto: {self.product_id}; Preço: {self.order_price:.2f}; Data: {self.order_date}\n"

# Create product

def create_new_product():
    file = open("./data/products.txt", "a+", encoding="UTF-8")
    file.readlines()  # Read existing lines (optional)
    file.seek(0)

    # Track the last used product code
    last_product_code = 0
    try:
        # Read the last used code from the file (if it exists)
        with open("./data/products.txt", "r", encoding="UTF-8") as f:
            last_line = f.readlines()[-1]  # Read the last line
            if last_line:
                last_product_code = int(last_line.strip().split(";")[0].split(":")[1])
    except FileNotFoundError:
        pass  # Ignore if file doesn't exist

    product_name = input("Digite o nome do produto: ")
    information = input("Descreva-o: ")
    buy_price = float(input("Digite o preco de compra: "))
    sell_price = float(input("Digite o preco de venda: "))

    product = Product(code=last_product_code + 1, name=product_name, description=information, buying_price=buy_price, selling_price=sell_price)

    if not product in file:
        file.write(str(product))
        file.flush()
        file.close()

    else:
        print("@@@ Erro: Informação inconsistente ou produto já cadastrado. Tente novamente... @@@")
        input("Pressione ENTER para voltar ao menu...")
        os.system('cls')  # Clear screen
        main()
    os.system('cls')  # Clear screen
    main()

# Update product
def update_product():
    # Abrir o arquivo para leitura e pegar todos os produtos
    try:
        with open("./data/products.txt", "r", encoding="UTF-8") as file:
            lines = file.readlines()  # Ler todas as linhas do arquivo
    except FileNotFoundError:
        print("Erro: Arquivo de produtos não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    # Pedir o código do produto a ser atualizado
    os.system('cls')
    drawBox(1, 1, 120, 25)
    gotoxy(3, 3)
    product_code = int(input("Digite o código do produto que deseja atualizar: "))

    # Variável para armazenar se o produto foi encontrado ou não
    produto_encontrado = False

    # Novo conteúdo para ser escrito no arquivo
    novo_conteudo = []

    # Percorrer todas as linhas do arquivo
    for line in lines:
        # Quebrar a linha para obter os dados do produto
        product_data = line.strip().split(";")
        codigo_atual = int(product_data[0].split(":")[1])

        # Verificar se o código atual é o código do produto a ser atualizado
        if codigo_atual == product_code:
            produto_encontrado = True  # Produto foi encontrado

            # Exibir os dados atuais do produto, um atributo por linha
            gotoxy(3, 4)
            print("Produto encontrado:")
            gotoxy(3, 5); print(f"Código: {codigo_atual}")
            gotoxy(3, 6); print(f"Nome: {product_data[1].split(':')[1]}")
            gotoxy(3, 7); print(f"Descrição: {product_data[2].split(':')[1]}")
            gotoxy(3, 8); print(f"Preço de compra: {product_data[3].split(':')[1]}")
            gotoxy(3, 9); print(f"Preço de venda: {product_data[4].split(':')[1]}")
            gotoxy(3, 10); print("Deixe o campo vazio se não quiser alterar um atributo.")

            # Pegar os novos valores ou manter os antigos
            gotoxy(3, 11)
            novo_nome = input(f"Nome atual ({product_data[1].split(':')[1]}): ") or product_data[1].split(":")[1]
            gotoxy(3, 12)
            nova_descricao = input(f"Descrição atual ({product_data[2].split(':')[1]}): ") or product_data[2].split(":")[1]
            gotoxy(3, 13)
            novo_preco_compra = input(f"Preço de compra atual ({product_data[3].split(':')[1]}): ") or product_data[3].split(":")[1]
            gotoxy(3, 14)
            novo_preco_venda = input(f"Preço de venda atual ({product_data[4].split(':')[1]}): ") or product_data[4].split(":")[1]

            # Recriar a linha com os dados atualizados
            linha_atualizada = (f"Código: {codigo_atual}; Nome do produto: {novo_nome}; "
                                f"Descrição: {nova_descricao}; Preço de compra: {novo_preco_compra}; "
                                f"Preço de venda: {novo_preco_venda}\n")

            # Adicionar a linha atualizada ao novo conteúdo
            novo_conteudo.append(linha_atualizada)
        else:
            # Manter as linhas não modificadas
            novo_conteudo.append(line)

    # Se o produto foi encontrado, reescrever o arquivo com os novos dados
    if produto_encontrado:
        with open("./data/products.txt", "w", encoding="UTF-8") as file:
            file.writelines(novo_conteudo)  # Reescreve o arquivo com os dados atualizados
        gotoxy(3, 15)
        print("Produto atualizado com sucesso!")
    else:
        gotoxy(3, 16)
        print(f"Produto com o código {product_code} não foi encontrado.")

    gotoxy(3, 17)
    input("Pressione ENTER para voltar ao menu...")
    os.system('cls')  # Limpar a tela
    main()


def delete_product():
    pass

def cancel_order():
    pass

def make_purchase():

    try:
        # Abrindo o arquivo de produtos
        with open("./data/products.txt", "r", encoding="UTF-8") as file:
            products = []  # Lista de produtos

            # Lendo os produtos do arquivo e criando objetos Product
            for line in file:
                product_data = line.strip().split(";")  # Split line on semicolon (';')
                if len(product_data) == 5:  # Verifica se há 5 campos no produto
                    product = Product(
                        code=int(product_data[0].split(":")[1]),
                        name=product_data[1].split(":")[1],
                        description=product_data[2].split(":")[1],
                        buying_price=float(product_data[3].split(":")[1]),
                        selling_price=float(product_data[4].split(":")[1]),
                    )
                    products.append(product) 

    except FileNotFoundError:
        print("Erro: Arquivo de produtos não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    # Exibindo os produtos cadastrados
    print("\nProdutos cadastrados:")
    for product in products:
        print(f"Produto: {product.name}\nDescrição: {product.description}\nCódigo: {product.code}\nPreço de compra: R$ {product.buying_price}\nPreço de venda: R$ {product.selling_price}\n{'='*80}")

    # Cart and total value
    product_order = []
    total_value = 0.0


    order = input("Digite o código do produto desejado (ou '0' para voltar ao menu): ")
    pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'

    if order == '0':  # Checkout if zero
        os.system('cls')
        main()
    
    try:
        # Convert to int the order code
        order_code = int(order)
        product_ammount = int(input("Digite a quantidade: "))
        order_date = input("Digite a data da compra no formato dd/mm/aaaa: ")
        
        # Search for the product by code
        selected_product = next((product for product in products if product.code == order_code), None)

        pattern_true = re.match(pattern, order_date)
        
        if selected_product:
            if not pattern_true:
                print("@@@@ Data inválida... @@@@")
            else:
                product_order.append(selected_product)
                total_value += selected_product.selling_price * product_ammount
                print(f"Produto: '{selected_product.name} ' adicionado ao carrinho. Preço: R$ {(selected_product.selling_price * product_ammount):.2f} ({selected_product.selling_price} por unidade)")
        else:
            print("Código de produto inválido. Tente novamente.")
    
    except ValueError:
        print("Código inválido! Digite um número.")

    # Checkout
    if product_order:
        print("\nCompra finalizada!")
        print("Itens no carrinho:")
        for product in product_order:
            print(f"- {product.name}: R$ {product.selling_price:.2f}")
        
        print(f"Total: R$ {total_value:.2f}")
    else:
        print("\nNenhum produto foi adicionado ao carrinho.")

    input("\nPressione Enter para voltar ao menu principal...")
    os.system('cls')  # Clear the screen
    main()

# Show products list
def show_all_products():
    file = open("./data/products.txt", "r", encoding="UTF-8")

    if not file:
        print("Nenhum produto encontrado...")
    else:
        print("\nProdutos cadastrados:")
        for line in file:
            # Create a Product object from each line
            product_data = line.strip().split(";")  # Split line on semicolon (';')
            product = Product(
                code=int(product_data[0].split(":")[1]),
                name=product_data[1].split(":")[1],
                description=product_data[2].split(":")[1],
                buying_price=float(product_data[3].split(":")[1]),
                selling_price=float(product_data[4].split(":")[1]),
            )

            # Print product details using the Product object
            print(f"Produto: {product.name}\nDescrição: {product.description}\nCódigo: {product.code}\nPreço de compra: R$ {product.buying_price}\nPreço de venda: R$ {product.selling_price}\n{'='*80}")

    file.close()  # Close the file after processing
    input("\nPressione ENTER para continuar...")
    os.system('cls')  # Clear the screen
    main()

def main():
    menu = f"MENU"
    menu1 = '1. Cadastrar produto'
    menu2 = '2. Exibir produtos'
    menu3 = '3. Nova Compra'
    menu4 = '4. Cancelar compra'
    menu5 = '5. Editar produto'
    menu6 = '6. Apagar produto'
    menu7 = '7. Sair'

    while True:
        os.system('cls') # Clear the screen
        
        drawRoundBorderBox(1, 1, 60, 20, GREEN)

        gotoxy(26, 1); printGreen(menu, end="")
        gotoxy(5, 3); printGreen(menu1, end="")
        gotoxy(5, 5); printGreen(menu2, end="")
        gotoxy(5, 7); printGreen(menu3, end="")
        gotoxy(5, 9); printGreen(menu4, end="")
        gotoxy(5, 11); printGreen(menu5, end="")
        gotoxy(5, 13); printGreen(menu6, end="")
        gotoxy(5, 15); printGreen(menu7, end="")
        gotoxy(5, 18); option = input("Digite o número da opção: ")


        if option == "1":
            os.system('cls')
            print(f"{'='*10}Cadastro de produto{'='*10}")
            create_new_product()
        elif option == "2":
            os.system('cls')
            show_all_products()
        elif option == "3":
            os.system('cls')
            make_purchase()
        elif option == "4":
            # cancel_order()
            gotoxy(5, 9)
            printRed("### Esta opção está em fase de desenvolvimento... ###", end="")
            gotoxy(5, 10)
            input("Pressione ENTER para voltar ao menu...")
            os.system('cls')
            main()
        elif option == "5":
            update_product()
        elif option == "6":
            # delete_product()
            gotoxy(5, 13)
            printRed("### Esta opção está em fase de desenvolvimento... ###", end="")
            gotoxy(5, 14)
            input("Pressione ENTER para voltar ao menu...")
            os.system('cls')
            main()
            pass
        elif option == "7":
            os.system('cls')
            drawBox(1, 1, 30, 7)
            gotoxy(10, 4)
            print("Saindo...")
            time.sleep(1)
            os.system('cls')
            drawBox(1, 1, 30, 7)
            gotoxy(10, 4)
            print("Até logo!")
            time.sleep(1)
            os.system('cls')
            quit()
        elif option == "":
            os.system('cls')
            drawBox(1, 1, 60, 7)
            gotoxy(10, 4)
            print("@@@ O campo não pode ficar vazio @@@")
            time.sleep(1)
            os.system('cls')
            main()
        else:
            os.system('cls')
            drawBox(1, 1, 60, 7)
            gotoxy(15, 4)
            print("@@@ Digite uma opção válida @@@")
            time.sleep(1)
            main()
        break

# Authenticate user
authenticate()
main()