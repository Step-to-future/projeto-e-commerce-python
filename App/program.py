import os
import security
import time

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
            print("opção 3")
            # novaCompra()
        elif option == 4:
            os.system('cls')
            print("Saindo...")
            time.sleep(2)
            os.system('cls')
            print("Até logo!")
            quit()
        else:
            os.system('cls')
            print("@@@ Digite uma opção válida @@@")
        break

# Authenticate user
security.authenticate()
main()