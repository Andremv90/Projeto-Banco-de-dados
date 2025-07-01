CREATE DATABASE IF NOT EXISTS webDriverDataBase;
USE webDriverDataBase;


CREATE TABLE IF NOT EXISTS Plano (
    id_plano INT AUTO_INCREMENT PRIMARY KEY,
    nome_plano VARCHAR(50) NOT NULL,
    duracao_plano DATE NOT NULL,
    data_aquisicao DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Instituicao (
    id_instituicao INT AUTO_INCREMENT PRIMARY KEY,
    nome_instituicao VARCHAR(50) NOT NULL,
    causa_social TEXT NOT NULL,
    endereco_instituicao TEXT NOT NULL,
    id_plano INT,
    FOREIGN KEY (id_plano) REFERENCES Plano(id_plano)
);

CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    login_usuario VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL,
    senha VARCHAR(25) NOT NULL,
    data_ingressao DATE NOT NULL,
    id_instituicao INT,
    FOREIGN KEY (id_instituicao) REFERENCES Instituicao(id_instituicao)
);

CREATE TABLE IF NOT EXISTS Administrador (
    id_administrador INT PRIMARY KEY,
    FOREIGN KEY (id_administrador) REFERENCES Usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS Arquivo (
    id_arquivo INT AUTO_INCREMENT PRIMARY KEY,
    nome_arquivo VARCHAR(50) NOT NULL,
    localizacao TEXT NOT NULL,
    permissao_de_acesso VARCHAR(25) NOT NULL,
    tamanho INT NOT NULL,
    data_ultima_atualizacao DATE NOT NULL,
    tipo VARCHAR(25) NOT NULL,
    URL_arquivo TEXT NOT NULL,
    id_dono INT,
    FOREIGN KEY (id_dono) REFERENCES Usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS Compartilhamento (
    id_arquivo INT,
    id_dono INT,
    id_compartilhado INT,
    data_compartilhamento DATE,
    PRIMARY KEY (id_arquivo, id_compartilhado),
    FOREIGN KEY (id_arquivo) REFERENCES Arquivo(id_arquivo),
    FOREIGN KEY (id_dono) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_compartilhado) REFERENCES Usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS Comentario (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    conteudo TEXT NOT NULL,
    data_comentario DATE NOT NULL,
    hora_comentario TIME NOT NULL,
    id_usuario INT,
    id_arquivo INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_arquivo) REFERENCES Arquivo(id_arquivo)
);

CREATE TABLE IF NOT EXISTS Historico (
    id_historico INT AUTO_INCREMENT PRIMARY KEY,
    data_historico DATE NOT NULL,
    hora_historico TIME NOT NULL,
    operacao VARCHAR(25) NOT NULL,
    conteudo_mudado TEXT NOT NULL,
    id_usuario INT,
    id_arquivo INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_arquivo) REFERENCES Arquivo(id_arquivo)
);

CREATE TABLE IF NOT EXISTS Suporte (
    id_suporte INT AUTO_INCREMENT PRIMARY KEY,
    dia DATE NOT NULL,
    hora TIME NOT NULL,
    descricao TEXT NOT NULL,
    id_usuario INT,
    id_arquivo INT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_arquivo) REFERENCES Arquivo(id_arquivo)
);

CREATE TABLE IF NOT EXISTS Atividades_Recentes (
    id_arquivo INT PRIMARY KEY,
    ultima_versao DATE NOT NULL,
    acesso ENUM('prioritário', 'não prioritário') NOT NULL,
    FOREIGN KEY (id_arquivo) REFERENCES Arquivo(id_arquivo)
);

-- Procedures, Funções e Triggers

DELIMITER $$

CREATE PROCEDURE Verificar_atividades()
BEGIN
    UPDATE Atividades_Recentes SET ultima_versao = CURRENT_DATE;
END$$

CREATE PROCEDURE Conta_usuarios(IN arquivo_id INT)
BEGIN
    SELECT COUNT(DISTINCT id_compartilhado)
    FROM Compartilhamento
    WHERE id_arquivo = arquivo_id;
END$$

CREATE PROCEDURE Chavear(IN arquivo_id INT)
BEGIN
    UPDATE Atividades_Recentes
    SET acesso = CASE
        WHEN acesso = 'prioritário' THEN 'não prioritário'
        ELSE 'prioritário'
    END
    WHERE id_arquivo = arquivo_id;
END$$

CREATE PROCEDURE Remover_acessos(IN arquivo_id INT)
BEGIN
    DELETE FROM Compartilhamento
    WHERE id_arquivo = arquivo_id
    AND id_compartilhado != (
        SELECT id_dono FROM Arquivo WHERE id_arquivo = arquivo_id
    );
END$$

CREATE FUNCTION Verifica_alteracao(arquivo_id INT)
RETURNS BOOLEAN
DETERMINISTIC
BEGIN
    DECLARE ultima DATE;
    SELECT data_ultima_atualizacao INTO ultima
    FROM Arquivo
    WHERE id_arquivo = arquivo_id;

    RETURN DATEDIFF(CURDATE(), ultima) > 100;
END$$

-- Triggers

CREATE TRIGGER Safe_security
BEFORE INSERT ON Arquivo
FOR EACH ROW
BEGIN
    IF NEW.tipo = 'exe' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Arquivos executáveis não são permitidos.';
    END IF;
END$$

CREATE TRIGGER Registrar_operacao
AFTER INSERT ON Historico
FOR EACH ROW
BEGIN
    UPDATE Atividades_Recentes
    SET ultima_versao = NEW.data_historico
    WHERE id_arquivo = NEW.id_arquivo;
END$$

CREATE TRIGGER Atualizar_acesso
AFTER INSERT ON Compartilhamento
FOR EACH ROW
BEGIN
    INSERT IGNORE INTO Atividades_Recentes (id_arquivo, ultima_versao, acesso)
    VALUES (NEW.id_arquivo, CURDATE(), 'não prioritário');
END$$

DELIMITER ;