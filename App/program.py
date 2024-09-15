import os
import security
import time
import re

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
    sell_price = float(input("Digite o preco de compra: "))

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
                    products.append(product)  # Adiciona o produto à lista

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

    # Order loop
    while True:
        order = input("Digite o código do produto desejado (ou '0' para finalizar): ")
        pattern = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$'

        if order == '0':  # Checkout if zero
            break
        
        try:
            # Convert to int the order code
            order_code = int(order)
            product_ammount = int(input("Digite a quantidade: "))
            
            # Search for the product by code
            selected_product = next((product for product in products if product.code == order_code), None)
            
            if selected_product:
                product_order.append(selected_product)
                total_value += selected_product.selling_price * product_ammount
                print(f"Produto: {selected_product.name} adicionado ao carrinho. Preço: R$ {(selected_product.selling_price * product_ammount):.2f} ({selected_product.selling_price} por unidade)")
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
    menu = f"{'='*15}MENU{'='*15}\n1. Cadastrar produto\n2. Exibir produtos\n3. Nova Compra\n4. Sair\n{'='*34}"

    while True:
        print(menu)
        option = int(input("Digite o número da opção: "))

        if option == 1:
            os.system('cls')
            print(f"{'='*10}Cadastro de produto{'='*10}")
            create_new_product()
        elif option == 2:
            os.system('cls')
            show_all_products()
        elif option == 3:
            os.system('cls')
            make_purchase()
        elif option == 4:
            os.system('cls')
            print("Saindo...")
            time.sleep(1)
            os.system('cls')
            print("Até logo!")
            time.sleep(1)
            os.system('cls')
            quit()
        else:
            os.system('cls')
            print("@@@ Digite uma opção válida @@@")
        break

# Authenticate user
security.authenticate()
main()