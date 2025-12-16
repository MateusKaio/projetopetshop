from flask import *
from dao.usuarioDAO import *
from dao.animalDAO import *

from dao.banco import *

usuarios = [['m','m@m','m']]


app = Flask(__name__)
app.secret_key = 'KJH#45K45JHQASs'

init_db()

@app.before_request
def pegar_sessao():
    g.session = Session()

@app.teardown_appcontext
def encerrar_sessao(exception=None):
    Session.remove()


@app.route('/')
def pagina_principal():
    return render_template('PetLogin.html')


@app.route('/login', methods=['POST'])
def pag_login():
    email = request.form.get('email')
    senha = request.form.get('senha')
    tipo = request.form.get('tipo')

    usuario_dao = UsuarioDAO(Session)

    if tipo == 'cliente':
        user = usuario_dao.autenticar(email, senha)
        if user:
                session['cliente'] = email
                return render_template('PetCadastro.html')
        return render_template('PetLogin.html')

    if email == 'admin@m' and senha == '123':
        session['admin'] = True
        return render_template('adm/pagadmin.html')

    return render_template('PetLogin.html')


@app.route("/cadastrarcliente", methods=["POST", 'GET'])
def cadastrar():
    if request.method == 'GET':
        return render_template('cadastrouser.html')

    usuario_dao = UsuarioDAO(g.session)

    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")

    novo_usuario = Usuario(nome=nome, email=email, senha=senha)

    usuario_dao.criar(novo_usuario)

    return render_template("PetLogin.html")


@app.route('/logout')
def fazer_logout():
    session.clear()
    return redirect('/')

def cliente_logado():
    return 'cliente' in session


@app.route('/adicionar', methods=['POST'])
def adicionar():

    if not cliente_logado():
        return redirect('/')

    nome = request.form["nome"]
    especie = request.form["especie"]
    email_dono = request.form["email"]
    tipodeservico = request.form["Tipodeservico"]

    animal_dao = AnimalDAO(g.session)

    novo = Animal(
        nome=nome,
        especie=especie,
        email_dono=email_dono,
        tipodeservico=tipodeservico
    )

    animal_dao.criar(novo)

    msg = f"{nome} adicionado com sucesso"
    return render_template("PetCadastro.html", msg=msg)

@app.route('/voltar', methods=['POST'])
def voltar():
    if not cliente_logado():
        return redirect('/')
    return render_template('PetCadastro.html')


def admin_logado():
    return 'admin' in session


@app.route('/menu', methods=['POST'])
def menu():
    if not admin_logado():
        return redirect('/')
    return render_template('adm/pagadmin.html')


@app.route('/verificarsenha', methods=['GET', 'POST'])
def verificar_senha():

    if request.method == 'GET':
        if admin_logado():
            animal_dao = AnimalDAO(g.session)
            lista = animal_dao.listar_animais()
            return render_template('adm/Petlista.html', lista=lista)

    login = request.form.get('login')
    senha = request.form.get('senha')

    if login == 'admin' and senha == '123':
        session['admin'] = True
        animal_dao = AnimalDAO(g.session)
        lista = animal_dao.listar_animais()
        return render_template('adm/Petlista.html', lista=lista)
    return render_template('adm/PetSenha.html')


@app.route('/remover', methods=['POST'])
def remover_animal():
    if not admin_logado():
        return redirect('/')

    id = request.form.get("id")

    animal_dao = AnimalDAO(g.session)
    animal = animal_dao.buscar_por_id(id)

    if animal:
        g.session.delete(animal)
        g.session.commit()

    animal_dao = AnimalDAO(g.session)
    lista = animal_dao.listar_animais()
    return render_template('adm/Petlista.html', lista=lista)


@app.route('/detalhes')
def mostrar_detalhes():
    if not admin_logado():
        return redirect('/')

    id_animal = request.values.get('id')

    animal_dao = AnimalDAO(g.session)
    animal = animal_dao.buscar_por_id(id_animal)

    return render_template('adm/detalhes.html', animal=animal)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

