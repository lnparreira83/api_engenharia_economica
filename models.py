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


class FatorAcumulacaoCapital(Base):
    __tablename__ = 'acumulacaocapital'
    id = Column(Integer, primary_key=True)
    fator_acumulado = Column(Float())
    taxa = Column(Float())
    tempo = Column(Float())
    montante_composto = Column(Float())

    def __repr__(self):
        return '<Fator Capital {}>'.format(self.fator_acumulado)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class DescontoSimples(Base):
    __tablename__ = 'descontosimples'
    id = Column(Integer, primary_key=True)
    desconto_simples = Column(Float())
    montante = Column(Float())
    taxa = Column(Float())
    tempo = Column(Float())
    valor_atual = Column(Float())

    def __repr__(self):
        return '<Fator Capital {}>'.format(self.desconto_simples)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class DescontoComposto(Base):
    __tablename__ = 'descontocomposto'
    id = Column(Integer, primary_key=True)
    desconto_composto = Column(Float())
    montante = Column(Float())
    taxa = Column(Float())
    tempo = Column(Float())
    valor_atual = Column(Float())

    def __repr__(self):
        return '<Desconto composto {}>'.format(self.desconto_composto)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class SistemaPrestacaoConstante(Base):
    __tablename__ = 'prestacaoconstante_spc'
    id = Column(Integer, primary_key=True)
    saldo_devedor = Column(Float())
    amortizacao = Column(Float())
    taxa = Column(Float())
    tempo = Column(Float())
    prestacao = Column(Float())

    def __repr__(self):
        return '<Desconto composto {}>'.format(self.saldo_devedor)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class SistemaAmortizacaoConstante(Base):
    __tablename__ = 'amortizacaoconstante'
    id = Column(Integer, primary_key=True)
    saldo_devedor = Column(Float())
    amortizacao = Column(Float())
    taxa = Column(Float())
    tempo = Column(Float())
    prestacao = Column(Float())

    def __repr__(self):
        return '<Amortizacao constante {}>'.format(self.saldo_devedor)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class AnaliseHorizontal(Base):
    __tablename__ = 'analisehorizontal_'
    id = Column(Integer, primary_key=True)
    receita_base = Column(Float())
    custo_base = Column(Float())
    periodo_base = Column(Integer())
    receita_atual = Column(Float())
    custo_atual = Column(Float())
    periodo_atual = Column(Integer())
    resultado_bruto = Column(Float())
    variacao_receita = Column(Float())
    variacao_custo = Column(Float())

    def __repr__(self):
        return '<Analise horizontal {}>'.format(self.variacao_custo)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class AnaliseVertical(Base):
    __tablename__ = 'analisevertical'
    id = Column(Integer, primary_key=True)
    receita_base = Column(Float())
    custo_base = Column(Float())
    periodo_base = Column(Integer())
    receita_atual = Column(Float())
    custo_atual = Column(Float())
    periodo_atual = Column(Integer())
    resultado_bruto = Column(Float())
    variacao_receita = Column(Float())
    variacao_custo = Column(Float())

    def __repr__(self):
        return '<Analise horizontal {}>'.format(self.variacao_custo)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class LiquidezImediata(Base):
    __tablename__ = 'liquidezimediata_'
    id = Column(Integer, primary_key=True)
    caixa = Column(Float())
    equivalentes_caixa = Column(Float())
    liquidez_imediata = Column(Float())
    passivo_circulante = Column(Float())
    resultado = Column(String())

    def __repr__(self):
        return '<Liquidez imediata {}>'.format(self.resultado)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class LiquidezCorrente(Base):
    __tablename__ = 'liquidezcorrente'
    id = Column(Integer, primary_key=True)
    ativo_circulante = Column(Float())
    liquidez_corrente = Column(Float())
    passivo_circulante = Column(Float())
    resultado = Column(String())

    def __repr__(self):
        return '<Liquidez corrente {}>'.format(self.resultado)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class LiquidezSeca(Base):
    __tablename__ = 'liquidezseca'
    id = Column(Integer, primary_key=True)
    ativo_circulante = Column(Float())
    estoques = Column(Float())
    liquidez_seca = Column(Float())
    passivo_circulante = Column(Float())
    resultado = Column(String())

    def __repr__(self):
        return '<Liquidez seca {}>'.format(self.resultado)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class LiquidezGeral(Base):
    __tablename__ = 'liquidezgeral'
    id = Column(Integer, primary_key=True)
    ativo_circulante = Column(Float())
    realizavel_longo_prazo = Column(Float())
    liquidez_geral = Column(Float())
    passivo_circulante = Column(Float())
    exigivel_longo_prazo = Column(Float())
    resultado = Column(String())

    def __repr__(self):
        return '<Liquidez geral {}>'.format(self.resultado)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class MargemLiquida(Base):
    __tablename__ = 'margemliquida'
    id = Column(Integer, primary_key=True)
    lucro_liquido = Column(Float())
    receita_liquida = Column(Float())
    margem_liquida = Column(Float())

    def __repr__(self):
        return '<Margem liquida {}>'.format(self.margem_liquida)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class GiroAtivo(Base):
    __tablename__ = 'giroativo'
    id = Column(Integer, primary_key=True)
    ativo = Column(Float())
    receita_liquida = Column(Float())
    giro_ativo = Column(Float())

    def __repr__(self):
        return '<Giro ativo {}>'.format(self.giro_ativo)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class RentabilidadeAtivo(Base):
    __tablename__ = 'rentabilidadeativo_'
    id = Column(Integer, primary_key=True)
    lucro_liquido = Column(Float())
    ativo = Column(Float())
    rentabilidade_ativo = Column(Float())

    def __repr__(self):
        return '<Rentabilidade do ativo {}>'.format(self.rentabilidade_ativo)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class RentabilidadePl(Base):
    __tablename__ = 'rentabilidadepl_'
    id = Column(Integer, primary_key=True)
    lucro_liquido = Column(Float())
    patrimonio_liquido = Column(Float())
    rentabilidade_pl = Column(Float())

    def __repr__(self):
        return '<Rentabilidade do PL {}>'.format(self.rentabilidade_pl)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class PrazoMedioEstocagem(Base):
    __tablename__ = 'prazomedioestocagem'
    id = Column(Integer, primary_key=True)
    ciclo_estocagem = Column(Float())
    estoque_medio = Column(Float())
    custo_mercadorias_vendidas = Column(Float())

    def __repr__(self):
        return '<Prazo medio de estocagem {}>'.format(self.ciclo_estocagem)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class PrazoMedioPagamento(Base):
    __tablename__ = 'prazomediopagamento'
    id = Column(Integer, primary_key=True)
    ciclo_pagamento = Column(Float())
    fornecedores_medios = Column(Float())
    custo_mercadorias_vendidas = Column(Float())

    def __repr__(self):
        return '<Prazo medio de pagamento {}>'.format(self.ciclo_pagamento)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class PrazoMedioRecebimento(Base):
    __tablename__ = 'prazomediorecebimento_'
    id = Column(Integer, primary_key=True)
    ciclo_recebimento = Column(Float())
    clientes_medios = Column(Float())
    receita_bruta = Column(Float())

    def __repr__(self):
        return '<Prazo medio de recebimento {}>'.format(self.ciclo_recebimento)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Ciclos(Base):
    __tablename__ = 'ciclos'
    id = Column(Integer, primary_key=True)
    prazo_medio_estocagem = Column(Float())
    prazo_medio_recebimento = Column(Float())
    prazo_medio_pagamento = Column(Float())
    ciclo_operacional = Column(Float())
    ciclo_financeiro = Column(Float())

    def __repr__(self):
        return '<Ciclo {}>'.format(self.ciclo_financeiro)

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
