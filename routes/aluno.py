from flask import Blueprint, render_template, redirect, url_for, session
from db import conectar_banco

aluno_bp = Blueprint('aluno', __name__)

@aluno_bp.route('/aluno')
def tela_aluno():

    if session.get('tipo') != 'aluno':
        return redirect(url_for('auth.tela_principal'))

    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT * FROM aluno WHERE usuario = %s
    """, (session['usuario'],))

    dados = cursor.fetchone()

    cursor.execute("""
        SELECT tipo_documento, nome_arquivo
        FROM documento d
        JOIN aluno a ON d.aluno_id = a.id
        WHERE a.usuario = %s
    """, (session['usuario'],))

    documentos_db = cursor.fetchall()
    conexao.close()

    documentos = {tipo: arquivo for tipo, arquivo in documentos_db}

    aluno = {
        'id':                    dados[0],
        'nome':                  dados[1],
        'telefone':              dados[2],
        'cpf':                   dados[3],
        'email':                 dados[4],
        'usuario':               dados[5],
        'faculdade':             dados[7],
        'curso':                 dados[8],
        'rota':                  dados[9],
        'status':                dados[11],
        'foto_perfil':           documentos.get('foto_perfil'),
        'rg_frente':             documentos.get('rg_frente'),
        'rg_verso':              documentos.get('rg_verso'),
        'comprovante_endereco':  documentos.get('comprovante_endereco'),
        'comprovante_matricula': documentos.get('comprovante_matricula'),
    }

    docs_espec = [
        {"tipo": aluno['comprovante_endereco'],  "nome": "Comprovante de Endereço"},
        {"tipo": aluno['comprovante_matricula'], "nome": "Comprovante de Matrícula"},
        {"tipo": aluno['rg_frente'],             "nome": "RG FRENTE"},
        {"tipo": aluno['rg_verso'],              "nome": "RG VERSO"},
    ]

    return render_template('Aluno.html', aluno=aluno, documentos=documentos, docs_espec=docs_espec)