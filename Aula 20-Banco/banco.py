import json

def carregar_conta():
   
   try:

      with open("conta.json", "r", encoding="utf-8") as f:
         return json.load(f)
   except FileNotFoundError:
      return None

def salvar_conta(conta):
   try:

      with open("conta.json", "w", encoding="utf-8") as f:
         json.dump(conta, f, ensure_ascii=False, indent=2)
      print("Conta guardada com sucesso!")
   except Exception as e:
      print(f"Erro ao guardar: {e}")

def depositar(conta, valor):
   if valor <= 0:
      print("O valor do deposito deve ser positivo.")
      return
   conta["saldo"] += valor
   conta["historico"].append(f"Deposito de R$ {valor:.2f}")
   print(f"Deposito realizado. Saldo atual: R$ {conta['saldo']:.2f}")

def sacar(conta, valor):
   if valor <= 0:
      print("X O valor do levantamento deve ser positivo.")
      return
   if valor > conta["saldo"]:
      print("X Saldo insuficiente para este levantamento.")
      return
   conta["saldo"] -= valor
   conta["historico"].append(f"Levantamento de R$ {valor:.2f}")
   print(f"Levantamento realizado. Saldo atual: R$ {conta['saldo']:.2f}")


def extrato(conta):
   print(f"\n--- EXTRATO DE {conta['titular'].upper()}")
   if not conta["historico"]:
      print("Nenhuma movimentação ainda.")
   else:
      for movimento in conta["historico"]:
         print(f". {movimento}")

   print(f"Saldo atual: R$ {conta['saldo']:.2f}")


print("--- BEM-VINDO AO PYBANK ---")
conta = carregar_conta()

if conta is None:
   nome_input = input("Não encontramos nenhuma conta. Qual seu nome? ")
   conta = {
      "titular": "Daniel",
      "cpf_rg": "8790",
      "celular": "15997462847",
      "email": "dd@gamil.com",
      "idade": "18",
      "estado_civil": "Solteiro",
      "agencia": "002",
      "conta": "1738.9568-1",
      "saldo": 1.00,
      "historico": []
   }
else:
   print(f"Bem vindo de volta, {conta['titular']}!")

while True:
   print(f'\nSaldo atual: R$ {conta["saldo"]:.2f}')
   opcao = input("[1] Depositar | [2] Levantar | [3] Extrato | [4] Guardar e Sair: ")

   if opcao == "1" or opcao == "2":
      try:
         valor = float(input("Valor: R$ "))
      except ValueError:
         print("Digite um numero valido.")
         continue

      if opcao == "1":
         depositar(conta, valor)
      else:
         sacar(conta, valor)

   elif opcao == "3":
      extrato(conta)

   elif opcao == "4":
      salvar_conta(conta)
      break

   else:
      print("Opção invalida.")