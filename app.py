from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from db import obter_conexao, fechar_conexao

app = Flask(__name__)
app.secret_key = "segredo_t1_flask"

@app.teardown_appcontext
def encerrar_conexao(exception):
    fechar_conexao(exception)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        if not email or not senha:
            flash("Preencha e-mail e senha.")
            return redirect(url_for("login"))
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s", (email, senha))
            usuario = cursor.fetchone()
        except mysql.connector.Error:
            flash("Erro ao conectar ao banco de dados.")
            usuario = None
        finally:
            cursor.close()
        if usuario:
            flash("Login realizado com sucesso.")
            return redirect(url_for("listar_usuarios"))
        else:
            flash("E-mail ou senha incorretos.")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar_senha = request.form.get("confirmar_senha")
        if not nome or not email or not senha or not confirmar_senha:
            flash("Preencha todos os campos.")
            return redirect(url_for("cadastro"))
        if senha != confirmar_senha:
            flash("As senhas não coincidem.")
            return redirect(url_for("cadastro"))
        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, perfil_id) VALUES (%s, %s, %s, %s)",
                (nome, email, senha, 5)
            )
            conexao.commit()
            flash("Cadastro realizado com sucesso. Faça login.")
            return redirect(url_for("login"))
        except mysql.connector.Error:
            conexao.rollback()
            flash("Erro ao cadastrar. E-mail já em uso.")
        finally:
            cursor.close()
    return render_template("cadastro.html")


@app.route("/logout")
def logout():
    flash("Logout realizado com sucesso.")
    return redirect(url_for("login"))


# ── USUÁRIOS ──────────────────────────────────────────────

@app.route("/usuarios/listar")
def listar_usuarios():
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT u.id_usuario AS id, u.nome, u.email, u.cpf, u.telefone,
                   u.cep, u.endereco, u.numero, u.bairro, u.cidade, u.estado,
                   p.nome AS perfil
            FROM usuarios u
            JOIN perfis p ON u.perfil_id = p.id_perfil
        """)
        lista_usuarios = cursor.fetchall()
    except mysql.connector.Error:
        flash("Erro ao buscar usuários.")
        lista_usuarios = []
    finally:
        cursor.close()
    return render_template("usuarios/listar_usuarios.html", usuarios=lista_usuarios)


@app.route("/usuarios/inserir", methods=["GET", "POST"])
def inserir_usuario():
    conexao = obter_conexao()
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        perfil_id = request.form.get("perfil")
        senha = request.form.get("senha")
        cpf = request.form.get("cpf")
        telefone = request.form.get("telefone")
        cep = request.form.get("cep")
        endereco = request.form.get("endereco")
        numero = request.form.get("numero")
        complemento = request.form.get("complemento")
        bairro = request.form.get("bairro")
        cidade = request.form.get("cidade")
        estado = request.form.get("estado")

        if not nome or not email or not perfil_id or not senha:
            flash("Preencha todos os campos obrigatórios.")
            return redirect(url_for("inserir_usuario"))

        cursor = conexao.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios 
                    (nome, email, senha, perfil_id, cpf, telefone, cep, endereco, numero, complemento, bairro, cidade, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nome, email, senha, perfil_id, cpf, telefone, cep, endereco, numero, complemento, bairro, cidade, estado))
            conexao.commit()
            flash("Usuário inserido com sucesso.")
            return redirect(url_for("listar_usuarios"))
        except mysql.connector.Error:
            conexao.rollback()
            flash("Erro ao inserir usuário. E-mail já existe.")
            return redirect(url_for("inserir_usuario"))
        finally:
            cursor.close()

    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_perfil AS id, nome FROM perfis")
        perfis = cursor.fetchall()
    except mysql.connector.Error:
        flash("Erro ao carregar perfis.")
        perfis = []
    finally:
        cursor.close()
    return render_template("usuarios/inserir_usuario.html", perfis=perfis)


@app.route("/usuarios/remover/<int:id>", methods=["POST"])
def remover_usuario(id):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
        conexao.commit()
        flash("Usuário removido com sucesso.")
    except mysql.connector.Error:
        conexao.rollback()
        flash("Erro ao remover usuário.")
    finally:
        cursor.close()
    return redirect(url_for("listar_usuarios"))


# ── PRODUTOS ──────────────────────────────────────────────

@app.route("/produtos/listar")
def listar_produtos():
    conexao = obter_conexao()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT p.id_produto AS id, p.nome, p.preco, p.estoque, c.nome AS categoria
            FROM produtos p
            JOIN categorias c ON p.categoria_id = c.id_categoria
        """)
        lista_produtos = cursor.fetchall()
    except mysql.connector.Error:
        flash("Erro ao buscar produtos.")
        lista_produtos = []
    finally:
        cursor.close()
    return render_template("produtos/listar_produtos.html", produtos=lista_produtos)


@app.route("/produtos/inserir", methods=["GET", "POST"])
def inserir_produto():
    conexao = obter_conexao()
    if request.method == "POST":
        nome = request.form.get("nome")
        preco = request.form.get("preco")
        estoque = request.form.get("estoque")
        categoria_id = request.form.get("categoria_id")
        if not nome or not preco or not estoque or not categoria_id:
            flash("Preencha todos os campos.")
            return redirect(url_for("inserir_produto"))
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO produtos (nome, preco, estoque, categoria_id) VALUES (%s, %s, %s, %s)",
                (nome, preco, estoque, categoria_id)
            )
            conexao.commit()
            flash("Produto inserido com sucesso.")
            return redirect(url_for("listar_produtos"))
        except mysql.connector.Error as e:
            conexao.rollback()
            flash(f"Erro ao inserir produto: {e}")
            return redirect(url_for("inserir_produto"))
        finally:
            cursor.close()
    cursor = conexao.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id_categoria AS id, nome FROM categorias")
        categorias = cursor.fetchall()
    except mysql.connector.Error:
        flash("Erro ao carregar categorias.")
        categorias = []
    finally:
        cursor.close()
    return render_template("produtos/inserir_produto.html", categorias=categorias)


if __name__ == "__main__":
    app.run(debug=True)