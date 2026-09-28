import json
import math
import random
from datetime import datetime


ARQUIVO = "conta.json"
LIMITE_DIARIO = 500.00


def carregar_contas():
   try:
      with open(ARQUIVO, "r", encoding="utf-8") as f:
         return json.load(f)
   except FileNotFoundError:
      return {}


def salvar_contas(contas):
   try:
      with open(ARQUIVO, "w", encoding="utf-8") as f:
         json.dump(contas, f, ensure_ascii=False, indent=2)
      print("Conta salva com sucesso!")
   except Exception as e:
      print(f"Erro ao salvar conta: {e}")


def pedir_pin(conta):
   for tentativa in range(3):
      pin = input("Digite o seu PIN para confirmar: ")
      if pin == conta["pin"]:
         return True
      print(f"X PIN incorreto. Restam {2 - tentativa} tentativa(s).")
   return False


def ler_valor(pergunta):
   try:
      valor = float(input(pergunta).replace(",", "."))
      if not math.isfinite(valor):
         raise ValueError
      return round(valor, 2)
   except ValueError:
      print("Digite um numero valido.")
      return None


def data_de_hoje():
   return datetime.now().strftime("%d/%m/%Y")


def sacado_hoje(conta):
   saques = conta.get("saques", [])
   return sum(s["valor"] for s in saques if s["data"] == data_de_hoje())


def escolher_conta(contas):
   lista = list(contas.values())
   if len(lista) == 1:
      return lista[0]


   print("\nEscolha a conta que deseja acessar:")
   for i, c in enumerate(lista, start=1):
      print(f"  [{i}] {c['titular']} ({c['conta']})")


   while True:
      escolha = input("Digite o número da opção: ").strip()
      if escolha.isdigit() and 1 <= int(escolha) <= len(lista):
         return lista[int(escolha) - 1]
      print(f"X Opção inválida. Digite um número de 1 a {len(lista)}.")


def criar_conta(contas):
   nome = input("Nome do titular da conta: ").strip()
   if not nome:
      print("X O nome não pode ficar vazio.")
      return None


   pin = input("Crie um PIN de 4 dígitos: ")
   if len(pin) != 4 or not pin.isdigit():
      print("X O PIN precisa ter exatamente 4 números. Conta não criada.")
      return None


   if input("Digite o PIN novamente para confirmar: ") != pin:
      print("X Os PINs não são iguais. Conta não criada.")
      return None


   numero = ""
   while numero == "" or numero in contas:
      numero = f"{random.randint(1000, 9999)}.{random.randint(1000, 9999)}-{random.randint(0, 9)}"


   conta = {"titular": nome, "pin": pin, "agencia": "088", "conta": numero,
            "saldo": 0.00, "historico": [], "saques": []}
   contas[numero] = conta
   print(f"Conta criada para {nome}! Número da conta: {numero}")
   return conta


def depositar(conta, valor):
   if valor <= 0:
      print("O valor do deposito não pode ser negativo,por favor não insista.")
      return
   conta["saldo"] += valor
   conta["historico"].append(f"Depósito em sua conta de R$ {valor:.2f}")
   print(f"Depósito realizado com sucesso. Saldo atual: R$ {conta['saldo']:.2f}")


def sacar(conta, valor):
   if valor <= 0:
      print("X O valor do levantamento deve ser positivo.")
      return
   if valor > conta["saldo"]:
      print("X O seu saldo é insuficiente para este levantamento.")
      return


   restante = max(0, LIMITE_DIARIO - sacado_hoje(conta))
   if valor > restante:
      print(f"X Limite diário de R$ {LIMITE_DIARIO:.2f} atingido. Ainda dá para levantar R$ {restante:.2f}.")
      return


   conta["saldo"] -= valor
   conta.setdefault("saques", []).append({"data": data_de_hoje(), "valor": valor})
   conta["historico"].append(f"Levantamento de R$ {valor:.2f}")
   print(f"Levantamento realizado com sucesso. Saldo atual: R$ {conta['saldo']:.2f}")


def transferir(contas, origem):
   numero = input("Número da conta de destino: ").strip()
   if numero == origem["conta"] or numero not in contas:
      print("X Conta de destino inválida. Confira o número e tente de novo.")
      return
   destino = contas[numero]


   valor = ler_valor(f"Quanto deseja enviar para {destino['titular']}? R$ ")
   if valor is None:
      return
   if valor <= 0 or valor > origem["saldo"]:
      print("X Valor inválido ou saldo insuficiente.")
      return
   

   print(f"Você vai enviar R$ {valor:.2f} para {destino['titular']}.")
   if not pedir_pin(origem):
      print("X Transferência cancelada por segurança.")
      return
   

   origem["saldo"] -= valor
   destino["saldo"] += valor
   origem["historico"].append(f"Transferência de R$ {valor:.2f} para {destino['titular']}")
   destino["historico"].append(f"Transferência recebida de R$ {valor:.2f} de {origem['titular']}")
   print(f"Transferência feita! R$ {valor:.2f} enviados para {destino['titular']}.")


def extrato(conta):
   print(f"\n--- EXTRATO DE {conta['titular'].upper()}")
   if not conta["historico"]:
      print("Nenhum deposito ou levantamento foi feito atualmente.")
   else:
      for movimento in conta["historico"]:
         print(f". {movimento}")


   print(f"Saldo atual: R$ {conta['saldo']:.2f}")


print("--- BEM-VINDO AO PYBANK ---")
contas = carregar_contas()


if not contas:
   print("Não encontramos nenhuma conta registrada. Vamos criar a primeira!")
   conta = None
   while conta is None:
      conta = criar_conta(contas)
else:
   conta = escolher_conta(contas)
   if not pedir_pin(conta):
      print("X Acesso bloqueado por segurança.")
      raise SystemExit
   print(f"Bem vindo de volta, {conta['titular']}!")


while True:
   print(f'\nSaldo atual: R$ {conta["saldo"]:.2f}')
   print("[1] Deposito | [2] Levantar | [3] Extrato | [4] Transferir")
   opcao = input("[5] Nova conta | [6] Salvar e Sair: ")


   if opcao == "1" or opcao == "2":
      if opcao == "2" and not pedir_pin(conta):
         print("X Levantamento cancelado por segurança.")
         continue


      valor = ler_valor("Valor: R$ ")
      if valor is None:
         continue


      if opcao == "1":
         depositar(conta, valor)
      else:
         sacar(conta, valor)


   elif opcao == "3":
      extrato(conta)


   elif opcao == "4":
      transferir(contas, conta)


   elif opcao == "5":
      criar_conta(contas)


   elif opcao == "6":
      salvar_contas(contas)
      break


   else:
      print("Opção invalida. Iremos colocar novamente as 6 opcoes para selecionamento.")
