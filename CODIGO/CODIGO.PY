import json
import os
from time import sleep
from datetime import datetime


#   CORES PARA TERMINAL (ANSI)

class Cor:
    RESET = '\033[0m'
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    ROXO = '\033[95m'
    CIANO = '\033[96m'



#   MODELO DE USUÁRIO

class Usuario:
    """Representa um usuário com nome, idade e data de cadastro."""

    def __init__(self, nome, idade):
        self.nome = nome.strip().title()
        self.idade = int(idade)
        self.data_cadastro = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    def to_dict(self):
        return {
            "nome": self.nome,
            "idade": self.idade,
            "data_cadastro": self.data_cadastro
        }



#   GERENCIADOR DE USUÁRIOS (BANCO DE DADOS JSON)

class GerenciadorUsuarios:
    """Controla operações de CRUD sobre um arquivo JSON."""

    def __init__(self):
        self.arquivo = os.path.join(os.path.dirname(__file__), 'usuarios.json')
        if not os.path.exists(self.arquivo):
            with open(self.arquivo, 'w') as f:
                json.dump([], f)

    def carregar(self):
        with open(self.arquivo, 'r') as f:
            return json.load(f)

    def salvar(self, dados):
        with open(self.arquivo, 'w') as f:
            json.dump(dados, f, indent=4)

    def adicionar_usuario(self, nome, idade):
        usuarios = self.carregar()
        novo = Usuario(nome, idade).to_dict()
        usuarios.append(novo)
        self.salvar(usuarios)
        print(Cor.VERDE + "✔ Usuário cadastrado com sucesso!" + Cor.RESET)

    def listar(self):
        usuarios = self.carregar()
        if not usuarios:
            print(Cor.AMARELO + "⚠ Nenhum usuário cadastrado." + Cor.RESET)
            return

        print(Cor.AZUL + "\n===== LISTA DE USUÁRIOS =====" + Cor.RESET)
        for u in usuarios:
            print(f"• Nome: {u['nome']} | Idade: {u['idade']} | Cadastro: {u['data_cadastro']}")
        print(Cor.AZUL + "=" * 33 + Cor.RESET)

    def buscar(self, nome):
        usuarios = self.carregar()
        encontrados = [u for u in usuarios if nome.lower() in u['nome'].lower()]

        if encontrados:
            print(Cor.ROXO + f"\n🔎 Usuários encontrados ({len(encontrados)}):" + Cor.RESET)
            for u in encontrados:
                print(f"• {u['nome']} ({u['idade']} anos)")
        else:
            print(Cor.VERMELHO + "❌ Nenhum usuário encontrado com esse nome." + Cor.RESET)

    def atualizar(self, nome_antigo, novo_nome, nova_idade):
        usuarios = self.carregar()
        for u in usuarios:
            if u['nome'].lower() == nome_antigo.lower():
            #Atualiza
                u['nome'] = novo_nome.strip().title()
                u['idade'] = int(nova_idade)
                u['atualizado_em'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                self.salvar(usuarios)
                print(Cor.VERDE + "✔ Usuário atualizado!" + Cor.RESET)
                return
        print(Cor.VERMELHO + "❌ Usuário não encontrado." + Cor.RESET)

    def excluir(self, nome):
        usuarios = self.carregar()
        novos = [u for u in usuarios if u['nome'].lower() != nome.lower()]

        if len(novos) == len(usuarios):
            print(Cor.VERMELHO + "❌ Usuário não encontrado." + Cor.RESET)
            return

        self.salvar(novos)
        print(Cor.AMARELO + "🗑 Usuário removido!" + Cor.RESET)

    def total(self):
        qtd = len(self.carregar())
        print(Cor.CIANO + f"\n📊 Total de usuários cadastrados: {qtd}" + Cor.RESET)



#   MENU PRINCIPAL

def menu():
    print(Cor.AZUL + """
===============================
        MENU PRINCIPAL
===============================
1 — Adicionar Usuário
2 — Listar Usuários
3 — Buscar Usuário
4 — Atualizar Usuário
5 — Excluir Usuário
6 — Total de Usuários
7 — Sair
""" + Cor.RESET)


def main():
    ger = GerenciadorUsuarios()

    while True:
        menu()
        opcao = input("👉 Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            idade = input("Idade: ")
            ger.adicionar_usuario(nome, idade)

        elif opcao == "2":
            ger.listar()

        elif opcao == "3":
            nome = input("Nome para buscar: ")
            ger.buscar(nome)

        elif opcao == "4":
            antigo = input("Nome a atualizar: ")
            novo = input("Novo nome: ")
            idade = input("Nova idade: ")
            ger.atualizar(antigo, novo, idade)

        elif opcao == "5":
            nome = input("Nome a excluir: ")
            ger.excluir(nome)

        elif opcao == "6":
            ger.total()

        elif opcao == "7":
            print(Cor.AMARELO + "Saindo..." + Cor.RESET)
            sleep(1)
            break

        else:
            print(Cor.VERMELHO + "❌ Opção inválida!" + Cor.RESET)


if __name__ == "__main__":
    main()
