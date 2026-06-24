from flask import Flask, request, render_template, redirect, url_for, send_file, session
import banco
import mariadb
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import shutil


app = Flask(__name__)

app.secret_key = 'Gk9!@2xLp3#mZ8$qW1_vY5&tX7*rB4+a'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

print(app.config["UPLOAD_FOLDER"])

os.makedirs('uploads', exist_ok=True)

load_dotenv()

# CONEXÃO COM O BANCO DE DADOS
def conectar_banco():
    return mariadb.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def salvar_arquivo(arquivo, nome_arquivo, aluno_id):

    pasta_aluno = os.path.join(
        app.config["UPLOAD_FOLDER"],
        f"aluno_{aluno_id}"
    )

    print(f"Pasta do aluno: {pasta_aluno}")
    print(f"Arquivo recebido: {arquivo.filename}")

    os.makedirs(pasta_aluno, exist_ok=True)

    extensao = os.path.splitext(
        secure_filename(arquivo.filename)
    )[1].lower()

    print(f"Extensão: {extensao}")

    nome_final = f"{nome_arquivo}{extensao}"
    caminho = os.path.join(pasta_aluno, nome_final)

    print(f"Salvando em: {caminho}")

    arquivo.save(caminho)

    print(f"Salvo com sucesso!")

    return nome_final

def atualizar_documento(aluno_id, tipo_documento, arquivo):

    if not arquivo or arquivo.filename == "":
        return

    pasta_aluno = os.path.join(
        app.config["UPLOAD_FOLDER"],
        f"aluno_{aluno_id}"
    )

    extensao = os.path.splitext(
        secure_filename(arquivo.filename)
    )[1].lower()

    nome_arquivo = f"{tipo_documento}{extensao}"

    caminho = os.path.join(
        pasta_aluno,
        nome_arquivo
    )

    # apagar versões antigas

    if not os.path.exists(pasta_aluno):
        os.makedirs(pasta_aluno, exist_ok=True)

    for arquivo_existente in os.listdir(pasta_aluno):

        if arquivo_existente.startswith(tipo_documento):

            os.remove(
                os.path.join(
                    pasta_aluno,
                    arquivo_existente
                )
            )

    arquivo.save(caminho)

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE documento
        SET nome_arquivo = %s
        WHERE aluno_id = %s
        AND tipo_documento = %s
    """,
    (
        nome_arquivo,
        aluno_id,
        tipo_documento
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

def executar_select(query, params=None):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(query, params or ())
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultado

def executar_write(query, params=None):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(query, params or ())
    conexao.commit()

    cursor.close()
    conexao.close()

# ROTA DA TELA PRINCIPAL
@app.route('/', methods=['GET', 'POST'])
def tela_principal():

    mensagem = None

    if request.method == 'POST':

        tipo_login = request.form.get('login_tipo')

        # LOGIN GESTÃO
        if tipo_login == 'gestao':

            usuario = request.form.get('user')
            senha = request.form.get('senha')

            conexao = conectar_banco()
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT usuario, senha
                FROM gestao
                WHERE usuario = %s AND senha = %s
            """, (usuario, senha))

            dados_verificacao = cursor.fetchone()


            if dados_verificacao:
                session['usuario'] = usuario
                session['tipo'] = 'gestao'
                return redirect(url_for('admin'))
            
            else:
                mensagem = "Informações não encontradas!"

            conexao.close()

        # LOGIN ALUNO
        elif tipo_login == 'aluno':

            usuario = request.form.get('user')
            senha = request.form.get('senha')

            conexao = conectar_banco()
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT usuario, senha
                FROM aluno
                WHERE usuario = %s AND senha = %s
            """, (usuario, senha))

            dados_verificacao = cursor.fetchone()


            if dados_verificacao:
                session['usuario'] = usuario
                session['tipo'] = 'aluno'
                return redirect(url_for('tela_aluno'))
            
            else:
                mensagem = "Informações não encontradas!"

            conexao.close()
    return render_template('login.html', resultado=mensagem)

# ROTA CADASTRO DE ALUNO
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():

    if request.method == 'POST':

        nome = request.form.get('nome')
        user = request.form.get('user')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        senha = request.form.get('senha')
        faculdade = request.form.get('faculdade')
        curso = request.form.get('curso')
        rota = request.form.get('rota')

        conexao = conectar_banco()
        cursor = conexao.cursor()

        cursor.execute("""
            INSERT INTO aluno
            (
                nome,
                usuario,
                telefone,
                cpf,
                email,
                senha,
                faculdade,
                curso,
                rota
            )
            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """, (
            nome,
            user,
            telefone,
            cpf,
            email,
            senha,
            faculdade,
            curso,
            rota
        ))

        conexao.commit()
        aluno_id = cursor.lastrowid
        foto_perfil = request.files["ft_perfil"]
        rg_frente = request.files["rg_frente"]
        rg_verso = request.files["rg_verso"]
        comprovante_endereco = request.files["comprovante_endereco"]
        comprovante_matricula = request.files["comprovante_matricula"]

        arquivo_foto = salvar_arquivo(
            foto_perfil,
            "foto_perfil",
            aluno_id
            )

        arquivo_rg_frente = salvar_arquivo(
            rg_frente,
            "rg_frente",
            aluno_id
        )

        arquivo_rg_verso = salvar_arquivo(
            rg_verso,
            "rg_verso",
            aluno_id
        )

        arquivo_endereco = salvar_arquivo(
            comprovante_endereco,
            "comprovante_endereco",
            aluno_id
        )

        arquivo_matricula = salvar_arquivo(
            comprovante_matricula,
            "comprovante_matricula",
            aluno_id
        )

        

        documentos = [
            ("foto_perfil", arquivo_foto),

            ("rg_frente", arquivo_rg_frente),

            ("rg_verso", arquivo_rg_verso),

            ("comprovante_endereco", arquivo_endereco),

            ("comprovante_matricula", arquivo_matricula)

        ]

        for tipo, arquivo in documentos:

            cursor.execute("""
                INSERT INTO documento
                (
                    aluno_id,
                    tipo_documento,
                    nome_arquivo
                )
                VALUES
                (
                    %s,%s,%s
                )
            """,
            (
                aluno_id,
                tipo,
                os.path.basename(arquivo)
            ))

        conexao.commit()
        conexao.close()

        return redirect(url_for('tela_principal'))

    return render_template('cadastro.html')

@app.route('/cadastro_admin', methods=['POST'])
def cadastrar_admin():

    if session.get('tipo') != 'gestao':
        return redirect(url_for('tela_principal'))

    nome     = request.form.get('nome')
    user     = request.form.get('user')
    telefone = request.form.get('telefone')
    cpf      = request.form.get('cpf')
    email    = request.form.get('email')
    senha    = request.form.get('senha')
    faculdade = request.form.get('faculdade')
    curso    = request.form.get('curso')
    rota     = request.form.get('rota')

    conexao = conectar_banco()
    cursor  = conexao.cursor()

    cursor.execute("""
        INSERT INTO aluno
        (nome, usuario, telefone, cpf, email, senha, faculdade, curso, rota, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Ativo')
    """, (nome, user, telefone, cpf, email, senha, faculdade, curso, rota))

    conexao.commit()
    aluno_id = cursor.lastrowid
    conexao.close()

    documentos = {
        "foto_perfil":           request.files.get("ft_perfil"),
        "rg_frente":             request.files.get("rg_frente"),
        "rg_verso":              request.files.get("rg_verso"),
        "comprovante_endereco":  request.files.get("comprovante_endereco"),
        "comprovante_matricula": request.files.get("comprovante_matricula"),
    }

    conexao = conectar_banco()
    cursor  = conexao.cursor()

    for tipo, arquivo in documentos.items():
        if arquivo and arquivo.filename != "":
            nome_arquivo = salvar_arquivo(arquivo, tipo, aluno_id)
            cursor.execute("""
                INSERT INTO documento (aluno_id, tipo_documento, nome_arquivo)
                VALUES (%s, %s, %s)
            """, (aluno_id, tipo, nome_arquivo))

    conexao.commit()
    conexao.close()

    return redirect(url_for('admin'))

def buscar_alunos_por_rota(rota):
    return executar_select("""
        SELECT * FROM aluno
        WHERE rota = %s AND status = 'Ativo'
    """, (rota,))

def buscar_alunos_por_status(status):
    return executar_select("""
        SELECT * FROM aluno
        WHERE status = %s
    """, (status,))

# ROTA DA PÁGINA DO ALUNO
@app.route('/aluno')
def tela_aluno():

    if 'usuario' not in session:
        return redirect(url_for('tela_principal'))

    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Busca dados do aluno logado
    cursor.execute("""
        SELECT *
        FROM aluno
        WHERE usuario = %s
    """, (session['usuario'],))

    dados = cursor.fetchone()
    print(dados)

    # Busca documentos do aluno
    cursor.execute("""
        SELECT tipo_documento, nome_arquivo
        FROM documento d
        JOIN aluno a ON d.aluno_id = a.id
        WHERE a.usuario = %s
    """, (session['usuario'],))

    documentos_db = cursor.fetchall()

    conexao.close()

    documentos = {}

    for tipo, arquivo in documentos_db:
        documentos[tipo] = arquivo

    # Organiza os dados em dicionário
    aluno = {
        'id': dados[0],
        'nome':       dados[1],
        'usuario':    dados[5],
        'telefone':   dados[2],
        'cpf':        dados[3],
        'email':      dados[4],
        'faculdade':  dados[7],
        'curso':      dados[8],
        'rota':       dados[9],
        'status':     dados[11],
        'comprovante_endereco': documentos.get('comprovante_endereco'),
        'comprovante_matricula': documentos.get('comprovante_matricula'),
        'foto_perfil': documentos.get('foto_perfil'),
        'rg_frente': documentos.get('rg_frente'),
        'rg_verso': documentos.get('rg_verso')
    }

    docs_espec = [
        {"tipo": aluno['comprovante_endereco'],
         "nome": "Comprovante de Endereço"
        },
        {"tipo": aluno['comprovante_matricula'],
         "nome": "Comprovante de Matrícula"
        },
        {"tipo": aluno['rg_frente'],
         "nome": "RG FRENTE"
        },
        {"tipo": aluno['rg_verso'],
         "nome": "RG VERSO"
        },
    ]

    return render_template(
        'Aluno.html',
        aluno=aluno,
        documentos = documentos,
        docs_espec = docs_espec
    )

# ROTA DA ADMINISTRAÇÃO DO SISTEMA
@app.route('/administrador', methods=['GET', 'POST'])
def admin():
    
    if session.get('tipo') != 'gestao':
        return redirect(url_for('tela_principal'))

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT aluno_id, tipo_documento, nome_arquivo FROM documento")
    rows = cursor.fetchall()

    docs_alunos = {}

    for row in rows:
        aluno_id      = row[0]
        tipo_documento = row[1]
        nome_arquivo  = row[2]

        if aluno_id not in docs_alunos:
            docs_alunos[aluno_id] = {}

        docs_alunos[aluno_id][tipo_documento] = nome_arquivo

    # Goiânia
    # cursor.execute(""" <--------------------->
    #     SELECT *
    #     FROM aluno
    #     WHERE rota = 'goiania'
    #     AND status = 'Ativo'
    # """)

    goiania = buscar_alunos_por_rota("goiania")

    cursor.execute("""
    SELECT COUNT(*)
    FROM aluno
    WHERE rota = 'goiania'
    AND status != 'Em espera'
    """)

    fora_espera_goiania = cursor.fetchone()[0]

    mostrar_mensagem_goiania = (fora_espera_goiania == 0)

    # Trindade
    # cursor.execute(""" <--------------------->
    #     SELECT *
    #     FROM aluno
    #     WHERE rota = 'trindade'
    #     AND status = 'Ativo'
    # """)

    trindade = buscar_alunos_por_rota('trindade')

    cursor.execute("""
    SELECT COUNT(*)
    FROM aluno
    WHERE rota = 'trindade'
    AND status != 'Em espera'
    """)

    fora_espera_trindade = cursor.fetchone()[0]

    mostrar_mensagem_trindade = (fora_espera_trindade == 0)

    cursor.execute("""
        SELECT
            aluno_id,
            tipo_documento
        FROM documento
    """)

    documentos = cursor.fetchall()

    documentos_alunos = {}

    for aluno_id, tipo in documentos:

        if aluno_id not in documentos_alunos:
            documentos_alunos[aluno_id] = {}

        documentos_alunos[aluno_id][tipo] = True

    cursor.execute("""
        SELECT usuario
        FROM gestao
        LIMIT 1
    """)
    admin = cursor.fetchone()

    usuario = admin[0] if admin else None

    cursor.execute("""
        SELECT DISTINCT faculdade
        FROM aluno
        WHERE rota = 'goiania'
        AND status = 'Ativo'
        ORDER BY faculdade
                """)
    faculdade_goiania = cursor.fetchall()

    cursor.execute("""
        SELECT DISTINCT faculdade
        FROM aluno
        WHERE rota = 'trindade'
        AND status = 'Ativo'
        ORDER BY faculdade
                """)
    faculdade_trindade = cursor.fetchall()


    conexao.close()



    return render_template(
        'adm.html',
        goiania=goiania,
        trindade=trindade,
        usuario=usuario,
        faculdade_goiania=faculdade_goiania,
        faculdade_trindade=faculdade_trindade,
        documentos_alunos=documentos_alunos,
        mostrar_mensagem_goiania=mostrar_mensagem_goiania,
        mostrar_mensagem_trindade=mostrar_mensagem_trindade,
        docs_alunos=docs_alunos
    )

@app.route('/editar_aluno/<int:id>', methods=['POST'])
def editar_aluno(id):

    nome = request.form['nome']
    telefone = request.form['telefone']
    cpf = request.form['cpf']
    email = request.form['email']
    usuario = request.form['user']
    senha = request.form['senha']
    faculdade = request.form['faculdade']
    curso = request.form['curso']
    rota = request.form['rota']
    foto_perfil = request.files.get("ft_perfil")
    rg_frente = request.files.get("rg_frente")
    rg_verso = request.files.get("rg_verso")
    comprovante_endereco = request.files.get("comprovante_endereco")
    comprovante_matricula = request.files.get("comprovante_matricula")
    
    print(id)
    print(nome)
    print(telefone)
    print(cpf)

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE aluno
        SET
            nome = %s,
            telefone = %s,
            cpf = %s,
            email = %s,
            usuario = %s,
            senha = %s,
            faculdade = %s,
            curso = %s,
            rota = %s
        WHERE id = %s
    """, (
        nome,
        telefone,
        cpf,
        email,
        usuario,
        senha,
        faculdade,
        curso,
        rota,
        id
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    atualizar_documento(
        id,
        "foto_perfil",
        foto_perfil
    )

    atualizar_documento(
        id,
        "rg_frente",
        rg_frente
    )

    atualizar_documento(
        id,
        "rg_verso",
        rg_verso
    )

    atualizar_documento(
        id,
        "comprovante_endereco",
        comprovante_endereco
    )

    atualizar_documento(
        id,
        "comprovante_matricula",
        comprovante_matricula
    )

    return redirect('/administrador')

@app.route('/excluir_aluno/<int:id>')
def excluir_aluno(id):

    pasta_aluno = os.path.join(
        app.config["UPLOAD_FOLDER"],
        f"aluno_{id}"
    )

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM aluno
        WHERE id = %s
    """, (id,))

    conexao.commit()

    cursor.close()
    conexao.close()

    if os.path.exists(pasta_aluno):
        shutil.rmtree(pasta_aluno)

    return redirect('/administrador')

@app.route('/lista_espera')
def lista_espera():
    
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
                   SELECT usuario
                   FROM gestao
                   LIMIT 1""")
    admin = cursor.fetchone()
    usuario = admin[0] if admin else None

    cursor.execute("""
                    SELECT *
                    FROM aluno
                    WHERE rota = 'goiania'
                    AND status = 'Em espera'
                    ORDER BY id
                   """)
    goiania = cursor.fetchall()

    cursor.execute("""
        SELECT *
        FROM aluno
        WHERE rota = 'trindade'
        AND status = 'Em espera'
        ORDER BY id
    """)

    trindade = cursor.fetchall()

    conexao.close()

    return render_template ('lista_espera.html',
                            usuario= usuario,
                            goiania=goiania,
                            trindade=trindade)

@app.route('/aprovar_aluno/<int:id>')
def aprovar_aluno(id):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE aluno
        SET status = 'Ativo'
        WHERE id = %s
    """, (id,))

    conexao.commit()

    cursor.close()
    conexao.close()

    return redirect('/lista_espera')

@app.route('/documento/<int:aluno_id>/<tipo>')
def visualizar_documento(aluno_id, tipo):

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome_arquivo
        FROM documento
        WHERE aluno_id = %s
        AND tipo_documento = %s
    """, (aluno_id, tipo))

    resultado = cursor.fetchone()

    conexao.close()

    if not resultado:
        return "Documento não encontrado", 404

    nome_arquivo = resultado[0]

    caminho = os.path.join(
        app.config["UPLOAD_FOLDER"],
        f"aluno_{aluno_id}",
        nome_arquivo
    )

    if not os.path.exists(caminho):
        return "Arquivo não encontrado", 404

    print(caminho)
    return send_file(caminho)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

# ---------------------- ADMIN ------------------------------------

    admin = executar_select("""SELECT usuario
                FROM gestao
                LIMIT 1
                """)

    usuario = admin[0][0] if admin else None

# ---------------------- Total de alunos --------------------------
    resultado_total = executar_select("SELECT COUNT(*) FROM aluno")
    mensagem_total_aluno = resultado_total[0][0]

# ---------------------- Ativos por rota --------------------------
    resultado_ativos = executar_select("""
    SELECT
        SUM(CASE WHEN status = 'Ativo'                             THEN 1 ELSE 0 END) AS total_ativo,
        SUM(CASE WHEN status = 'Ativo'   AND rota = 'goiania'      THEN 1 ELSE 0 END) AS ativo_goiania,
        SUM(CASE WHEN status = 'Ativo'   AND rota = 'trindade'     THEN 1 ELSE 0 END) AS ativo_trindade,
        SUM(CASE WHEN status = 'Em espera'                         THEN 1 ELSE 0 END) AS total_espera,
        SUM(CASE WHEN status = 'Em espera' AND rota = 'goiania'    THEN 1 ELSE 0 END) AS espera_goiania,
        SUM(CASE WHEN status = 'Em espera' AND rota = 'trindade'   THEN 1 ELSE 0 END) AS espera_trindade,
        COUNT(DISTINCT faculdade)                                                      AS total_faculdade,
        COUNT(DISTINCT CASE WHEN rota = 'goiania' AND status = 'Ativo' THEN faculdade END)                AS faculdade_goiania,
        COUNT(DISTINCT CASE WHEN rota = 'trindade' THEN faculdade END)                AS faculdade_trindade
    FROM aluno
""")

    row = resultado_ativos[0]

    mensagem_total_ativo      = row[0]
    mensagem_total_ativoG     = row[1]
    mensagem_total_ativoT     = row[2]  # <-- estava sendo ignorado antes
    mensagem_total_espera     = row[3]
    mensagem_total_esperaG    = row[4]  # <-- estava sendo misturado com ativoG
    mensagem_total_esperaT    = row[5]
    mensagem_total_faculdade  = row[6]  # <-- agora conta faculdades únicas
    mensagem_total_faculdadeG = row[7]

    mensagem_total_faculdadeT = row[8]

    return render_template('dashboard.html',
                        mensagem_total_ativo=mensagem_total_ativo,
                        mensagem_total_espera=mensagem_total_espera,
                        mensagem_total_faculdade=mensagem_total_faculdade,
                        mensagem_total_ativoG=mensagem_total_ativoG,
                        mensagem_total_ativoT=mensagem_total_ativoT,
                        mensagem_total_faculdadeG=mensagem_total_faculdadeG,
                        mensagem_total_faculdadeT=mensagem_total_faculdadeT,
                        mensagem_total_esperaG=mensagem_total_esperaG,
                        mensagem_total_esperaT=mensagem_total_esperaT,
                        mensagem_total_aluno=mensagem_total_aluno,
                        usuario=usuario)

if __name__ == '__main__':
    app.run(debug=True)