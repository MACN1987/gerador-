import random
import os
import time
import sys
from validate_docbr import CPF, CNPJ

# Para formatos coloridos no terminal
AZUL_NEGRITO = '\033[1;34m'
VERDE_NEGRITO = '\033[1;32m'
VERMELHO_NEGRITO = '\033[1;31m'
BRANCO_NEGRITO = '\033[1;37m'
RESET = '\033[0m'

# Dicionário código -> estados para CPF
estados_codigos = {
    '0': 'RS',
    '1': 'DF, GO, MT, MS, TO',
    '2': 'AC, AP, AM, PA, RO, RR',
    '3': 'CE, MA, PI',
    '4': 'AL, PB, PE, RN',
    '5': 'BA, SE',
    '6': 'MG',
    '7': 'ES, RJ',
    '8': 'SP',
    '9': 'PR, SC',
}

cpf_obj = CPF()
cnpj_obj = CNPJ()

def limpa_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def contagem_regressiva(t):
    for i in range(t, 0, -1):
        sys.stdout.write(f"\rEncerrando em {i} segundos... ")
        sys.stdout.flush()
        time.sleep(1)
    print("\rEncerrando agora!           ")

def espera_usuario():
    resposta = input("Pressione qualquer tecla para continuar ou 'S' para sair: ").strip().upper()
    return resposta == 'S'

def calcula_digitos_verificadores(cpf_base):
    soma = sum(int(digito) * peso for digito, peso in zip(cpf_base, range(10, 1, -1)))
    resto = soma % 11
    digito1 = '0' if resto < 2 else str(11 - resto)

    cpf_com_digito1 = cpf_base + digito1
    soma = sum(int(digito) * peso for digito, peso in zip(cpf_com_digito1, range(11, 1, -1)))
    resto = soma % 11
    digito2 = '0' if resto < 2 else str(11 - resto)

    return digito1 + digito2

def gerar_cpf_por_codigo_estado(codigo):
    while True:
        primeiros_8_digitos = ''.join(str(random.randint(0, 9)) for _ in range(8))
        if len(set(primeiros_8_digitos)) > 1:
            break
    cpf_base = primeiros_8_digitos + codigo
    digitos_verificadores = calcula_digitos_verificadores(cpf_base)
    return cpf_base + digitos_verificadores

def gerar_cnpj_valido():
    return cnpj_obj.generate(mask=True)

def main():
    limpa_tela()
    print(f"{BRANCO_NEGRITO}Bem-vindo ao Gerador de CPF e CNPJ válido{RESET}\n")

    while True:
        print(f"{BRANCO_NEGRITO}Escolha uma opção:{RESET}")
        print(f"{BRANCO_NEGRITO}1 - Gerar CPF{RESET}")
        print(f"{BRANCO_NEGRITO}2 - Gerar CNPJ{RESET}")
        print(f"{BRANCO_NEGRITO}S - Sair{RESET}")

        opcao = input("\nDigite a opção: ").strip().upper()

        if opcao == 'S':
            print(f"{VERMELHO_NEGRITO}Obrigado por usar o gerador CPF/CNPJ. Até a próxima.{RESET}")
            contagem_regressiva(5)
            limpa_tela()
            break

        elif opcao == '1':
            while True:
                print(f"{BRANCO_NEGRITO}Escolha um código de estado (0 a 9) para gerar um CPF:{RESET}")
                for codigo, estados in estados_codigos.items():
                    print(f"{BRANCO_NEGRITO}{codigo} - {estados}{RESET}")

                codigo = input("\nDigite o código: ").strip()
                if codigo in estados_codigos:
                    cpf = gerar_cpf_por_codigo_estado(codigo)
                    cpf_formatado = cpf_obj.mask(cpf)
                    print(f"\nCódigo selecionado: {AZUL_NEGRITO}{codigo}{RESET} (Estados: {estados_codigos[codigo]})")
                    print(f"{AZUL_NEGRITO}CPF gerado: {cpf_formatado}{RESET}\n")
                    break
                else:
                    print(f"{VERMELHO_NEGRITO}Código inválido. Tente novamente.{RESET}")

            if espera_usuario():
                print(f"{VERMELHO_NEGRITO}Obrigado por usar o gerador CPF/CNPJ. Até a próxima.{RESET}")
                contagem_regressiva(5)
                limpa_tela()
                break
            limpa_tela()

        elif opcao == '2':
            cnpj = gerar_cnpj_valido()
            print(f"\n{VERDE_NEGRITO}CNPJ gerado: {cnpj}{RESET}\n")
            if espera_usuario():
                print(f"{VERMELHO_NEGRITO}Obrigado por usar o gerador CPF/CNPJ. Até a próxima.{RESET}")
                contagem_regressiva(5)
                limpa_tela()
                break
            limpa_tela()
        else:
            print(f"{VERMELHO_NEGRITO}Opção inválida. Tente novamente.{RESET}")

if __name__ == "__main__":
    main()

