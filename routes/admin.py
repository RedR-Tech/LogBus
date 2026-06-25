from flask import Blueprint, request, render_template, redirect, url_for, session, current_app, send_file
from db import conectar_banco, executar_select
from werkzeug.utils import secure_filename
import os
import shutil

admin_bp = Blueprint('admin', __name__)

def atualizar_documento(aluno_id, tipo_documento, arquivo):

    if not arquivo or arquivo.filename == "":
        return

    pasta_aluno = os.path.join(current_app.config["UPLOAD_FOLDER"], f"aluno_{aluno_id}")
    extensao = os.path.splitext(secure_filename(arquivo.filename))[1].lower()
    nome_arquivo = f"{tipo_documento}{extensao}"
    caminho = os.path.join(pasta_aluno, nome_arquivo)

    if not os.path.exists(pasta_aluno):
        os.makedirs(pasta_aluno, exist_ok=True)

    for arquivo_existente in os.listdir(pasta_aluno):
        if arquivo_existente.startswith(tipo_documento):
            os.remove(os.path.join(pasta_aluno, arquivo_existente))

    arquivo.save(caminho)

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE documento SET nome_arquivo = %s
        WHERE aluno_id = %s AND tipo_documento = %s
    """, (nome_arquivo, aluno_id, tipo_documento))
    conexao.commit()
    cursor.close()
    conexao.close()

@admin_bp.route('/administrador', methods=['GET', 'POST'])
def admin():

    if session.get('tipo') != 'gestao':
        return redirect(url_for('auth.tela_principal'))

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT aluno_id, tipo_documento, nome_arquivo FROM documento")
    rows = cursor.fetchall()

    docs_alunos = {}
    for row in rows:
        aluno_id, tipo_documento, nome_arquivo = row
        if aluno_id not in docs_alunos:
            docs_alunos[aluno_id] = {}
        docs_alunos[aluno_id][tipo_documento] = nome_arquivo

    goiania  = executar_select("SELECT * FROM aluno WHERE rota = %s AND status = 'Ativo'", ("goiania",))
    trindade = executar_select("SELECT * FROM aluno WHERE rota = %s AND status = 'Ativo'", ("trindade",))

    cursor.execute("SELECT COUNT(*) FROM aluno WHERE rota = 'goiania' AND status != 'Em espera'")
    mostrar_mensagem_goiania = (cursor.fetchone()[0] == 0)

    cursor.execute("SELECT COUNT(*) FROM aluno WHERE rota = 'trindade' AND status != 'Em espera'")
    mostrar_mensagem_trindade = (cursor.fetchone()[0] == 0)

    cursor.execute("SELECT aluno_id, tipo_documento FROM documento")
    documentos_alunos = {}
    for aluno_id, tipo in cursor.fetchall():
        if aluno_id not in documentos_alunos:
            documentos_alunos[aluno_id] = {}
        documentos_alunos[aluno_id][tipo] = True

    cursor.execute("SELECT usuario FROM gestao LIMIT 1")
    admin = cursor.fetchone()
    usuario = admin[0] if admin else None

    cursor.execute("SELECT DISTINCT faculdade FROM aluno WHERE rota = 'goiania' AND status = 'Ativo' ORDER BY faculdade")
    faculdade_goiania = cursor.fetchall()

    cursor.execute("SELECT DISTINCT faculdade FROM aluno WHERE rota = 'trindade' AND status = 'Ativo' ORDER BY faculdade")
    faculdade_trindade = cursor.fetchall()

    conexao.close()

    return render_template('adm.html',
        goiania=goiania, trindade=trindade, usuario=usuario,
        faculdade_goiania=faculdade_goiania, faculdade_trindade=faculdade_trindade,
        documentos_alunos=documentos_alunos,
        mostrar_mensagem_goiania=mostrar_mensagem_goiania,
        mostrar_mensagem_trindade=mostrar_mensagem_trindade,
        docs_alunos=docs_alunos)

@admin_bp.route('/editar_aluno/<int:id>', methods=['POST'])
def editar_aluno(id):

    if session.get('tipo') != 'gestao':
        return redirect(url_for('auth.tela_principal'))

    import bcrypt
    nome      = request.form['nome']
    telefone  = request.form['telefone']
    cpf       = request.form['cpf']
    email     = request.form['email']
    usuario   = request.form['user']
    senha_raw = request.form['senha']
    senha     = bcrypt.hashpw(senha_raw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    faculdade = request.form['faculdade']
    curso     = request.form['curso']
    rota      = request.form['rota']

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE aluno SET nome=%s, telefone=%s, cpf=%s, email=%s,
        usuario=%s, senha=%s, faculdade=%s, curso=%s, rota=%s
        WHERE id = %s
    """, (nome, telefone, cpf, email, usuario, senha, faculdade, curso, rota, id))

    conexao.commit()
    cursor.close()
    conexao.close()

    for tipo in ["foto_perfil", "rg_frente", "rg_verso", "comprovante_endereco", "comprovante_matricula"]:
        atualizar_documento(id, tipo, request.files.get(tipo if tipo != "foto_perfil" else "ft_perfil"))

    return redirect(url_for('admin.admin'))

@admin_bp.route('/excluir_aluno/<int:id>')
def excluir_aluno(id):

    if session.get('tipo') != 'gestao':
        return redirect(url_for('auth.tela_principal'))

    pasta_aluno = os.path.join(current_app.config["UPLOAD_FOLDER"], f"aluno_{id}")

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM aluno WHERE id = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()

    if os.path.exists(pasta_aluno):
        shutil.rmtree(pasta_aluno)

    return redirect(url_for('admin.admin'))

@admin_bp.route('/lista_espera')
def lista_espera():

    if session.get('tipo') != 'gestao':
        return redirect(url_for('auth.tela_principal'))

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT usuario FROM gestao LIMIT 1")
    admin = cursor.fetchone()
    usuario = admin[0] if admin else None

    cursor.execute("SELECT * FROM aluno WHERE rota = 'goiania' AND status = 'Em espera' ORDER BY id")
    goiania = cursor.fetchall()

    cursor.execute("SELECT * FROM aluno WHERE rota = 'trindade' AND status = 'Em espera' ORDER BY id")
    trindade = cursor.fetchall()

    conexao.close()

    return render_template('lista_espera.html', usuario=usuario, goiania=goiania, trindade=trindade)

@admin_bp.route('/aprovar_aluno/<int:id>')
def aprovar_aluno(id):

    if session.get('tipo') != 'gestao':
        return redirect(url_for('auth.tela_principal'))

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("UPDATE aluno SET status = 'Ativo' WHERE id = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()

    return redirect(url_for('admin.lista_espera'))

@admin_bp.route('/documento/<int:aluno_id>/<tipo>')
def visualizar_documento(aluno_id, tipo):

    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome_arquivo FROM documento WHERE aluno_id = %s AND tipo_documento = %s", (aluno_id, tipo))
    resultado = cursor.fetchone()
    conexao.close()

    if not resultado:
        return "Documento não encontrado", 404

    caminho = os.path.join(current_app.config["UPLOAD_FOLDER"], f"aluno_{aluno_id}", resultado[0])

    if not os.path.exists(caminho):
        return "Arquivo não encontrado", 404

    return send_file(caminho)

@admin_bp.route('/dashboard')
def dashboard():

    if session.get('tipo') != 'gestao':
        return redirect(url_for('auth.tela_principal'))

    admin = executar_select("SELECT usuario FROM gestao LIMIT 1")
    usuario = admin[0][0] if admin else None

    resultado_total = executar_select("SELECT COUNT(*) FROM aluno")
    mensagem_total_aluno = resultado_total[0][0]

    resultado_ativos = executar_select("""
        SELECT
            SUM(CASE WHEN status = 'Ativo'                                              THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Ativo'     AND rota = 'goiania'                     THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Ativo'     AND rota = 'trindade'                    THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Em espera'                                          THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Em espera' AND rota = 'goiania'                     THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Em espera' AND rota = 'trindade'                    THEN 1 ELSE 0 END),
            COUNT(DISTINCT faculdade),
            COUNT(DISTINCT CASE WHEN rota = 'goiania'  AND status = 'Ativo' THEN faculdade END),
            COUNT(DISTINCT CASE WHEN rota = 'trindade'                      THEN faculdade END)
        FROM aluno
    """)

    row = resultado_ativos[0]

    return render_template('dashboard.html',
        mensagem_total_ativo=row[0],      mensagem_total_espera=row[3],
        mensagem_total_faculdade=row[6],  mensagem_total_ativoG=row[1],
        mensagem_total_ativoT=row[2],     mensagem_total_faculdadeG=row[7],
        mensagem_total_faculdadeT=row[8], mensagem_total_esperaG=row[4],
        mensagem_total_esperaT=row[5],    mensagem_total_aluno=mensagem_total_aluno,
        usuario=usuario)