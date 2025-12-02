from flask import *

app = Flask(__name__)
app.secret_key = 'KJH#45K45JHQASs'
animais = []
usuarios = [['m','m@m','m']]

@app.route('/')
def pagina_principal():
    return render_template('PetLogin.html')

@app.route('/login', methods=['post'])
def pag_login():
    global usuarios
    email = request.form.get('email')
    senha = request.form.get('senha')
    tipo = request.form.get('tipo')
    if tipo == 'cliente':
        if email == 'm@m' and senha == 'm':
            session['cliente'] = email
            return render_template('PetCadastro.html')
        else:
            return render_template('PetLogin.html')
    else:
        if email == 'admin@m' and senha == '123':
            session['admin'] = 'admin'
            return render_template('adm/pagadmin.html')
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


@app.route('/verificarsenha', methods=['post','get'])
def verificar_senha():
    if request.method == 'GET':
        return render_template('adm/Petlista.html', lista=animais)
    else:
        login = request.form.get('login')
        senha = request.form.get('senha')
        if login == 'admin' and senha == '123':
            session['login'] = login
            return render_template('adm/Petlista.html', lista=animais)
        else:
            return render_template('adm/PetSenha.html')

@app.route("/adicionar", methods=["post"])
def adicionar():

    nome= request.form["nome"]
    especie = request.form["especie"]
    email_dono = request.form["email"]
    tipodeservico = request.form["Tipodeservico"]

    animais.append([nome, especie, email_dono, tipodeservico ])
    msg =  nome + ' adicionado com sucesso'
    print(msg)
    return render_template("PetCadastro.html", animais=animais, msg=msg)

@app.route('/logout')
def fazer_logout():
    session.clear()
    return render_template('PetLogin.html')

@app.route('/voltar', methods=['post'])
def voltar():
    return render_template('PetCadastro.html')

@app.route('/menu', methods=['post'])
def menu():
    return render_template('adm/pagadmin.html')



@app.route('/remover', methods=['post'])
def remover_animal():
    global animais
    email_dono = request.form.get("email_dono")

    for animal in animais:
        if animal[2] == email_dono:
            animais.remove(animal)
            print("animal removido")


    return render_template('adm/PetLista.html', lista=animais)



@app.route('/detalhes')
def mostrar_detalhes():
    email = request.values.get('email')
    achei = None
    for animal in animais:
        if email == animal[2]:
            achei = animal
        break

    return render_template('adm/detalhes.html', animais=achei)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
