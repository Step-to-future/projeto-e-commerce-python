import os
from security import *
import time
import re
from TextUtils import *
from datetime import datetime

class Product:
    def __init__(self, code, name, description, buying_price, selling_price):
        self.code = code
        self.name = name
        self.description = description
        self.buying_price = buying_price
        self.selling_price = selling_price
    
    def __str__(self):
        return f"Código: {self.code}; Nome: {self.name}; Descrição: {self.description}; Preço Compra: {self.buying_price}; Preço Venda: {self.selling_price}"

class Order:
    def __init__(self, order_id, product_id, product_amount, order_price, order_date):
        self.order_id = order_id
        self.product_id = product_id
        self.product_amount = product_amount
        self.order_price = order_price
        self.order_date = order_date

global_sell_count = 0

class Sell:
    def __init__(self, id, item, price, quantity, date, payment_method):
        global global_sell_count
        global_sell_count += 1
        self.id = global_sell_count 
        self.item = item
        self.id = id
        self.price = price
        self.quantity = quantity
        self.total_price = price * quantity
        self.date = date
        self.payment_method = payment_method

    def __str__(self):
        return (f"ID: {self.id}; Produto: {self.item}; Preço Unitário: {self.price:.2f}; "
                f"Quantidade: {self.quantity}; Total: {self.total_price:.2f}; "
                f"Data: {self.date}; Método de Pagamento: {self.payment_method}")

# Update product

def update_product():
    # Open the file to read and get all products
    try:
        with open("./data/products.txt", "r", encoding="UTF-8") as file:
            lines = file.readlines()  # Read all lines of the file
    except FileNotFoundError:
        print("Erro: Arquivo de produtos não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    # Request the product code to be updated
    os.system('cls')
    drawBox(1, 1, 120, 25, MAGENTA)
    gotoxy(3, 3)
    product_code = int(input("Digite o código do produto que deseja atualizar: "))

    # Variable to store whether the product was found or not
    product_found= False

    # New content to be written to the file
    new_content = []

    for line in lines:
        product_data = line.strip().split(";")
        present_code = int(product_data[0].split(":")[1])

        if present_code == product_code:
            product_found = True  

            # Exibir os dados atuais do produto, um atributo por linha
            gotoxy(3, 4)
            print("Produto encontrado:")
            gotoxy(3, 5); print(f"Código: {present_code}")
            gotoxy(3, 6); print(f"Nome: {product_data[1].split(':')[1]}")
            gotoxy(3, 7); print(f"Descrição: {product_data[2].split(':')[1]}")
            gotoxy(3, 8); print(f"Preço de compra: {product_data[3].split(':')[1]}")
            gotoxy(3, 9); print(f"Preço de venda: {product_data[4].split(':')[1]}")
            gotoxy(3, 10); print("Deixe o campo vazio se não quiser alterar um atributo.")

            # Pegar os novos valores ou manter os antigos
            gotoxy(3, 11)
            new_name = input(f"Nome atual ({product_data[1].split(':')[1]}): ") or product_data[1].split(":")[1]
            gotoxy(3, 12)
            new_description = input(f"Descrição atual ({product_data[2].split(':')[1]}): ") or product_data[2].split(":")[1]
            gotoxy(3, 13)
            new_buy_price = input(f"Preço de compra atual ({product_data[3].split(':')[1]}): ") or product_data[3].split(":")[1]
            gotoxy(3, 14)
            new_sell_price = input(f"Preço de venda atual ({product_data[4].split(':')[1]}): ") or product_data[4].split(":")[1]

            # Recriar a linha com os dados atualizados
            updated_line = (f"Código: {present_code}; Nome do produto: {new_name}; "
                                f"Descrição: {new_description}; Preço de compra: {new_buy_price}; "
                                f"Preço de venda: {new_sell_price}\n")

            # Adicionar a linha atualizada ao novo conteúdo
            new_content.append(updated_line)
        else:
            # Manter as linhas não modificadas
            new_content.append(line)

    # Se o produto foi encontrado, reescrever o arquivo com os novos dados
    if product_found:
        with open("./data/products.txt", "w", encoding="UTF-8") as file:
            file.writelines(new_content)  # Reescreve o arquivo com os dados atualizados
        gotoxy(3, 15)
        print("Produto atualizado com sucesso!")
    else:
        gotoxy(3, 16)
        print(f"Produto com o código {product_code} não foi encontrado.")

    gotoxy(3, 17)
    input("Pressione ENTER para voltar ao menu...")
    os.system('cls')  # Limpar a tela
    main()

# Delete product

def delete_product():
    # Open the file with registered products
    with open("./data/products.txt", "r", encoding="UTF-8") as file:
        lines = file.readlines()

    # If the file is empty
    if not lines:
        print("Nenhum produto encontrado...")
        return

    # Display registered products
    printTitle("Produtos cadastrados: ", GREEN, WHITE)
    print("\n")
    products = []
    for line in lines:
        # Create a Product object for each line of the file
        product_data = line.strip().split(";")
        product = Product(
            code=int(product_data[0].split(":")[1]),
            name=product_data[1].split(":")[1],
            description=product_data[2].split(":")[1],
            buying_price=float(product_data[3].split(":")[1]),
            selling_price=float(product_data[4].split(":")[1]),
        )
        products.append(product)

        # View product details
        print(f"Produto: {product.name}\nDescrição: {product.description}\nCódigo: {product.code}\nPreço de compra: R$ {product.buying_price}\nPreço de venda: R$ {product.selling_price}\n{'─'*80}")

    # Receive the product code that the user wants to delete
    try:
        product_code = int(input("Digite o código do produto que deseja apagar: "))
    except ValueError:
        print("Código inválido! Por favor, insira um número inteiro.")
        return
    
    # Check if the product with the code provided exists
    product_exists = any(p.code == product_code for p in products)
    if not product_exists:
        os.system('cls')
        printTitle("Erro: ", RED)
        drawBox(1, 4, 120, 6, MAGENTA)
        gotoxy(2, 5)
        print(f"Produto com código {product_code} não encontrado.")
        gotoxy(2, 8)
        print(input("Pressione ENTER para voltar ao menu..."))
        os.system('cls')
        main()
        return

    # Confirm removal
    os.system('cls')
    printTitle(f"Confirmar a remoção de produto de código: {product_code}...", RED, WHITE)
    
    # Filter products to remove the product with the given code
    products = [p for p in products if p.code != product_code]

    # Update the archive with remaining products
    with open("./data/products.txt", "w", encoding="UTF-8") as file:
        for product in products:
            # Rewrite each product in the file
            file.write(f"code:{product.code};name:{product.name};description:{product.description};buying_price:{product.buying_price};selling_price:{product.selling_price}\n")

    # Display the success message
    drawBox(1, 4, 120, 6, MAGENTA)
    gotoxy(2, 5)
    print(f"Produto de código {product_code} removido com sucesso.")
    
    gotoxy(2, 8)
    print(input("Pressione ENTER para voltar ao menu..."))
    os.system('cls')
    main()


def cancel_order():
    try:
        # Read orders from the file
        with open("./data/orders.txt", "r", encoding="UTF-8") as file:
            orders = file.readlines()
    except FileNotFoundError:
        print("Erro: Arquivo de pedidos não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    if not orders:
        print("Nenhum pedido encontrado.")
        input("Pressione ENTER para voltar ao menu...")
        os.system('cls')
        main()
        return

    print("Pedidos cadastrados:")
    for line in orders:
        order_data = line.strip().split(";")
        order_id = order_data[0].split(":")[1].strip()
        print(f"ID do pedido: {order_id}")

    order_id_to_cancel = input("Digite o ID do pedido que deseja cancelar: ").strip()

    # Check if the order ID exists
    order_found = False
    new_content = []

    for line in orders:
        order_data = line.strip().split(";")
        current_order_id = order_data[0].split(":")[1].strip()

        if current_order_id == order_id_to_cancel:
            order_found = True
            print(f"Pedido {order_id_to_cancel} cancelado com sucesso!")
            continue  # Skip the line to remove the order
        
        new_content.append(line)  # Keep orders that are not canceled

    # Rewrite the file without the canceled order
    if order_found:
        with open("./data/orders.txt", "w", encoding="UTF-8") as file:
            file.writelines(new_content)
    else:
        print(f"Pedido com ID {order_id_to_cancel} não encontrado.")

    input("Pressione ENTER para voltar ao menu...")
    os.system('cls')
    main()


def register_product_and_purchase():
    # Open the product file for writing
    try:
        with open("./data/products.txt", "a+", encoding="UTF-8") as products_file:
            products_file.seek(0)
            product_lines = products_file.readlines()

            # Track the last used product code
            last_product_code = 0
            if product_lines:
                last_product_line = product_lines[-1]
                last_product_code = int(last_product_line.strip().split(";")[0].split(":")[1])

            # Request product data
            printTitle("Ordem de compra", GREEN, WHITE)
            drawBox(1, 5, 120, 16, MAGENTA)
            gotoxy(2, 6)
            product_name = input("Digite o nome do produto: ")
            gotoxy(2, 7)
            product_desc = input("Descreva o produto: ")
            gotoxy(2, 8)
            buying_price = float(input("Digite o preço de compra do produto: "))
            gotoxy(2, 9)
            selling_price = float(input("Digite o preço de venda do produto: "))
            gotoxy(2, 10)
            product_amount = int(input("Digite a quantidade comprada: "))

            # Validate purchase date
            date_regex = re.compile(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$")
            while True:
                gotoxy(2, 11)
                order_date = input("Digite a data da compra no formato dd/mm/aaaa: ")
                if date_regex.match(order_date):
                    break
                else:
                    print("Data inválida. Insira no formato correto (dd/mm/aaaa).")

            # Calculate total purchase value (quantity * purchase price)
            total_buying_value = buying_price * product_amount

            # Create new product and add to archive
            new_product = Product(code=last_product_code + 1, name=product_name, description=product_desc, buying_price=buying_price, selling_price=selling_price)
            products_file.write(f"{new_product}\n")
            gotoxy(2, 12)
            print(f"Produto '{new_product.name}' registrado com sucesso!")

    except Exception as e:
        gotoxy(2, 12)
        print(f"Erro ao manipular o arquivo de produtos: {e}")
        return

    # Register in order file
    try:
        with open("./data/orders.txt", "a+", encoding="UTF-8") as orders_file:
            orders_file.seek(0)
            order_lines = orders_file.readlines()

            # Track the last used order ID
            last_order_id = 0
            if order_lines:
                last_order_line = order_lines[-1]
                last_order_id = int(last_order_line.strip().split(";")[0].split(":")[1])

            # Calculate total purchase price (selling price * quantity)
            total_selling_value = selling_price * product_amount

            # Create new order and add to file
            new_order = Order(order_id=last_order_id + 1, product_id=new_product.code, product_amount=product_amount, order_price=total_selling_value, order_date=order_date)
            orders_file.write(f"ID da compra: {new_order.order_id}; Código: {new_product.code}; Quantidade: {new_order.product_amount}; Preço Compra Total: {total_buying_value:.2f}; Preço Venda Total: {total_selling_value:.2f}; Data: {new_order.order_date}\n")
            gotoxy(2, 14)
            printColored(f"Compra registrada com sucesso! Total da compra: R$ {total_selling_value:.2f}", GREEN, end="")

    except Exception as e:
        gotoxy(2, 14)
        printColored(f"Erro ao registrar a compra: {e}", RED, end="")
        return

    # Return to main menu  
    gotoxy(2, 15)
    input("Pressione ENTER para voltar ao menu principal...")
    os.system('cls')
    main()

# show purchase history

def show_purchase_history():
    try:
        # Read orders from the file
        with open("./data/orders.txt", "r", encoding="UTF-8") as file:
            orders = file.readlines()
    except FileNotFoundError:
        print("Erro: Arquivo de pedidos não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    if not orders:
        print("Nenhum pedido encontrado.")
    else:
        printTitle("Histórico de Compras", GREEN, WHITE)
        print("\n")

        for line in orders:
            order_data = line.strip().split(";")
            order_id = order_data[0].split(":")[1].strip()
            product_code = order_data[1].split(":")[1].strip()
            quantity = order_data[2].split(":")[1].strip()
            total_price = order_data[3].split(":")[1].strip()
            order_date = order_data[4].split(":")[1].strip()

            print(f"ID do Pedido: {order_id}")
            print(f"Código do Produto: {product_code}")
            print(f"Quantidade: {quantity}")
            print(f"Preço Total: R$ {total_price}")
            print(f"Data: {order_date}")
            print("─" * 40)

    input("Pressione ENTER para continuar...")
    os.system('cls') 
    main()

# Show products list

def show_all_products():
    file = open("./data/products.txt", "r", encoding="UTF-8")

    if not file:
        print("Nenhum produto encontrado...")
    else:
        printTitle("Produtos cadastrados: ", GREEN, WHITE)
        print("\n")

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
            print(f"Produto: {product.name}\nDescrição: {product.description}\nCódigo: {product.code}\nPreço de compra: R$ {product.buying_price}\nPreço de venda: R$ {product.selling_price}\n{'─'*80}")

    file.close()  # Close the file after processing
    input("\nPressione ENTER para continuar...")
    os.system('cls')  # Clear the screen
    main()

# Register new sale

def new_sale():
    clearScreen()
    printTitle("Nova Venda", MAGENTA, MAGENTA)

    try:
        with open("./data/products.txt", "r", encoding="utf-8") as file:
            products = []
            date_regex = re.compile(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$")

            for line in file:
                try:
                    fields = line.strip().split(";")
                    if len(fields) < 5:
                        gotoxy(2, 7)
                        print(f"Erro ao processar a linha: {line}. Formatação incorreta.")
                        continue
                    
                    code = int(fields[0].split(":")[1].strip())
                    name = fields[1].split(":")[1].strip()
                    selling_price = float(fields[4].split(":")[1].strip())
                    
                    products.append((code, name, selling_price))

                except (IndexError, ValueError) as e:
                    gotoxy(2, 7)
                    print(f"Erro ao processar a linha: {line}. Erro: {e}")
                    continue
            
            if not products:
                gotoxy(2, 7)
                print("Nenhum produto disponível para venda.")
                return

            drawBox(1, 5, 120, 16, WHITE)
            gotoxy(2, 6)
            selected_product = int(input("Digite o código do produto: "))
            product_found = next((p for p in products if p[0] == selected_product), None)

            if product_found:
                gotoxy(2, 7)
                print(f"Produto selecionado: {product_found[1]} - Preço de venda: R${product_found[2]:.2f}")
                
                gotoxy(2, 8)
                quantity = int(input("Digite a quantidade: "))
                
                gotoxy(2, 9)
                while True:
                    selling_date = input("Digite a data da venda (dd/mm/aaaa): ")
                    if re.match(date_regex, selling_date):
                        break
                    gotoxy(2, 10)
                    print("Erro: Data inválida. Formato dd/mm/aaaa.")

                gotoxy(2, 11)
                payment_method = input("Informe o método de pagamento: ")

                # Generate a new sales ID based on previous sales
                try:
                    with open("./data/sell_log.txt", "r", encoding="utf-8") as sell_file:
                        last_sale = sell_file.readlines()[-1]
                        last_id = int(last_sale.split(";")[0].split(":")[1].strip())
                        sale_id = last_id + 1
                except (FileNotFoundError, IndexError):
                    # If the file does not exist or is empty, we start with ID 1
                    sale_id = 1

                # Sell ​​instance creation
                sale = Sell(
                    id=sale_id,
                    item=product_found[1],
                    price=product_found[2],
                    quantity=quantity,
                    date=selling_date,
                    payment_method=payment_method
                )

                # Record the sale in the log file
                with open("./data/sell_log.txt", "a", encoding="utf-8") as sell_file:
                    sell_file.write(str(sale) + "\n")

                # View sale confirmation
                gotoxy(2, 12)
                printColored(f"Venda ID {sale_id} realizada: {quantity}x {product_found[1]} a R${product_found[2]:.2f} cada com {payment_method} como forma de pagamento.", GREEN)
                gotoxy(2, 13)
                print(f"Total: R${sale.total_price:.2f}")
                gotoxy(2, 14)
                input("Pressione ENTER para voltar ao menu...")
                main()

            else:
                gotoxy(2, 15)
                printColored("Erro: Produto não encontrado.", RED)

    except FileNotFoundError:
        gotoxy(2, 7)
        print("Erro: Arquivo de produtos não encontrado.")
    except Exception as e:
        gotoxy(2, 7)
        print(f"Erro inesperado: {e}")


    except FileNotFoundError:
        print("Erro: Arquivo de produtos não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# cancel sale

def cancel_sale():
    clearScreen()
    printTitle("Cancelar Venda", RED, RED)
    
    try:
        # Open the sales file
        with open("./data/sell_log.txt", "r", encoding="utf-8") as sell_file:
            sales = sell_file.readlines()
            
            if not sales:
                gotoxy(1, 5)
                print("Nenhuma venda registrada.")
                gotoxy(1, 6)
                input("Pressione ENTER para voltar ao menu...")
                main()

        # Show all recorded sales
        gotoxy(1, 5)
        print("Vendas registradas:\n")
        for sale in sales:
            print(f"{sale.strip()}")

        # Request the ID of the sale to be canceled
        sale_id = int(input("\nDigite o ID da venda que deseja cancelar (ou '0' para cancelar a operação): "))

        if sale_id == 0:
            os.system('cls')
            printTitle("Cancelamento de venda abortado.", GREEN)
            gotoxy(1, 5)
            input("Pressione ENTER para voltar ao menu...")
            main()

        # Check if the entered ID is valid
        sale_found = None
        for sale in sales:
            sale_data = sale.split(";")
            if int(sale_data[0].split(":")[1].strip()) == sale_id:
                sale_found = sale
                break

        if not sale_found:
            os.system('cls')
            printTitle("Erro: Venda com ID não encontrada.", RED)
            gotoxy(1, 5)
            input("Pressione ENTER para voltar ao menu...")
            main()

        # Remove the found sale from the list
        sales.remove(sale_found)

        # Save remaining sales to file by overwriting original file
        with open("./data/sell_log.txt", "w", encoding="utf-8") as sell_file:
            sell_file.writelines(sales)

        # Record cancellation in a new cancellation log file
        with open("./data/canceled_sales.txt", "a", encoding="utf-8") as cancel_file:
            cancel_file.write(f"Venda cancelada: {sale_found.strip()}\n")

        os.system('cls')
        printTitle(f"A venda com ID {sale_id} foi cancelada com sucesso.", MAGENTA)
        gotoxy(1, 5)
        input("Pressione ENTER para voltar ao menu...")

    except FileNotFoundError:
        os.system('cls')
        printTitle("Erro: Arquivo de vendas não encontrado.", YELLOW)
        gotoxy(2, 5)
        input("Pressione ENTER para voltar ao menu...")
    except ValueError:
        os.system('cls')
        printTitle("Erro: Entrada inválida, por favor digite um número.")
        gotoxy(2, 5)
        input("Pressione ENTER para voltar ao menu...")
    except Exception as e:
        os.system('cls')
        print(f"Erro inesperado: {e}")
        gotoxy(2, 5)
        input("Pressione ENTER para voltar ao menu...")

    clearScreen()
    main()
# Sale history

def show_sales_history():
    clearScreen()
    printTitle("Histórico de Vendas", BLUE, WHITE)
    
    try:
        # Open the sales file
        with open("./data/sell_log.txt", "r", encoding="utf-8") as sell_file:
            sales = sell_file.readlines()

            if not sales:
                gotoxy(1, 5)
                print("Nenhuma venda registrada.")
                gotoxy(1, 6)
                input("Pressione ENTER para voltar ao menu...")
                return

        # View all sales

        for i, sale in enumerate(sales, start=1):
            gotoxy(2, 3 + i)
            print(f"{sale.strip()}")

        # After displaying sales, ask the user to press ENTER to return to the main menu
        gotoxy(2, 5 + i)
        input("Pressione ENTER para voltar ao menu...")

    except FileNotFoundError:
        gotoxy(2, 5)
        print("Erro: Arquivo de vendas não encontrado.")
        gotoxy(2, 6)
        input("Pressione ENTER para voltar ao menu...")
    except Exception as e:
        gotoxy(2, 5)
        print(f"Erro inesperado: {e}")
        gotoxy(2, 6)
        input("Pressione ENTER para voltar ao menu...")

    clearScreen()
    main()

# cancelled sales

def show_cancelled_sales_history():
    clearScreen()
    printTitle("Histórico de Vendas Canceladas", WHITE)
    
    try:
        # Open the canceled sales file
        with open("./data/canceled_sales.txt", "r", encoding="utf-8") as cancel_file:
            cancelled_sales = cancel_file.readlines()
            
            if not cancelled_sales:
                gotoxy(1, 5)
                print("Nenhuma venda cancelada registrada.")
                gotoxy(1, 6)
                input("Pressione ENTER para voltar ao menu...")
                main()
            else:
                # Variable to control the print line
                start_row = 5
                
                for sale in cancelled_sales:
                    gotoxy(2, start_row)
                    print(sale.strip())
                    
                    
                    start_row += 1

                gotoxy(1, start_row + 1)
                input("Pressione ENTER para voltar ao menu...")
                main()

    except FileNotFoundError:
        gotoxy(1, 5)
        print("Erro: Arquivo de vendas canceladas não encontrado.")
        gotoxy(1, 6)
        input("Pressione ENTER para voltar ao menu...")
        main()
def main():


    menu = f"MENU"
    menu1 = '1. Nova compra'
    menu2 = '2. Cancelar compra'
    menu3 = '3. Exibir produtos'
    menu4 = '4. Editar produto'
    menu5 = '5. Apagar produto'
    menu6 = '6. Histórico de compras'
    menu7 = '7. Nova venda'
    menu8 = '8. Cancelar venda'
    menu9 = '9. Histórico de vendas'
    menu10 = '10. Vendas canceladas'
    menu11 = '11. Sair'



    while True:
        os.system('cls') # Clear the screen
        printTitle(menu, GREEN)
        
        drawRoundBorderBox(1, 4, 120, 22, GREEN)

        gotoxy(5, 6); printGreen(menu1, end="")
        gotoxy(5, 7); printGreen(menu2, end="")
        gotoxy(5, 8); printGreen(menu3, end="")
        gotoxy(5, 9); printGreen(menu4, end="")
        gotoxy(5, 10); printGreen(menu5, end="")
        gotoxy(5, 11); printGreen(menu6, end="")
        gotoxy(5, 12); printGreen(menu7, end="")
        gotoxy(5, 13); printGreen(menu8, end="")
        gotoxy(5, 14); printGreen(menu9, end="")
        gotoxy(5, 15); printGreen(menu10, end="")
        gotoxy(5, 16); printGreen(menu11, end="")
        gotoxy(5, 20); option = input("Digite o número da opção: ")


        if option == "1":
            os.system('cls')
            register_product_and_purchase()
        elif option == "2":
            os.system('cls')
            cancel_order()
        elif option == "3":
            os.system('cls')
            show_all_products()
        elif option == "4":
            update_product()
        elif option == "5":
            os.system('cls')
            delete_product()
        elif option == "6":
            os.system('cls')
            show_purchase_history()
        elif option == "7":
            os.system('cls')
            new_sale()
        elif option == "8":
            os.system('cls')
            cancel_sale()
        elif option == "9":
            os.system('cls')
            show_sales_history()
        elif option == "10":
            os.system('cls')
            show_cancelled_sales_history()
        elif option == "11":
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
            drawBox(1, 1, 60, 7, RED)
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