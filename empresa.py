from plano import Plano

class Empresa:
    def __init__(self, conexao):
        self.conexao = conexao
        self.plano = Plano(conexao)

    def listar_arquivos_dos_funcionarios(self):
        cursor = self.conexao.cursor()
        try:
            cursor.execute("""
                SELECT nome_arquivo, tipo, URL_arquivo, U.login_usuario
                FROM Arquivo A
                JOIN Usuario U ON A.id_dono = U.id_usuario
            """)
            arquivos = cursor.fetchall()
            if arquivos:
                for arq in arquivos:
                    print(f"Arquivo: {arq[0]} | Tipo: {arq[1]} | URL: {arq[2]} | Dono: {arq[3]}")
            else:
                print("Nenhum arquivo encontrado.")
        except Exception as err:
            print(f"Erro: {err}")
        finally:
            cursor.close()
