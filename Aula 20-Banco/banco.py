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
      print("Conta salva com sucesso!")
   except Exception as e:
      print(f"Erro ao salvar conta: {e}")

def depositar(conta, valor):
   if valor <= 0:
      print("O valor do deposito não pode ser negativo,por favor não insista.")
      return
   conta["saldo"] += valor
   conta["historico"].append(f"Deposito em sua conta de R$ {valor:.2f}")
   print(f"Deposito realizado com sucesso. Saldo atualmente: R$ {conta['saldo']:.2f}")

def sacar(conta, valor):
   if valor <= 0:
      print("X O valor do levantamento deve ser positivo.")
      return
   if valor > conta["saldo"]:
      print("X O seu saldo e insuficiente para este levantamento.")
      return
   conta["saldo"] -= valor
   conta["historico"].append(f"Levantamento de R$ {valor:.2f}")
   print(f"Levantamento realizado com sucesso. Saldo atual: R$ {conta['saldo']:.2f}")


def extrato(conta):
   print(f"\n--- EXTRATO DE {conta['titular'].upper()}")
   if not conta["historico"]:
      print("Nenhuma deposito ou levantamento foi feito atualmente.")
   else:
      for movimento in conta["historico"]:
         print(f". {movimento}")

   print(f"Saldo atual: R$ {conta['saldo']:.2f}")


print("--- BEM-VINDO AO PYBANK ---")
conta = carregar_conta()

if conta is None:
   nome_input = input("Não encontramos nenhuma conta registrada. Poderia nos dizer qual e o nome de sua conta? ")
   conta = {
      "titular": "Derricko",
      "senha": "9888",
      "cpf_rg": "4280",
      "celular": "15998562827",
      "email": "De4r1ck0@gmail.com",
      "idade": "18",
      "estado_civil": "Solteiro",
      "agencia": "088",
      "conta": "1278.9508-2",
      "saldo": 0.00,
      "historico": []
   }
else:
   print(f"Bem vindo de volta, Sr.{conta['titular']}!")

while True:
   print(f'\nSaldo atual: R$ {conta["saldo"]:.2f}')
   opcao = input("[1] Deposito | [2] Levantar | [3] Extrato | [4] Salvar e Sair: ")

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
      print("Opção invalida. Iremos colocar novamente as 4 opcoes para selecionamento.")
