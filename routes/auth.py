from flask import Blueprint, request, render_template, redirect, url_for, session
from db import conectar_banco
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def tela_principal():

    mensagem = None

    if request.method == 'POST':

        tipo_login = request.form.get('login_tipo')

        if tipo_login == 'gestao':

            usuario = request.form.get('user')
            senha = request.form.get('senha')

            conexao = conectar_banco()
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT usuario, senha
                FROM gestao
                WHERE usuario = %s
            """, (usuario,))

            dados_verificacao = cursor.fetchone()
            conexao.close()

            if dados_verificacao and bcrypt.checkpw(senha.encode('utf-8'), dados_verificacao[1].encode('utf-8')):
                session['usuario'] = usuario
                session['tipo'] = 'gestao'
                return redirect(url_for('admin.admin'))
            else:
                mensagem = "Informações não encontradas!"

        elif tipo_login == 'aluno':

            usuario = request.form.get('user')
            senha = request.form.get('senha')

            conexao = conectar_banco()
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT usuario, senha
                FROM aluno
                WHERE usuario = %s
            """, (usuario,))

            dados_verificacao = cursor.fetchone()
            conexao.close()

            try:
                if dados_verificacao and bcrypt.checkpw(senha.encode('utf-8'), dados_verificacao[1].encode('utf-8')):
                    session['usuario'] = usuario
                    session['tipo'] = 'aluno'
                    return redirect(url_for('aluno.tela_aluno'))
                else:
                    mensagem = "Informações não encontradas!"
            except ValueError:
                mensagem = "Informações não encontradas!"

    return render_template('login.html', resultado=mensagem)