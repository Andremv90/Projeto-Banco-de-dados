import mysql.connector

class Plano:
    def __init__(self, conexao):
        self.conexao = conexao

    def criar_plano(self, id_empresa):
        nome = input("Nome do plano: ")
        preco = float(input("Preço do plano: "))

        cursor = self.conexao.cursor()
        try:
            cursor.execute("INSERT INTO plano (nome, preco, empresa_id) VALUES (%s, %s, %s)",
                           (nome, preco, id_empresa))
            self.conexao.commit()
            print(" Plano criado com sucesso!")
        except mysql.connector.Error as err:
            print(f" Erro ao criar plano: {err}")
        finally:
            cursor.close()

    def listar_planos_empresa(self, id_empresa):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("SELECT nome, preco FROM plano WHERE empresa_id = %s", (id_empresa,))
            planos = cursor.fetchall()
            if not planos:
                print("Nenhum plano cadastrado.")
                return
            for plano in planos:
                print(f"Plano: {plano[0]} | Preço: R$ {plano[1]}")
        except mysql.connector.Error as err:
            print(f"Erro ao listar planos: {err}")
        finally:
            cursor.close()
