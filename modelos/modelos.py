from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

#é um modelo que vai  representar uma tabela no BD
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'

    email = Column(String, primary_key=True)
    nome = Column(String)
    senha = Column(String)


    def __repr__(self):
        return f"<Usuario(email='{self.email}', nome='{self.nome}')>"

class Animal(Base):
    __tablename__ = 'animais'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    especie = Column(String)
    email_dono = Column(String)
    tipodeservico = Column(String)

    def __repr__(self):
        return f"<animais(id='{self.id}', nome='{self.nome}')>"
