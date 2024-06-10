import json
import uuid


filmes = {}
ingressos = {}
usuarios = {"admin": {"senha": "admin", "tipo_usuario": "admin"}, "cliente": {"senha": "cliente", "tipo_usuario": "cliente"}}
ingressos_comprados = {"admin": [], "cliente": []}
sessao = None

def registrar():
    nome_usuario = input("Digite o novo nome de usuário: ")
    if nome_usuario in usuarios:
        print("Nome de usuário inválido. Escolha um nome de usuário diferente.")
        return

    senha = input("Digite a senha: ")
    tipo_usuario = input("Digite o seu tipo de usuário (admin/cliente): ").lower()
    if tipo_usuario not in ["admin", "cliente"]:
        print("Tipo de usuário inválido. Escolha 'admin' ou 'cliente'.")
        return

    usuarios[nome_usuario] = {"senha": senha, "tipo_usuario": tipo_usuario}
    ingressos_comprados[nome_usuario] = []
    print(f"Usuário '{nome_usuario}' registrado com sucesso como '{tipo_usuario}'.")

def login(nome_usuario, senha):
    usuario = usuarios.get(nome_usuario)
    if usuario and usuario["senha"] == senha:
        global sessao
        sessao = nome_usuario
        return usuario
    else:
        return None

def logout():
    global sessao
    sessao = None
    print("Logout realizado com sucesso.")

def menu_admin():
    print("Menu Administrador:")
    print("1. Adicionar Filme")
    print("2. Gerenciar Filmes")
    print("3. Buscar Filmes")
    print("4. Listar Ingressos Vendidos")
    print("5. Listar Ingressos Vendidos por Filme")
    print("6. Exportar Ingressos Vendidos para TXT")
    print("7. Adicionar Reservas de Cortesia")
    print("8. Mostrar Assentos Disponíveis por Filme")
    print("9. Logout")
    escolha = input("Digite a opção: ")
    return escolha

def menu_cliente():
    print("Menu Cliente:")
    print("1. Comprar Ingressos")
    print("2. Listar Ingressos Comprados")
    print("3. Exportar Ingressos Comprados para TXT")
    print("4. Filmes em Alta")
    print("5. Logout")
    escolha = input("Digite a opção: ")
    return escolha

def adicionar_filme():
    id_filme = str(uuid.uuid4())
    titulo = input("Digite o título do filme: ")
    assentos_disponiveis = int(input("Digite o número de assentos disponíveis: "))
    valor_ingresso = float(input("Digite o valor do ingresso: "))
    filmes[id_filme] = {"titulo": titulo, "assentos_disponiveis": assentos_disponiveis, "valor_ingresso": valor_ingresso}
    print(f"Filme '{titulo}' adicionado com sucesso!")

def gerenciar_filmes():
    for id_filme, detalhes in filmes.items():
        print(
            f"ID: {id_filme}, Título: {detalhes['titulo']}, Assentos Disponíveis: {detalhes['assentos_disponiveis']}, Valor do Ingresso: R$ {detalhes['valor_ingresso']:.2f}")
    titulo = input("Digite o título do filme para gerenciar: ")
    encontrado = False
    for id_filme, detalhes in filmes.items():
        if titulo.lower() in detalhes['titulo'].lower():
            encontrado = True
            print(f"1. Atualizar {detalhes['titulo']}")
            print(f"2. Remover {detalhes['titulo']}")
            escolha = input("Digite a opção: ")
            if escolha == "1":
                novo_titulo = input("Digite o novo título: ")
                assentos_disponiveis = int(input("Digite o novo número de assentos disponíveis: "))
                valor_ingresso = float(input("Digite o novo valor do ingresso: "))
                filmes[id_filme] = {"titulo": novo_titulo, "assentos_disponiveis": assentos_disponiveis,
                                    "valor_ingresso": valor_ingresso}
                print(f"Filme '{novo_titulo}' atualizado com sucesso!")
            elif escolha == "2":
                del filmes[id_filme]
                print(f"Filme '{detalhes['titulo']}' removido com sucesso!")
            break
    if not encontrado:
        print("Filme não encontrado.")
def buscar_filmes():
    titulo = input("Digite o título do filme para buscar: ")
    encontrado = False
    for id_filme, detalhes in filmes.items():
        if titulo.lower() in detalhes["titulo"].lower():
            print(f"ID: {id_filme}, Título: {detalhes['titulo']}, Assentos Disponíveis: {detalhes['assentos_disponiveis']}, Valor do Ingresso: R$ {detalhes['valor_ingresso']:.2f}")
            encontrado = True
    if not encontrado:
        print("Nenhum filme encontrado.")

def listar_ingressos_vendidos():
    for id_filme, detalhes in filmes.items():
        if id_filme in ingressos:
            print(f"Filme: {detalhes['titulo']}, Ingressos Vendidos: {len(ingressos_comprados[id_filme])}")

def listar_ingressos_vendidos_por_filme():
    titulo = input("Digite o título do filme para listar ingressos vendidos: ")
    encontrado = False
    for id_filme, detalhes in filmes.items():
        if titulo.lower() in detalhes["titulo"].lower():
            if id_filme in ingressos:
                print(f"Filme: {detalhes['titulo']}, Ingressos Vendidos: {len(ingressos_comprados[id_filme])}")
            else:
                print(f"Filme: {detalhes['titulo']}, Ingressos Vendidos: 0")
            encontrado = True
            break
    if not encontrado:
        print("Filme não encontrado.")

def Reservas_de_cortesia():
    titulo = input("Digite o título do filme para adicionar reservas de cortesia: ")
    encontrado = False
    for id_filme, detalhes in filmes.items():
        if titulo.lower() in detalhes["titulo"].lower():
            encontrado = True
            quantidade = int(input(f"Digite a quantidade de ingressos de cortesia para {detalhes['titulo']}: "))
            if quantidade <= detalhes['assentos_disponiveis']:
                filmes[id_filme]['assentos_disponiveis'] -= quantidade
                print(
                    f"Reservas de cortesia ajustadas para o filme '{detalhes['titulo']}'. Assentos restantes: {filmes[id_filme]['assentos_disponiveis']}")
            else:
                print(
                    f"Quantidade de ingressos de cortesia maior do que os assentos disponíveis para o filme '{detalhes['titulo']}'")
            break
    if not encontrado:
        print("Filme não encontrado.")

def mostrar_assentos_disponiveis_por_filme():
    titulo = input("Digite o título do filme para mostrar assentos disponíveis: ")
    encontrado = False
    for id_filme, detalhes in filmes.items():
        se_filme_encontrado = titulo.lower() in detalhes["titulo"].lower()
        if se_filme_encontrado:
            encontrado = True
            print(f"Assentos Disponíveis para {detalhes['titulo']}: {detalhes['assentos_disponiveis']}")
            break
    if not encontrado:
        print("Filme não encontrado.")

def salvar_ingresso_cliente(nome_usuario, id_filme, num_ingressos):
    with open(f"ingressos_cliente_{nome_usuario}.txt", "a") as arquivo:
        arquivo.write(f"{id_filme}, {num_ingressos}\n")

def salvar_ingresso_vendido(nome_usuario, id_filme, num_ingressos):
    with open(f"ingressos_vendidos_{id_filme}.txt", "a") as arquivo:
        arquivo.write(f"{nome_usuario}, {num_ingressos}\n")

def comprar_ingressos(nome_usuario):
    print(filmes)
    titulo = input("Digite o título do filme que deseja comprar ingressos: ")
    encontrado = False
    for id_filme, detalhes in filmes.items():
        if titulo.lower() in detalhes["titulo"].lower():
            encontrado = True
            print(f"ID: {id_filme}, Título: {detalhes['titulo']}, Assentos Disponíveis: {detalhes['assentos_disponiveis']}, Valor do Ingresso: R$ {detalhes['valor_ingresso']:.2f}")
            quantidade = int(input("Digite a quantidade de ingressos que deseja comprar: "))
            if quantidade <= 0:
                print("Quantidade inválida.")
                return

            if filmes[id_filme]["assentos_disponiveis"] < quantidade:
                print("Não há assentos suficientes disponíveis.")
                return

            valor_total = filmes[id_filme]["valor_ingresso"] * quantidade
            print(f"Total a pagar: R$ {valor_total:.2f}")
            forma_pagamento = input("Digite a forma de pagamento (pix/outro): ").lower()
            if forma_pagamento == "pix":
                print(f"QR Code PIX gerado:\n")
            else:
                processar_pagamento(nome_usuario, id_filme, quantidade, valor_total)

            filmes[id_filme]["assentos_disponiveis"] -= quantidade
            ingressos_comprados[nome_usuario].append({"id_filme": id_filme, "quantidade": quantidade})
            if id_filme not in ingressos:
                ingressos[id_filme] = []
            ingressos[id_filme].append({"usuario": nome_usuario, "quantidade": quantidade})

            salvar_ingresso_cliente(nome_usuario, id_filme, quantidade)
            salvar_ingresso_vendido(nome_usuario, id_filme, quantidade)

            print("Compra realizada com sucesso!")
            break
    if not encontrado:
        print("Filme não encontrado.")

def gerar_qrcode_pix(valor_total):
    return f"QR Code de pagamento PIX para o valor de R$ {valor_total:.2f}"

def processar_pagamento(nome_usuario, id_filme, quantidade, valor_total):
    print(f"Pagamento de R$ {valor_total:.2f} processado com sucesso para {quantidade} ingressos do filme ID {id_filme}.")

def listar_ingressos_comprados(nome_usuario):
    print("Ingressos comprados:")
    for ingresso in ingressos_comprados[nome_usuario]:
        id_filme = ingresso["id_filme"]
        quantidade = ingresso["quantidade"]
        detalhes = filmes.get(id_filme, {"titulo": "Desconhecido"})
        print(f"Filme: {detalhes['titulo']}, Quantidade: {quantidade}")

def exportar_ingressos_comprados_para_txt(nome_usuario):
    with open(f"ingressos_comprados_{nome_usuario}.txt", "w") as arquivo:
        for ingresso in ingressos_comprados[nome_usuario]:
            id_filme = ingresso["id_filme"]
            quantidade = ingresso["quantidade"]
            detalhes = filmes.get(id_filme, {"titulo": "Desconhecido"})
            arquivo.write(f"Filme: {detalhes['titulo']}, Quantidade: {ingressos_comprados}\n")
    print("Ingressos comprados exportados com sucesso!")

def filmes_em_alta():
    vendidos_por_filme = {}
    for id_filme, ingressos_vendidos in ingressos.items():
        vendidos_por_filme[id_filme] = len(ingressos_vendidos)
    filmes_ordenados = sorted(vendidos_por_filme.items(), key=lambda x: x[1], reverse=True)
    print("Filmes em Alta:")
    for id_filme, vendidos in filmes_ordenados:
        detalhes = filmes.get(id_filme, {"titulo": "Desconhecido"})
        print(f"Filme: {detalhes['titulo']}, Ingressos Vendidos: {ingressos_vendidos:}")

while True:
    if sessao:
        usuario = usuarios[sessao]
        if usuario["tipo_usuario"] == "admin":
            escolha = menu_admin()
            if escolha == "1":
                adicionar_filme()
            elif escolha == "2":
                gerenciar_filmes()
            elif escolha == "3":
                buscar_filmes()
            elif escolha == "4":
                listar_ingressos_vendidos()
            elif escolha == "5":
                listar_ingressos_vendidos_por_filme()
            elif escolha == "6":
                exportar_ingressos_vendidos_para_txt()
            elif escolha == "7":
                Reservas_de_cortesia()
            elif escolha == "8":
                mostrar_assentos_disponiveis_por_filme()
            elif escolha == "9":
                logout()
            else:
                print("Opção inválida.")
        elif usuario["tipo_usuario"] == "cliente":
            escolha = menu_cliente()
            if escolha == "1":
                comprar_ingressos(sessao)
            elif escolha == "2":
                listar_ingressos_comprados(sessao)
            elif escolha == "3":
                exportar_ingressos_comprados_para_txt(sessao)
            elif escolha == "4":
                filmes_em_alta()
            elif escolha == "5":
                logout()
            else:
                print("Opção inválida.")
    else:
        print("1. Registrar")
        print("2. Login")
        print("3. Sair")
        opcao = input("Digite a opção: ")
        if opcao == "1":
            registrar()
        elif opcao == "2":
            nome_usuario = input("Digite o nome de usuário: ")
            senha = input("Digite a senha: ")
            if login(nome_usuario, senha):
                print(f"Bem-vindo(a), {nome_usuario}!")
            else:
                print("Nome de usuário ou senha incorretos.")
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")