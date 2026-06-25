from flask import Blueprint, request, render_template, redirect, url_for, session, current_app
from db import conectar_banco, executar_select
from werkzeug.utils import secure_filename
import bcrypt
import os

cadastro_bp = Blueprint('cadastro', __name__)

def salvar_arquivo(arquivo, nome_arquivo, aluno_id):
    pasta_aluno = os.path.join(current_app.config["UPLOAD_FOLDER"], f"aluno_{aluno_id}")
    os.makedirs(pasta_aluno, exist_ok=True)
    extensao = os.path.splitext(secure_filename(arquivo.filename))[1].lower()
    nome_final = f"{nome_arquivo}{extensao}"
    caminho = os.path.join(pasta_aluno, nome_final)
    arquivo.save(caminho)
    return nome_final

@cadastro_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():

    if request.method == 'POST':

        nome = request.form.get('nome')
        user = request.form.get('user')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        senha_raw = request.form.get('senha')
        senha = bcrypt.hashpw(senha_raw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        faculdade = request.form.get('faculdade')
        curso = request.form.get('curso')
        rota = request.form.get('rota')

        conexao = conectar_banco()
        cursor = conexao.cursor()

        try:
            cursor.execute("""
                INSERT INTO aluno
                (nome, usuario, telefone, cpf, email, senha, faculdade, curso, rota)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, user, telefone, cpf, email, senha, faculdade, curso, rota))

            conexao.commit()

        except Exception as e:
            conexao.close()
            erro = str(e)
            if 'cpf' in erro.lower():
                return render_template('cadastro.html', erro="CPF já cadastrado!")
            elif 'email' in erro.lower():
                return render_template('cadastro.html', erro="E-mail já cadastrado!")
            elif 'usuario' in erro.lower():
                return render_template('cadastro.html', erro="Usuário já cadastrado!")
            else:
                return render_template('cadastro.html', erro="Dados já cadastrados!")

        aluno_id = cursor.lastrowid

        arquivos = {
            "foto_perfil": request.files["ft_perfil"],
            "rg_frente": request.files["rg_frente"],
            "rg_verso": request.files["rg_verso"],
            "comprovante_endereco": request.files["comprovante_endereco"],
            "comprovante_matricula": request.files["comprovante_matricula"],
        }

        for tipo, arquivo in arquivos.items():
            nome_arquivo = salvar_arquivo(arquivo, tipo, aluno_id)
            cursor.execute("""
                INSERT INTO documento (aluno_id, tipo_documento, nome_arquivo)
                VALUES (%s, %s, %s)
            """, (aluno_id, tipo, os.path.basename(nome_arquivo)))

        conexao.commit()
        conexao.close()

        return redirect(url_for('auth.tela_principal'))

    return render_template('cadastro.html')

@cadastro_bp.route('/cadastro_admin', methods=['POST'])
def cadastrar_admin():

    if session.get('tipo') != 'gestao':
        return redirect(url_for('auth.tela_principal'))

    nome      = request.form.get('nome')
    user      = request.form.get('user')
    telefone  = request.form.get('telefone')
    cpf       = request.form.get('cpf')
    email     = request.form.get('email')
    senha_raw = request.form.get('senha')
    senha     = bcrypt.hashpw(senha_raw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    faculdade = request.form.get('faculdade')
    curso     = request.form.get('curso')
    rota      = request.form.get('rota')

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

    conexao = conectar_banco()
    cursor  = conexao.cursor()

    documentos = {
        "foto_perfil":           request.files.get("ft_perfil"),
        "rg_frente":             request.files.get("rg_frente"),
        "rg_verso":              request.files.get("rg_verso"),
        "comprovante_endereco":  request.files.get("comprovante_endereco"),
        "comprovante_matricula": request.files.get("comprovante_matricula"),
    }

    for tipo, arquivo in documentos.items():
        if arquivo and arquivo.filename != "":
            nome_arquivo = salvar_arquivo(arquivo, tipo, aluno_id)
            cursor.execute("""
                INSERT INTO documento (aluno_id, tipo_documento, nome_arquivo)
                VALUES (%s, %s, %s)
            """, (aluno_id, tipo, nome_arquivo))

    conexao.commit()
    conexao.close()

    return redirect(url_for('admin.admin'))

@cadastro_bp.route('/verificar/cpf/<cpf>')
def verificar_cpf(cpf):
    resultado = executar_select("SELECT id FROM aluno WHERE cpf = %s", (cpf,))
    return {'existe': len(resultado) > 0}

@cadastro_bp.route('/verificar/email/<email>')
def verificar_email(email):
    resultado = executar_select("SELECT id FROM aluno WHERE email = %s", (email,))
    return {'existe': len(resultado) > 0}

@cadastro_bp.route('/verificar/usuario/<usuario>')
def verificar_usuario(usuario):
    resultado = executar_select("SELECT id FROM aluno WHERE usuario = %s", (usuario,))
    return {'existe': len(resultado) > 0}