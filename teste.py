import textwrap

def menu():
    menu = """\n
    _____________________  MENU ________________________
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nc]\tNova conta
[lc]\tListar contas
[nu]\tNovo usuário
[q]\tSair
=> """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito:\tR$ {valor:.2f}\n'
        print("\n=== Depósito realizado com sucesso! ===\n")
    else:
        print("\n@@@ Valor inválido! @@@\n")
    return saldo, extrato

def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Saldo insuficiente! @@@\n")
    elif excedeu_limite:
        print("\n@@@ Limite de saque excedido! @@@\n")
    elif excedeu_saques:
        print("\n@@@ Limite de saques diários excedido! @@@\n")
    elif valor > 0:
        saldo -= valor
        extrato += f'Saque:\tR$ {valor:.2f}\n'
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===\n")
    else:
        print("\n@@@ Valor inválido! @@@\n")
    return saldo, extrato, numero_saques

def extrato(saldo, extrato):
    print("\n                  EXTRATO                         ")
    print("Não foram realizadas movimentações.") if not extrato else print(extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("\nPressione Enter para continuar...")
    input()  # Aguarda o usuário pressionar Enter

def criar_usuario(usuarios):
    cpf = input("Informe o cpf (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ CPF já cadastrado! @@@\n")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade - estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n=== Usuário criado com sucesso! ===\n")

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o cpf do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===\n")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, criação de conta cancelada! @@@\n")
    return None

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == "d":
            if not contas:
                print("\n@@@ É necessário criar uma conta antes de realizar um depósito! @@@\n")
                continue
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            if not contas:
                print("\n@@@ É necessário criar uma conta antes de realizar um saque! @@@\n")
                continue
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            if not contas:
                print("\n@@@ É necessário criar uma conta para exibir o extrato! @@@\n")
                continue
            extrato(saldo, extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, selecione novamente por favor.")

main()
