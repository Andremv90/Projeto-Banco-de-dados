from conectar import ligar

class Usuario:
    def __init__(self, id_usuario):
        self.id = id_usuario

    def listar_arquivos(self):
        conn = ligar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nome_arquivo, tipo, URL_arquivo
            FROM Arquivo
            WHERE id_dono = %s
        """, (self.id,))
        arquivos = cursor.fetchall()
        conn.close()
        return arquivos

    def inserir_arquivo(self, nome, local, tipo, url, permissao, tamanho):
        if permissao.lower() != "privado":
            print(" Usuários só podem criar arquivos com permissão 'privado'.")
            return

        conn = ligar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Arquivo (nome_arquivo, localizacao, permissao_de_acesso,
                                 tamanho, data_ultima_atualizacao, tipo, URL_arquivo, id_dono)
            VALUES (%s, %s, %s, %s, CURDATE(), %s, %s, %s)
        """, (nome, local, permissao, tamanho, tipo, url, self.id))
        conn.commit()
        conn.close()
        print(" Arquivo inserido com sucesso.")

    def atualizar_arquivo(self, url_arquivo):
        conn = ligar()
        cursor = conn.cursor()

        cursor.execute("SELECT id_arquivo FROM Arquivo WHERE URL_arquivo = %s AND id_dono = %s",
                       (url_arquivo, self.id))
        resultado = cursor.fetchone()

        if not resultado:
            print(" Arquivo não encontrado ou não pertence a você.")
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
            print(" Opção inválida.")
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
        print(" Arquivo atualizado com sucesso.")

    def adicionar_comentario(self, url_arquivo):
        conn = ligar()
        cursor = conn.cursor()

        cursor.execute("SELECT id_arquivo FROM Arquivo WHERE URL_arquivo = %s AND id_dono = %s",
                       (url_arquivo, self.id))
        resultado = cursor.fetchone()

        if not resultado:
            print(" Arquivo não encontrado ou não pertence a você.")
            conn.close()
            return

        id_arquivo = resultado[0]
        conteudo = input("Digite seu comentário: ")

        cursor.execute("""
            INSERT INTO Comentario (conteudo, data_comentario, hora_comentario, id_usuario, id_arquivo)
            VALUES (%s, CURDATE(), CURTIME(), %s, %s)
        """, (conteudo, self.id, id_arquivo))

        conn.commit()
        conn.close()
        print(" Comentário adicionado.")

    def compartilhar_arquivo(self, url_arquivo):
        conn = ligar()
        cursor = conn.cursor()

        cursor.execute("SELECT id_arquivo FROM Arquivo WHERE URL_arquivo = %s AND id_dono = %s",
                       (url_arquivo, self.id))
        resultado = cursor.fetchone()

        if not resultado:
            print(" Arquivo não encontrado ou não pertence a você.")
            conn.close()
            return

        id_arquivo = resultado[0]
        id_compartilhado = int(input("Digite o ID do usuário para compartilhar: "))

        cursor.execute("""
            INSERT INTO Compartilhamento (id_arquivo, id_dono, id_compartilhado, data_compartilhamento)
            VALUES (%s, %s, %s, CURDATE())
        """, (id_arquivo, self.id, id_compartilhado))

        conn.commit()
        conn.close()
        print(" Arquivo compartilhado com sucesso.")

    def abrir_suporte(self):
        conn = ligar()
        cursor = conn.cursor()

        url = input("Digite a URL do arquivo (ou pressione Enter se não houver): ")

        id_arquivo = None
        if url:
            cursor.execute("SELECT id_arquivo FROM Arquivo WHERE URL_arquivo = %s AND id_dono = %s",
                           (url, self.id))
            resultado = cursor.fetchone()
            if resultado:
                id_arquivo = resultado[0]
            else:
                print(" Arquivo não encontrado ou não pertence a você.")
                conn.close()
                return

        descricao = input("Descreva seu problema: ")

        cursor.execute("""
            INSERT INTO Suporte (dia, hora, descricao, id_usuario, id_arquivo)
            VALUES (CURDATE(), CURTIME(), %s, %s, %s)
        """, (descricao, self.id, id_arquivo))

        conn.commit()
        conn.close()
        print(" Suporte registrado.")