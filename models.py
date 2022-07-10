from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///operacoes.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class OperacaoJuroComposto(Base):
    __tablename__ = 'juroscompostos'
    id = Column(Integer, primary_key=True)
    juroscompostos = Column(Float())
    capital = Column(Float())
    taxa = Column(Float())
    tempo = Column(Float())

    def __repr__(self):
        return '<Juros Compostos {}>'.format(self.juroscompostos)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Operacoes(Base):
    __tablename__ = 'jurossimples'
    id = Column(Integer, primary_key=True)
    jurossimples = Column(Float())
    capital = Column(Float())
    taxa = Column(Float())
    tempo = Column(Float())

    def __repr__(self):
        return '<Juros {}>'.format(self.jurossimples)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class OperacaoTaxaNominal(Base):
    __tablename__ = 'taxanominal'
    id = Column(Integer, primary_key=True)
    valor_emprestimo = Column(Float())
    valor_quitacao = Column(Float())
    taxa = Column(Float())

    def __repr__(self):
        return '<Taxa nominal {}>'.format(self.taxa)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class OperacaoTaxaEfetiva(Base):
    __tablename__ = 'taxaefetiva'
    id = Column(Integer, primary_key=True)
    taxa_efetiva = Column(Float())
    taxa_nominal = Column(Float())
    quantidade_periodos = Column(Float())

    def __repr__(self):
        return '<Taxa efetiva {}>'.format(self.taxa_efetiva)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class OperacaoTaxaJurosReal(Base):
    __tablename__ = 'taxareal'
    id = Column(Integer, primary_key=True)
    taxa_real = Column(Float())
    taxa_nominal = Column(Float())
    inflacao_periodo = Column(Float())

    def __repr__(self):
        return '<Taxa efetiva {}>'.format(self.taxa_real)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
