import mariadb


def conectar_banco():
    return mariadb.connect(
        host="localhost",
        port=3306,
        user="root",
        password="dbtransporte",
        database="transporte"
    )


def criar_banco():

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Tabela gestão
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gestao (
        id INT NOT NULL AUTO_INCREMENT,
        usuario VARCHAR(50)
            COLLATE utf8mb4_uca1400_as_cs
            NOT NULL UNIQUE,
        senha VARCHAR(255)
            COLLATE utf8mb4_uca1400_as_cs
            NOT NULL,
        PRIMARY KEY (id)
    )
    """)

    # Tabela aluno
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS aluno (
        id INT NOT NULL AUTO_INCREMENT,

        nome VARCHAR(100) NOT NULL,
        telefone VARCHAR(20) NOT NULL,

        cpf VARCHAR(14) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,

        usuario VARCHAR(50) 
            COLLATE utf8mb4_uca1400_as_cs       
            NOT NULL UNIQUE,
        senha VARCHAR(255) 
            COLLATE utf8mb4_uca1400_as_cs       
            NOT NULL,

        faculdade VARCHAR(100) NOT NULL,
        curso VARCHAR(100) NOT NULL,

        rota ENUM('trindade', 'goiania') NOT NULL,

        posicao_fila INT,

        status ENUM('Em espera', 'Ativo', 'Inativo')
            DEFAULT 'Em espera',

        PRIMARY KEY (id)
    )
    """)

    # Tabela documento
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documento (
    id INT NOT NULL AUTO_INCREMENT,

    aluno_id INT NOT NULL,

    tipo_documento ENUM(
        'foto_perfil',
        'rg_frente',
        'rg_verso',
        'comprovante_endereco',
        'comprovante_matricula'
    ) NOT NULL,

    nome_arquivo VARCHAR(255) NOT NULL,

    PRIMARY KEY (id),

    CONSTRAINT fk_documento_aluno
        FOREIGN KEY (aluno_id)
        REFERENCES aluno(id)
        ON DELETE CASCADE
)
    """)

    # Índice para melhorar buscas da fila
    cursor.execute("""
    CREATE INDEX idx_fila
    ON aluno (rota, posicao_fila)
    """)

    # Verifica se já existe administrador
    cursor.execute("""
    SELECT id
    FROM gestao
    WHERE usuario = %s
    """, ('admin',))

    admin = cursor.fetchone()

    if not admin:

        cursor.execute("""
        INSERT INTO gestao (usuario, senha)
        VALUES (%s, %s)
        """, ('admin', '1234'))

    conexao.commit()
    conexao.close()


if __name__ == '__main__':
    criar_banco()