from usuario import Usuario
from empresa import Empresa
from administrador import Administrador
from conectar import ligar
from plano import Plano
import mysql.connector


def menu_usuario(id_usuario):
    usuario = Usuario(id_usuario)

    while True:
        print("\n=== MENU USUÁRIO ===")
        print("[1] Ver meus arquivos")
        print("[2] Inserir novo arquivo")
        print("[3] Atualizar meu arquivo")
        print("[4] Adicionar comentário")
        print("[5] Compartilhar arquivo")
        print("[6] Abrir suporte")
        print("[0] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            arquivos = usuario.listar_arquivos()
            if arquivos:
                for arq in arquivos:
                    print(f"Arquivo: {arq[0]} | Tipo: {arq[1]} | URL: {arq[2]}")
            else:
                print("Nenhum arquivo encontrado.")

        elif opcao == "2":
            nome = input("Nome do arquivo: ")
            local = input("Localização: ")
            tipo = input("Tipo do arquivo: ")
            url = input("URL: ")
            permissao = "privado"
            tamanho = int(input("Tamanho (em bytes): "))
            usuario.inserir_arquivo(nome, local, tipo, url, permissao, tamanho)

        elif opcao == "3":
            url = input("Digite a URL do arquivo que deseja atualizar: ")
            usuario.atualizar_arquivo(url)

        elif opcao == "4":
            url = input("Digite a URL do arquivo para comentar: ")
            usuario.adicionar_comentario(url)

        elif opcao == "5":
            url = input("Digite a URL do arquivo para compartilhar: ")
            usuario.compartilhar_arquivo(url)

        elif opcao == "6":
            usuario.abrir_suporte()

        elif opcao == "0":
            print("Saindo do menu usuário...")
            break

        else:
            print(" Opção inválida.")


def menu_empresa(conexao):
    empresa = Empresa(conexao)

    while True:
        print("\n=== MENU EMPRESA ===")
        print("[1] Listar arquivos dos funcionários")
        print("[0] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            empresa.listar_arquivos_dos_funcionarios()

        elif opcao == "0":
            print("Saindo do menu empresa...")
            break

        else:
            print(" Opção inválida.")


def menu_admin():
    admin = Administrador()

    while True:
        print("\n=== MENU ADMINISTRADOR ===")
        print("[1] Listar todos os arquivos")
        print("[2] Inserir novo arquivo")
        print("[3] Atualizar um arquivo")
        print("[4] Deletar um arquivo")
        print("[0] Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            arquivos = admin.listar_tudo()
            if arquivos:
                for arq in arquivos:
                    print(f"Arquivo: {arq[0]} | Tipo: {arq[1]} | URL: {arq[2]}")
            else:
                print("Nenhum arquivo encontrado.")

        elif opcao == "2":
            nome = input("Nome: ")
            local = input("Localização: ")
            tipo = input("Tipo: ")
            url = input("URL: ")
            permissao = input("Permissão: ")
            tamanho = int(input("Tamanho (em bytes): "))
            dono = int(input("ID do dono do arquivo: "))
            admin.inserir_arquivo(nome, local, tipo, url, permissao, tamanho, dono)

        elif opcao == "3":
            url = input("Digite a URL do arquivo que deseja atualizar: ")
            admin.atualizar_arquivo(url)

        elif opcao == "4":
            id_arquivo = int(input("Digite o ID do arquivo para deletar: "))
            admin.deletar_arquivo(id_arquivo)

        elif opcao == "0":
            print("Saindo do menu administrador...")
            break

        else:
            print(" Opção inválida.")


def cadastrar_usuario():
    print("\n=== Cadastro de novo usuário ===")
    login = input("Login: ")
    email = input("Email: ")
    senha = input("Senha: ")

    conn = ligar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Usuario (login_usuario, email, senha, data_ingressao)
        VALUES (%s, %s, %s, CURDATE())
    """, (login, email, senha))
    conn.commit()

    cursor.execute("SELECT LAST_INSERT_ID()")
    id_usuario = cursor.fetchone()[0]

    conn.close()
    print(f" Usuário cadastrado com sucesso! Seu ID é: {id_usuario}")
    return id_usuario


def main():
    print("=== SISTEMA WEB DRIVER ===")
    papel = input("Digite seu papel (usuario, empresa, admin): ").strip().lower()

    if papel == "usuario":
        resposta = input("Você já está cadastrado? (s/n): ").strip().lower()

        if resposta == "s":
            try:
                id_usuario = int(input("Digite seu ID de usuário: "))
                menu_usuario(id_usuario)
            except ValueError:
                print(" ID inválido.")
        elif resposta == "n":
            id_usuario = cadastrar_usuario()
            menu_usuario(id_usuario)
        else:
            print(" Resposta inválida.")

    elif papel == "empresa":
        conexao = ligar()
        menu_empresa(conexao)

    elif papel == "admin":
        menu_admin()

    else:
        print(" Papel inválido.")


if __name__ == "__main__":
    main()
