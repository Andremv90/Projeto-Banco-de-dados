from conectar import ligar

class Administrador:
    def listar_tudo(self):
        conn = ligar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome_arquivo, tipo, URL_arquivo FROM Arquivo")
        arquivos = cursor.fetchall()
        conn.close()
        return arquivos

    def inserir_arquivo(self, nome, local, tipo, url, permissao, tamanho, dono):
        conn = ligar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Arquivo (nome_arquivo, localizacao, permissao_de_acesso,
                                 tamanho, data_ultima_atualizacao, tipo, URL_arquivo, id_dono)
            VALUES (%s, %s, %s, %s, CURDATE(), %s, %s, %s)
        """, (nome, local, permissao, tamanho, tipo, url, dono))
        conn.commit()
        conn.close()

    def atualizar_arquivo(self, url_arquivo):
        conn = ligar()
        cursor = conn.cursor()

        cursor.execute("SELECT id_arquivo FROM Arquivo WHERE URL_arquivo = %s", (url_arquivo,))
        resultado = cursor.fetchone()

        if not resultado:
            print("Arquivo não encontrado.")
            conn.close()
            return

        id_arquivo = resultado[0]

        print("\nO que deseja atualizar?")
        print("1. Nome")
        print("2. Localização")
        print("3. URL")
        print("4. Tipo")
        print("5. Tamanho")
        opcao = input("Escolha uma opção (1-5): ")

        campos = {
            "1": "nome_arquivo",
            "2": "localizacao",
            "3": "URL_arquivo",
            "4": "tipo",
            "5": "tamanho"
        }

        if opcao not in campos:
            print("Opção inválida.")
            conn.close()
            return

        novo_valor = input(f"Digite o novo valor para {campos[opcao]}: ")

        sql = f"""
            UPDATE Arquivo
            SET {campos[opcao]} = %s, data_ultima_atualizacao = CURDATE()
            WHERE id_arquivo = %s
        """
        cursor.execute(sql, (novo_valor, id_arquivo))
        conn.commit()
        conn.close()
        print("Arquivo atualizado com sucesso.")

    def deletar_arquivo(self, id_arquivo):
        conn = ligar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Arquivo WHERE id_arquivo = %s", (id_arquivo,))
        conn.commit()
        conn.close()
        print("Arquivo deletado com sucesso.")
