from flask import *

app = Flask(__name__)
animais = []
usuarios = [['a','a@a','a']]

@app.route('/')
def pagina_principal():
    return render_template('PetLogin.html')

@app.route('/Login', methods=['post'])
def pag_login():
    global usuarios
    email = request.form.get('email')
    senha = request.form.get('senha')
    logado = False
    for user in usuarios:
        if email == user[1] and senha == user[2]:
            logado = True
            break

    if logado:
        return render_template('pagClienteAdm.html')
    else:
        return render_template('PetLogin.html')


@app.route("/cadastrarcliente", methods=["post"])
def cadastrar():
    nome = request.form["nome"]
    email = request.form["email"]
    senha = request.form["Senha"]

    usuarios.append([nome,email,senha])

    return render_template("PetLogin.html")



@app.route('/Cadastrese', methods=['post'])
def pag_cadastro():
    return render_template('Cadastrese.html')

@app.route('/escolher', methods=['post'])
def escolher():
    if 'cliente' in request.form:
        return render_template('PetCadastro.html')
    elif 'servidor' in request.form:
        return render_template('PetSenha.html')



@app.route('/verificarsenha', methods=['post'])
def verificar_senha():
    senha = request.form.get('senha')
    if senha == 'pet':
        return render_template('PetLista.html', animais=animais)
    else:
        return render_template('PetSenha.html')

@app.route("/adicionar", methods=["post"])
def adicionar():

    nome= request.form["nome"]
    especie = request.form["especie"]
    email_dono = request.form["email"]
    tipodeservico = request.form["Tipodeservico"]

    animais.append([nome, especie, email_dono, tipodeservico ])
    return render_template("PetCadastro.html", animais=animais)

@app.route('/voltar', methods=['post'])
def voltar():
    return render_template('PetCadastro.html')

@app.route('/remover', methods=['post'])
def remover_animal():
    global animais
    nome = request.form.get("nome")
    animais = [a for a in animais if a["nome"] != nome]

    return render_template('PetLista.html', animais=animais)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
