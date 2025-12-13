from sqlalchemy.orm import scoped_session
from modelos.modelos import Usuario, Animal


class AnimalDAO:
    #construtor da classe: instanciar um objeto, ele cria uma sessao
    def __init__(self, session: scoped_session):
        self.session = session

    def criar(self, animal):

        self.session.add(animal)
        self.session.commit()

    def buscar_por_id(self, id):
        return self.session.query(Animal).filter_by(id=id).first()

    def listar_animais(self):
        return self.session.query(Animal).all()

    def autenticar(self, id, senha):
        user = self.buscar_por_id(id)
        if user and user.senha == senha:
            return user
        return None