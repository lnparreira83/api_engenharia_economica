import math

from flask import Flask, request
from flask_restful import Resource, Api
from models import OperacaoJuroComposto
from models import Operacoes
from models import OperacaoTaxaNominal
from models import OperacaoTaxaEfetiva
from models import OperacaoTaxaJurosReal
from models import FatorAcumulacaoCapital
from models import DescontoSimples
from models import DescontoComposto
from models import SistemaPrestacaoConstante
from models import SistemaAmortizacaoConstante
from models import AnaliseHorizontal
from models import AnaliseVertical
from models import LiquidezImediata
from models import LiquidezCorrente
from models import LiquidezSeca
from models import LiquidezGeral
from models import MargemLiquida
from models import GiroAtivo
from models import RentabilidadeAtivo
from models import RentabilidadePl
import numpy

app = Flask(__name__)
api = Api(app)


class JuroComposto(Resource):
    def get(self, juroscompostos):
        juros_compostos = OperacaoJuroComposto.query.filter_by(juroscompostos=juroscompostos).first()
        try:
            response = {
                'juroscompostos': juros_compostos.juroscompostos,
                'capital': juros_compostos.capital,
                'taxa': juros_compostos.taxa,
                'tempo': juros_compostos.tempo
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Juros não encontrado'
            }
        return response

    def put(self, juroscompostos):
        juros_compostos = OperacaoJuroComposto.query.filter_by(juroscompostos=juroscompostos).first()
        dados = request.json
        if 'juroscompostos' in dados:
            juros_compostos.juroscompostos = dados['juroscompostos']

        if 'capital' in dados:
            juros_compostos.capital = dados['capital']

        if 'taxa' in dados:
            juros_compostos.taxa = dados['taxa']

        if 'tempo' in dados:
            juros_compostos.taxa = dados['tempo']

        juros_compostos.save()
        response = {
            'id': juros_compostos.id,
            'juroscompostos': juros_compostos.juroscompostos,
            'capital': juros_compostos.capital,
            'taxa': juros_compostos.taxa,
            'tempo': juros_compostos.tempo
        }

        return response

    def delete(self, juroscompostos):
        juroscompostos = OperacaoJuroComposto.query.filter_by(id=juroscompostos).first()
        mensagem = 'Juros {} excluidos com sucesso'.format(juroscompostos)
        juroscompostos.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaJurosCompostos(Resource):

    def get(self):
        juros_compostos = OperacaoJuroComposto.query.all()
        response = [{
            'id': i.id,
            'juroscompostos': i.juroscompostos,
            'capital': i.capital,
            'taxa': i.taxa,
            'tempo': i.tempo
        } for i in juros_compostos]
        return response

    def post(self):
        dados = request.json
        # calcular o Juros
        if dados['capital'] and dados['taxa'] and dados['tempo'] > 0:
            juros_compostos = OperacaoJuroComposto(
                id=dados['id'],
                juroscompostos=dados['capital'] * pow(1 + dados['taxa'] / 100, dados['tempo']),
                capital=dados['capital'],
                taxa=dados['taxa'],
                tempo=dados['tempo']
            )
        # calcular a taxa
        if dados['juroscompostos'] and dados['capital'] and dados['tempo'] > 0:
            juros_compostos = OperacaoJuroComposto(
                id=dados['id'],
                juroscompostos=dados['juroscompostos'],
                capital=dados['capital'],
                taxa=numpy.sqrt(dados['juroscompostos'] / dados['capital']) - 1,
                tempo=dados['tempo']
            )
        # calcular o capital
        if dados['juroscompostos'] and dados['taxa'] and dados['tempo'] > 0:
            juros_compostos = OperacaoJuroComposto(
                id=dados['id'],
                juroscompostos=dados['juroscompostos'],
                capital=dados['juroscompostos'] / (1 + dados['taxa'] / 100) ^ dados['tempo'],
                taxa=dados['taxa'],
                tempo=dados['tempo']
            )
        # calcular o tempo
        if dados['juroscompostos'] and dados['capital'] and dados['taxa'] > 0:
            juros_compostos = OperacaoJuroComposto(
                id=dados['id'],
                juroscompostos=dados['juroscompostos'],
                capital=dados['capital'],
                taxa=dados['taxa'],
                tempo=numpy.log(dados['juroscompostos'] / dados['capital']) / numpy.log(1 + dados['taxa'] / 100)
            )
        juros_compostos.save()
        response = {
            'id': juros_compostos.id,
            'juroscompostos': juros_compostos.juroscompostos,
            'capital': juros_compostos.capital,
            'taxa': juros_compostos.taxa,
            'tempo': juros_compostos.tempo
        }
        return response


class Operacao(Resource):
    def get(self, jurossimples):
        juros_simples = Operacoes.query.filter_by(jurossimples=jurossimples).first()
        try:
            response = {
                'jurossimples': juros_simples.jurossimples,
                'capital': juros_simples.capital,
                'taxa': juros_simples.taxa,
                'tempo': juros_simples.tempo
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Juros não encontrado'
            }
        return response

    def put(self, jurossimples):
        juros_simples = Operacoes.query.filter_by(jurossimples=jurossimples).first()
        dados = request.json
        if 'jurossimples' in dados:
            juros_simples.jurossimples = dados['jurossimples']

        if 'capital' in dados:
            juros_simples.capital = dados['capital']

        if 'taxa' in dados:
            juros_simples.taxa = dados['taxa']

        if 'tempo' in dados:
            juros_simples.taxa = dados['tempo']

        juros_simples.save()
        response = {
            'id': juros_simples.id,
            'jurossimples': juros_simples.jurossimples,
            'capital': juros_simples.capital,
            'taxa': juros_simples.taxa,
            'tempo': juros_simples.tempo
        }

        return response

    def delete(self, id):
        jurossimples = Operacoes.query.filter_by(id=id).first()
        mensagem = 'Juros {} excluidos com sucesso'.format(jurossimples)
        jurossimples.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaOperacoes(Resource):

    def get(self):
        juros_simples = Operacoes.query.all()
        response = [{
            'id': i.id,
            'jurossimples': i.jurossimples,
            'capital': i.capital,
            'taxa': i.taxa,
            'tempo': i.tempo
        } for i in juros_simples]
        return response

    # J = C * i * t

    def post(self):
        dados = request.json
        # calcular o Juros
        if dados['capital'] and dados['taxa'] and dados['tempo'] > 0:
            juros_simples = Operacoes(
                id=dados['id'],
                jurossimples=dados['capital'] * (dados['taxa'] / 100) * dados['tempo'],
                capital=dados['capital'],
                taxa=dados['taxa'],
                tempo=dados['tempo']
            )
        # calcular a taxa
        if dados['jurossimples'] and dados['capital'] and dados['tempo'] > 0:
            juros_simples = Operacoes(
                id=dados['id'],
                jurossimples=dados['jurossimples'],
                capital=dados['capital'],
                taxa=dados['jurossimples'] / dados['capital'] * dados['tempo'],
                tempo=dados['tempo']
            )
        # calcular o capital
        if dados['jurossimples'] and dados['taxa'] and dados['tempo'] > 0:
            juros_simples = Operacoes(
                id=dados['id'],
                jurossimples=dados['jurossimples'],
                capital=dados['jurossimples'] / dados['tempo'] * (dados['taxa'] / 100),
                taxa=dados['taxa'],
                tempo=dados['tempo']
            )
        # calcular o tempo
        if dados['jurossimples'] and dados['capital'] and dados['taxa'] > 0:
            juros_simples = Operacoes(
                id=dados['id'],
                jurossimples=dados['jurossimples'],
                capital=dados['capital'],
                taxa=dados['taxa'],
                tempo=dados['jurossimples'] / dados['capital'] * (dados['taxa'] / 100)
            )
        juros_simples.save()
        response = {
            'id': juros_simples.id,
            'jurossimples': juros_simples.jurossimples,
            'capital': juros_simples.capital,
            'taxa': juros_simples.taxa,
            'tempo': juros_simples.tempo
        }
        return response


# calcular taxa nominal e taxa efetiva

class TaxaNominal(Resource):
    def get(self, taxanominal):
        taxa_nominal = OperacaoTaxaNominal.query.filter_by(taxanominal=taxanominal).first()
        try:
            response = {
                'taxanominal': taxa_nominal.taxa,
                'valor_emprestimo': taxa_nominal.valor_emprestimo,
                'valor_quitacao': taxa_nominal.valor_quitacao
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Taxa não encontrada'
            }
        return response

    def put(self, taxanominal):
        taxa_nominal = OperacaoTaxaNominal.query.filter_by(taxanominal=taxanominal).first()
        dados = request.json
        if 'valor_emprestimo' in dados:
            taxa_nominal.valor_emprestimo = dados['valor_emprestimo']

        if 'valor_quitacao' in dados:
            taxa_nominal.valor_quitacao = dados['valor_quitacao']

        if 'taxa' in dados:
            taxa_nominal.taxa = dados['taxa']

        taxa_nominal.save()
        response = {
            'id': taxa_nominal.id,
            'valor_emprestimo': taxa_nominal.valor_emprestimo,
            'valor_quitacao': taxa_nominal.valor_quitacao,
            'taxa': taxa_nominal.taxa
        }

        return response

    def delete(self, taxanominal):
        taxa_nominal = OperacaoJuroComposto.query.filter_by(id=taxanominal).first()
        mensagem = 'Juros {} excluidos com sucesso'.format(taxa_nominal)
        taxa_nominal.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaTaxaNominal(Resource):

    def get(self):
        taxa_nominal = OperacaoTaxaNominal.query.all()
        response = [{
            'id': i.id,
            'valor_emprestimo': i.valor_emprestimo,
            'valor_quitacao': i.valor_quitacao,
            'taxa': i.taxa
        } for i in taxa_nominal]
        return response

    # taxa nominal = Juros (valor quitacao - valor emprestimo) / valor emprestimo

    def post(self):
        dados = request.json
        # calcular a taxa
        if dados['valor_emprestimo'] and dados['valor_quitacao'] > 0:
            taxa_nominal = OperacaoTaxaNominal(
                id=dados['id'],
                taxa=(dados['valor_quitacao'] - dados['valor_emprestimo']) / dados['valor_emprestimo'],
                valor_emprestimo=dados['valor_emprestimo'],
                valor_quitacao=dados['valor_quitacao']
            )
        # calcular o valor da quitação
        if dados['valor_emprestimo'] and dados['taxa'] > 0:
            taxa_nominal = OperacaoTaxaNominal(
                id=dados['id'],
                taxa=dados['taxa'],
                valor_emprestimo=dados['valor_emprestimo'],
                valor_quitacao=(dados['valor_emprestimo'] * dados['taxa']) + dados['valor_emprestimo']
            )
        # calcular o valor emprestimo
        # if dados['valor_emprestimo'] and dados['taxa'] > 0:
        #    juros_simples = Operacoes(
        #        id=dados['id'],
        #        taxa=dados['taxa'],
        #        valor_emprestimo=(dados['valor_quitacao'] * dados['taxa']) + dados['valor_emprestimo'],
        #        valor_quitacao=dados['valor_quitacao']
        #    )

        taxa_nominal.save()
        response = {
            'id': taxa_nominal.id,
            'valor_emprestimo': taxa_nominal.valor_emprestimo,
            'valor_quitacao': taxa_nominal.valor_quitacao,
            'taxa': taxa_nominal.taxa
        }
        return response


class TaxaEfetiva(Resource):
    def get(self, taxaefetiva):
        taxa_efetiva = OperacaoTaxaEfetiva.query.filter_by(taxaefetiva=taxaefetiva).first()
        try:
            response = {
                'taxa_efetiva': taxa_efetiva.taxa_efetiva,
                'taxa_nominal': taxa_efetiva.taxa_nominal,
                'quantidade_periodos': taxa_efetiva.quantidade_periodos
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Taxa não encontrada'
            }
        return response

    def put(self, taxaefetiva):
        taxa_efetiva = OperacaoTaxaEfetiva.query.filter_by(taxaefetiva=taxaefetiva).first()
        dados = request.json
        if 'taxa_efetiva' in dados:
            taxa_efetiva.taxa_efetiva = dados['taxa_efetiva']

        if 'taxa_nominal' in dados:
            taxa_efetiva.taxa_nominal = dados['taxa_nominal']

        if 'quantidade_periodos' in dados:
            taxa_efetiva.quantidade_periodos = dados['quantidade_periodos']

        taxa_efetiva.save()
        response = {
            'id': taxa_efetiva.id,
            'taxa_efetiva': taxa_efetiva.taxa_efetiva,
            'taxa_nominal': taxa_efetiva.taxa_nominal,
            'quantidade_periodos': taxa_efetiva.quantidade_periodos
        }

        return response

    def delete(self, taxaefetiva):
        taxa_efetiva = OperacaoJuroComposto.query.filter_by(id=taxaefetiva).first()
        mensagem = 'Taxa efetiva {} excluida com sucesso'.format(taxa_efetiva)
        taxa_efetiva.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaTaxaEfetiva(Resource):

    def get(self):
        taxa_efetiva = OperacaoTaxaEfetiva.query.all()
        response = [{
            'id': i.id,
            'taxa_nominal': i.taxa_nominal,
            'taxa_efetiva': i.taxa_efetiva,
            'quantidade_periodos': i.quantidade_periodos
        } for i in taxa_efetiva]
        return response

    # Tendo em mente a taxa de juros declarada, utilize a seguinte fórmula: r = (1 + i/n)^n – 1, \\\
    # em que r é a taxa de juros efetiva, i, a nominal, e n, a quantidade de períodos compostos no período de um ano.
    def post(self):
        dados = request.json
        # calcular a taxa
        if dados['taxa_nominal'] and dados['quantidade_periodos'] > 0:
            taxa_efetiva = OperacaoTaxaEfetiva(
                id=dados['id'],
                taxa_efetiva=pow(1 + dados['taxa_nominal'] / dados['quantidade_periodos'],
                                 dados['quantidade_periodos']) - 1,
                taxa_nominal=dados['taxa_nominal'],
                quantidade_periodos=dados['quantidade_periodos']
            )

        taxa_efetiva.save()
        response = {
            'id': taxa_efetiva.id,
            'taxa_efetiva': taxa_efetiva.taxa_efetiva,
            'taxa_nominal': taxa_efetiva.taxa_nominal,
            'quantidade_periodos': taxa_efetiva.quantidade_periodos
        }
        return response


class TaxaJurosReal(Resource):
    def get(self, taxajurosreal):
        taxa_real = OperacaoTaxaEfetiva.query.filter_by(taxajurosreal=taxajurosreal).first()
        try:
            response = {
                'taxa_real': taxa_real.taxa_real,
                'taxa_nominal': taxa_real.taxa_nominal,
                'inflacao_periodo': taxa_real.inflacao_periodo
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Taxa não encontrada'
            }
        return response

    def put(self, taxaefetiva):
        taxa_real = OperacaoTaxaEfetiva.query.filter_by(taxaefetiva=taxaefetiva).first()
        dados = request.json
        if 'taxa_real' in dados:
            taxa_real.taxa_real = dados['taxa_real']

        if 'taxa_nominal' in dados:
            taxa_real.taxa_nominal = dados['taxa_nominal']

        if 'inflacao_periodo' in dados:
            taxa_real.inflacao_periodo = dados['inflacao_periodo']

        taxa_real.save()
        response = {
            'id': taxa_real.id,
            'taxa_efetiva': taxa_real.taxa_real,
            'taxa_nominal': taxa_real.taxa_nominal,
            'quantidade_periodos': taxa_real.inflacao_periodo
        }

        return response

    def delete(self, taxareal):
        taxa_real = OperacaoJuroComposto.query.filter_by(id=taxareal).first()
        mensagem = 'Taxa efetiva {} excluida com sucesso'.format(taxa_real)
        taxa_real.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaTaxaReal(Resource):

    def get(self):
        taxa_real = OperacaoTaxaJurosReal.query.all()
        response = [{
            'id': i.id,
            'taxa_nominal': i.taxa_nominal,
            'taxa_real': i.taxa_real,
            'inflacao_periodo': i.inflacao_periodo
        } for i in taxa_real]
        return response

    # taxa de juros real
    # (1 + in) = (1 + r) × (1 + j)
    # in: taxa de juros nominal
    # r: taxa de juros real
    # j: inflação do período.
    def post(self):
        dados = request.json
        # calcular a taxa
        if dados['taxa_nominal'] and dados['inflacao_periodo'] > 0:
            taxa_real = OperacaoTaxaJurosReal(
                id=dados['id'],
                taxa_real=(1 + dados['taxa_nominal']) / (1 + dados['inflacao_periodo']) - 1,
                taxa_nominal=dados['taxa_nominal'],
                inflacao_periodo=dados['inflacao_periodo']
            )

        taxa_real.save()
        response = {
            'id': taxa_real.id,
            'taxa_real': taxa_real.taxa_real,
            'taxa_nominal': taxa_real.taxa_nominal,
            'inflacao_periodo': taxa_real.inflacao_periodo
        }
        return response


class FormacaoCapital(Resource):
    def get(self, fatoracumulado):
        fator_acumulado = FatorAcumulacaoCapital.query.filter_by(fatoracumulado=fatoracumulado).first()
        try:
            response = {
                'fator_acumulado': fator_acumulado.fator_acumulado,
                'taxa': fator_acumulado.taxa,
                'tempo': fator_acumulado.tempo,
                'montante_composto': fator_acumulado.montante_composto
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'fator acumulado não encontrada'
            }
        return response

    def put(self, fatoracumulado):
        fator_acumulado = FatorAcumulacaoCapital.query.filter_by(fatoracumulado=fatoracumulado).first()
        dados = request.json
        if 'fator_acumulado' in dados:
            fator_acumulado.fator_acumulado = dados['fator_acumulado']

        if 'taxa' in dados:
            fator_acumulado.taxa = dados['taxa']

        if 'tempo' in dados:
            fator_acumulado.tempo = dados['tempo']

        if 'montante_composto' in dados:
            fator_acumulado.montante_composto = dados['montante_composto']

        fator_acumulado.save()
        response = {
            'id': fator_acumulado.id,
            'fator_acumulado': fator_acumulado.fator_acumulado,
            'taxa': fator_acumulado.taxa,
            'tempo': fator_acumulado.tempo,
            'montante_composto': fator_acumulado.montante_composto
        }

        return response

    def delete(self, fatoracumulado):
        fator_acumulado = OperacaoJuroComposto.query.filter_by(id=fatoracumulado).first()
        mensagem = 'fator acumulado {} excluido com sucesso'.format(fator_acumulado)
        fator_acumulado.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaFormacaoCapital(Resource):

    def get(self):
        fator_acumulado = FatorAcumulacaoCapital.query.all()
        response = [{
            'id': i.id,
            'fator_acumulado': i.fator_acumulado,
            'taxa': i.taxa,
            'tempo': i.tempo,
            'montante_composto': i.montante_composto
        } for i in fator_acumulado]
        return response

    # P=S(1+i)**−n
    # S = montante composto
    def post(self):
        dados = request.json
        if dados['taxa'] and dados['tempo'] > 0:
            fator_acumulado = FatorAcumulacaoCapital(
                id=dados['id'],
                fator_acumulado=(1 + dados['montante_composto']) / (1 + dados['inflacao_periodo']) - 1,
                taxa=dados['taxa_nominal'],
                tempo=dados['inflacao_periodo'],
                montante_composto=dados['montante_composto']
            )

        fator_acumulado.save()
        response = {
            'id': fator_acumulado.id,
            'fator_acumulado': fator_acumulado.fator_acumulado,
            'taxa': fator_acumulado.taxa,
            'tempo': fator_acumulado.tempo,
            'montante_composto': fator_acumulado.montante_composto
        }
        return response


class CalculoDescSimples(Resource):
    def get(self, descontosimples):
        desconto_simples = DescontoSimples.query.filter_by(descontosimples=descontosimples).first()
        try:
            response = {
                'desconto_simples': desconto_simples.desconto_simples,
                'montante': desconto_simples.montante,
                'taxa': desconto_simples.taxa,
                'tempo': desconto_simples.tempo,
                'valor_atual': desconto_simples.valor_atual
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'fator acumulado não encontrada'
            }
        return response

    def put(self, descontosimples):
        desconto_simples = DescontoSimples.query.filter_by(descontosimples=descontosimples).first()
        dados = request.json
        if 'desconto_simples' in dados:
            desconto_simples.desconto_simples = dados['desconto_simples']

        if 'montante' in dados:
            desconto_simples.montante = dados['montante']

        if 'taxa' in dados:
            desconto_simples.taxa = dados['taxa']

        if 'tempo' in dados:
            desconto_simples.tempo = dados['tempo']

        if 'valor_atual' in dados:
            desconto_simples.valor_atual = dados['valor_atual']

        desconto_simples.save()
        response = {
            'id': desconto_simples.id,
            'desconto_simples': desconto_simples.desconto_simples,
            'montante': desconto_simples.montante,
            'taxa': desconto_simples.taxa,
            'tempo': desconto_simples.tempo,
            'valor_atual': desconto_simples.valor_atual
        }

        return response

    def delete(self, descontosimples):
        desconto_simples = DescontoSimples.query.filter_by(id=descontosimples).first()
        mensagem = 'fator acumulado {} excluido com sucesso'.format(desconto_simples)
        desconto_simples.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaDescontoSimples(Resource):

    def get(self):
        desconto_simples = DescontoSimples.query.all()
        response = [{
            'id': i.id,
            'desconto_simples': i.desconto_simples,
            'montante': i.montante,
            'taxa': i.taxa,
            'tempo': i.tempo,
            'valor_atual': i.valor_atual
        } for i in desconto_simples]
        return response

    # Dr = A . i . t          A = N / (1 + i.t)
    #
    # Onde:
    #
    # Dr = desconto racional
    #
    # N = valor nominal
    #
    # i = taxa
    #
    # t = tempo
    #
    # A = valor atual
    def post(self):
        dados = request.json
        if dados['taxa'] and dados['tempo'] and dados['montante'] > 0:
            desconto_simples = DescontoSimples(
                id=dados['id'],
                desconto_simples=(dados['montante'] * (dados['taxa'] / 100) * dados['tempo']),
                montante=dados['montante'],
                taxa=dados['taxa'],
                tempo=dados['tempo'],
                valor_atual=dados['montante'] / (1 + (dados['taxa'] / 100) * dados['tempo'])
            )

        desconto_simples.save()
        response = {
            'id': desconto_simples.id,
            'desconto_simples': desconto_simples.desconto_simples,
            'montante': desconto_simples.montante,
            'taxa': desconto_simples.taxa,
            'tempo': desconto_simples.tempo,
            'valor_atual': desconto_simples.valor_atual
        }
        return response


class CalculoDescComposto(Resource):
    def get(self, descontocomposto):
        desconto_composto = DescontoComposto.query.filter_by(descontocomposto=descontocomposto).first()
        try:
            response = {
                'desconto_composto': desconto_composto.desconto_composto,
                'montante': desconto_composto.montante,
                'taxa': desconto_composto.taxa,
                'tempo': desconto_composto.tempo,
                'valor_atual': desconto_composto.valor_atual
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'fator acumulado não encontrada'
            }
        return response

    def put(self, descontocomposto):
        desconto_composto = DescontoComposto.query.filter_by(descontocomposto=descontocomposto).first()
        dados = request.json
        if 'desconto_composto' in dados:
            desconto_composto.desconto_composto = dados['desconto_composto']

        if 'montante' in dados:
            desconto_composto.montante = dados['montante']

        if 'taxa' in dados:
            desconto_composto.taxa = dados['taxa']

        if 'tempo' in dados:
            desconto_composto.tempo = dados['tempo']

        if 'valor_atual' in dados:
            desconto_composto.valor_atual = dados['valor_atual']

        desconto_composto.save()
        response = {
            'id': desconto_composto.id,
            'desconto_composto': desconto_composto.desconto_simples,
            'montante': desconto_composto.montante,
            'taxa': desconto_composto.taxa,
            'tempo': desconto_composto.tempo,
            'valor_atual': desconto_composto.valor_atual
        }

        return response

    def delete(self, descontocomposto):
        desconto_composto = DescontoComposto.query.filter_by(id=descontocomposto).first()
        mensagem = 'fator acumulado {} excluido com sucesso'.format(desconto_composto)
        desconto_composto.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaDescontoComposto(Resource):

    def get(self):
        desconto_composto = DescontoComposto.query.all()
        response = [{
            'id': i.id,
            'desconto_composto': i.desconto_composto,
            'montante': i.montante,
            'taxa': i.taxa,
            'tempo': i.tempo,
            'valor_atual': i.valor_atual
        } for i in desconto_composto]
        return response

    # DC = N . i . t        A = N . (1 – i)**t

    def post(self):
        dados = request.json
        if dados['taxa'] and dados['tempo'] and dados['montante'] > 0:
            desconto_composto = DescontoComposto(
                id=dados['id'],
                desconto_composto=dados['montante'] - (
                        dados['montante'] * (pow(1 - (dados['taxa'] / 100), dados['tempo']))),
                montante=dados['montante'],
                taxa=dados['taxa'],
                tempo=dados['tempo'],
                valor_atual=dados['montante'] * pow(1 - (dados['taxa'] / 100), dados['tempo'])
            )

        desconto_composto.save()
        response = {
            'id': desconto_composto.id,
            'desconto_composto': desconto_composto.desconto_composto,
            'montante': desconto_composto.montante,
            'taxa': desconto_composto.taxa,
            'tempo': desconto_composto.tempo,
            'valor_atual': desconto_composto.valor_atual
        }
        return response


class CalculoPrestacaoConstante(Resource):
    def get(self, prestacaoconstante):
        prestacao_constante = SistemaPrestacaoConstante.query.filter_by(prestacaoconstante=prestacaoconstante).first()
        try:
            response = {
                'saldo_devedor': prestacao_constante.saldo_devedor,
                'amortizacao': prestacao_constante.amortizacao,
                'taxa': prestacao_constante.taxa,
                'tempo': prestacao_constante.tempo,
                'prestacao': prestacao_constante.valor_atual
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'fator acumulado não encontrada'
            }
        return response

    def put(self, prestacaoconstante):
        prestacao_constante = SistemaPrestacaoConstante.query.filter_by(prestacaoconstante=prestacaoconstante).first()
        dados = request.json
        if 'saldo_devedor' in dados:
            prestacao_constante.saldo_devedor = dados['saldo_devedor']

        if 'amortizacao' in dados:
            prestacao_constante.amortizacao = dados['amortizacao']

        if 'taxa' in dados:
            prestacao_constante.taxa = dados['taxa']

        if 'tempo' in dados:
            prestacao_constante.tempo = dados['tempo']

        if 'prestacao' in dados:
            prestacao_constante.prestacao = dados['prestacao']

        prestacao_constante.save()
        response = {
            'id': prestacao_constante.id,
            'saldo_devedor': prestacao_constante.saldo_devedor,
            'amortizacao': prestacao_constante.amortizacao,
            'taxa': prestacao_constante.taxa,
            'tempo': prestacao_constante.tempo,
            'prestacao': prestacao_constante.prestacao
        }

        return response

    def delete(self, prestacaoconstante):
        prestacao_constante = SistemaPrestacaoConstante.query.filter_by(id=prestacaoconstante).first()
        mensagem = 'fator acumulado {} excluido com sucesso'.format(prestacao_constante)
        prestacao_constante.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaPrestacaoConstante(Resource):

    def get(self):
        prestacao_constante = SistemaPrestacaoConstante.query.all()
        response = [{
            'id': i.id,
            'saldo_devedor': i.saldo_devedor,
            'amortizacao': i.amortizacao,
            'taxa': i.taxa,
            'tempo': i.tempo,
            'prestacao': i.prestacao
        } for i in prestacao_constante]
        return response

    def post(self):
        dados = request.json
        if dados['taxa'] and dados['tempo'] and dados['saldo_devedor'] > 0:
            prestacao_constante = SistemaPrestacaoConstante(
                id=dados['id'],
                saldo_devedor=dados['saldo_devedor'],
                amortizacao=dados['saldo_devedor'] / dados['tempo'],
                taxa=dados['taxa'],
                tempo=dados['tempo'],
                prestacao=(dados['saldo_devedor'] / dados['tempo']) + (dados['taxa'] / 100 * dados['saldo_devedor'])
            )

        prestacao_constante.save()
        response = {
            'id': prestacao_constante.id,
            'saldo_devedor': prestacao_constante.saldo_devedor,
            'amortizacao': prestacao_constante.amortizacao,
            'taxa': prestacao_constante.taxa,
            'tempo': prestacao_constante.tempo,
            'prestacao': prestacao_constante.prestacao
        }
        return response


class CalculoAmortizacaoConstante(Resource):
    def get(self, amortizacaoconstante):
        amortizacao_constante = SistemaAmortizacaoConstante.query.filter_by(
            amortizacaoconstante=amortizacaoconstante).first()
        try:
            response = {
                'saldo_devedor': amortizacao_constante.saldo_devedor,
                'amortizacao': amortizacao_constante.amortizacao,
                'taxa': amortizacao_constante.taxa,
                'tempo': amortizacao_constante.tempo,
                'prestacao': amortizacao_constante.valor_atual
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'fator acumulado não encontrada'
            }
        return response

    def put(self, amortizacaoconstante):
        amortizacao_constante = SistemaAmortizacaoConstante.query.filter_by(
            amortizacaoconstante=amortizacaoconstante).first()
        dados = request.json
        if 'saldo_devedor' in dados:
            amortizacao_constante.saldo_devedor = dados['saldo_devedor']

        if 'amortizacao' in dados:
            amortizacao_constante.amortizacao = dados['amortizacao']

        if 'taxa' in dados:
            amortizacao_constante.taxa = dados['taxa']

        if 'tempo' in dados:
            amortizacao_constante.tempo = dados['tempo']

        if 'prestacao' in dados:
            amortizacao_constante.prestacao = dados['prestacao']

        amortizacao_constante.save()
        response = {
            'id': amortizacao_constante.id,
            'saldo_devedor': amortizacao_constante.saldo_devedor,
            'amortizacao': amortizacao_constante.amortizacao,
            'taxa': amortizacao_constante.taxa,
            'tempo': amortizacao_constante.tempo,
            'prestacao': amortizacao_constante.prestacao
        }

        return response

    def delete(self, amortizacaoconstante):
        amortizacao_constante = SistemaAmortizacaoConstante.query.filter_by(id=amortizacaoconstante).first()
        mensagem = 'fator acumulado {} excluido com sucesso'.format(amortizacao_constante)
        amortizacao_constante.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaAmortizacaoConstante(Resource):

    def get(self):
        amortizacao_constante = SistemaAmortizacaoConstante.query.all()
        response = [{
            'id': i.id,
            'saldo_devedor': i.saldo_devedor,
            'amortizacao': i.amortizacao,
            'taxa': i.taxa,
            'tempo': i.tempo,
            'prestacao': i.prestacao
        } for i in amortizacao_constante]
        return response

    def post(self):
        dados = request.json
        if dados['taxa'] and dados['tempo'] and dados['saldo_devedor'] > 0:
            amortizacao_constante = SistemaAmortizacaoConstante(
                id=dados['id'],
                saldo_devedor=dados['saldo_devedor'],
                amortizacao=dados['saldo_devedor'] / dados['tempo'],
                taxa=dados['taxa'],
                tempo=dados['tempo'],
                prestacao=(dados['saldo_devedor'] * (dados['taxa'] / 100)) + (dados['saldo_devedor'] / dados['tempo'])
            )

        amortizacao_constante.save()
        response = {
            'id': amortizacao_constante.id,
            'saldo_devedor': amortizacao_constante.saldo_devedor,
            'amortizacao': amortizacao_constante.amortizacao,
            'taxa': amortizacao_constante.taxa,
            'tempo': amortizacao_constante.tempo,
            'prestacao': amortizacao_constante.prestacao
        }
        return response


class CalculoAnaliseHorizontal(Resource):
    def get(self, analisehorizontal):
        analise_horizontal = AnaliseHorizontal.query.filter_by(
            analisehorizontal=analisehorizontal).first()
        try:
            response = {
                'receita_base': analise_horizontal.receita_base,
                'custo_base': analise_horizontal.custo_base,
                'periodo_base': analise_horizontal.periodo_base,
                'receita_atual': analise_horizontal.receita_atual,
                'custo_atual': analise_horizontal.custo_atual,
                'periodo_atual': analise_horizontal.periodo_atual,
                'resultado_bruto': analise_horizontal.resultado_bruto,
                'variacao_receita': analise_horizontal.variacao_receita,
                'variacao_custo': analise_horizontal.variacao_custo,
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'analise horizontal não encontrada'
            }
        return response

    def put(self, analisehorizontal):
        analise_horizontal = AnaliseHorizontal.query.filter_by(
            analisehorizontal=analisehorizontal).first()
        dados = request.json
        if 'receita_base' in dados:
            analise_horizontal.receita_base = dados['receita_base']

        if 'custo_base' in dados:
            analise_horizontal.custo_base = dados['custo_base']

        if 'periodo_base' in dados:
            analise_horizontal.periodo_base = dados['periodo_base']

        if 'receita_atual' in dados:
            analise_horizontal.receita_atual = dados['receita_atual']

        if 'custo_atual' in dados:
            analise_horizontal.custo_atual = dados['custo_atual']

        if 'periodo_atual' in dados:
            analise_horizontal.periodo_atual = dados['periodo_atual']

        if 'resultado_bruto' in dados:
            analise_horizontal.resultado_bruto = dados['resultado_bruto']

        if 'variacao_receita' in dados:
            analise_horizontal.variacao_receita = dados['variacao_receita']

        if 'variacao_custo' in dados:
            analise_horizontal.variacao_custo = dados['variacao_custo']

        analise_horizontal.save()
        response = {
            'id': analise_horizontal.id,
            'receita_base': analise_horizontal.receita_base,
            'custo_base': analise_horizontal.custo_base,
            'periodo_base': analise_horizontal.periodo_base,
            'receita_atual': analise_horizontal.receita_atual,
            'custo_atual': analise_horizontal.custo_atual,
            'periodo_atual': analise_horizontal.periodo_atual,
            'resultado_bruto': analise_horizontal.resultado_bruto,
            'variacao_receita': analise_horizontal.variacao_receita,
            'variacao_custo': analise_horizontal.variacao_custo
        }

        return response

    def delete(self, analisehorizontal):
        analise_horizontal = AnaliseHorizontal.query.filter_by(id=analisehorizontal).first()
        mensagem = 'fator acumulado {} excluido com sucesso'.format(analise_horizontal)
        analise_horizontal.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaAnaliseHorizontal(Resource):

    def get(self):
        analise_horizontal = AnaliseHorizontal.query.all()
        response = [{
            'id': i.id,
            'receita_base': i.receita_base,
            'custo_base': i.custo_base,
            'periodo_base': i.periodo_base,
            'receita_atual': i.receita_atual,
            'custo_atual': i.custo_atual,
            'periodo_atual': i.periodo_atual,
            'resultado_bruto': i.resultado_bruto,
            'variacao_receita': i.variacao_receita,
            'variacao_custo': i.variacao_custo,
        } for i in analise_horizontal]
        return response

    def post(self):
        dados = request.json
        if dados['receita_base'] and dados['custo_base'] and dados['periodo_base'] > 0:
            analise_horizontal = AnaliseHorizontal(
                id=dados['id'],
                receita_base=dados['receita_base'],
                custo_base=dados['custo_base'],
                periodo_base=dados['periodo_base'],
                receita_atual=dados['receita_atual'],
                custo_atual=dados['custo_atual'],
                periodo_atual=dados['periodo_atual'],
                resultado_bruto=dados['receita_base'] - dados['custo_base'],
                variacao_receita=(dados['receita_atual'] / dados['receita_base']) * 100,
                variacao_custo=(dados['custo_atual'] / dados['custo_base']) * 100
            )

        analise_horizontal.save()
        response = {
            'id': analise_horizontal.id,
            'receita_base': analise_horizontal.receita_base,
            'custo_base': analise_horizontal.custo_base,
            'periodo_base': analise_horizontal.periodo_base,
            'receita_atual': analise_horizontal.receita_atual,
            'custo_atual': analise_horizontal.custo_atual,
            'periodo_atual': analise_horizontal.periodo_atual,
            'resultado_bruto': analise_horizontal.resultado_bruto,
            'variacao_receita': analise_horizontal.variacao_receita,
            'variacao_custo': analise_horizontal.variacao_custo
        }
        return response


class CalculoAnaliseVertical(Resource):
    def get(self, analisevertical):
        analise_vertical = AnaliseVertical.query.filter_by(
            id=analisevertical).first()
        try:
            response = {
                'receita_base': analise_vertical.receita_base,
                'custo_base': analise_vertical.custo_base,
                'periodo_base': analise_vertical.periodo_base,
                'receita_atual': analise_vertical.receita_atual,
                'custo_atual': analise_vertical.custo_atual,
                'periodo_atual': analise_vertical.periodo_atual,
                'resultado_bruto': analise_vertical.resultado_bruto,
                'variacao_receita': analise_vertical.variacao_receita,
                'variacao_custo': analise_vertical.variacao_custo,
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'analise vertical não encontrada'
            }
        return response

    def put(self, analisevertical):
        analise_vertical = AnaliseVertical.query.filter_by(
            analisevertical=analisevertical).first()
        dados = request.json
        if 'receita_base' in dados:
            analise_vertical.receita_base = dados['receita_base']

        if 'custo_base' in dados:
            analise_vertical.custo_base = dados['custo_base']

        if 'periodo_base' in dados:
            analise_vertical.periodo_base = dados['periodo_base']

        if 'receita_atual' in dados:
            analise_vertical.receita_atual = dados['receita_atual']

        if 'custo_atual' in dados:
            analise_vertical.custo_atual = dados['custo_atual']

        if 'periodo_atual' in dados:
            analise_vertical.periodo_atual = dados['periodo_atual']

        if 'resultado_bruto' in dados:
            analise_vertical.resultado_bruto = dados['resultado_bruto']

        if 'variacao_receita' in dados:
            analise_vertical.variacao_receita = dados['variacao_receita']

        if 'variacao_custo' in dados:
            analise_vertical.variacao_custo = dados['variacao_custo']

        analise_vertical.save()
        response = {
            'id': analise_vertical.id,
            'receita_base': analise_vertical.receita_base,
            'custo_base': analise_vertical.custo_base,
            'periodo_base': analise_vertical.periodo_base,
            'receita_atual': analise_vertical.receita_atual,
            'custo_atual': analise_vertical.custo_atual,
            'periodo_atual': analise_vertical.periodo_atual,
            'resultado_bruto': analise_vertical.resultado_bruto,
            'variacao_receita': analise_vertical.variacao_receita,
            'variacao_custo': analise_vertical.variacao_custo
        }

        return response

    def delete(self, analisevertical):
        analise_vertical = AnaliseVertical.query.filter_by(id=analisevertical).first()
        mensagem = 'fator acumulado {} excluido com sucesso'.format(analise_vertical)
        analise_vertical.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaAnaliseVertical(Resource):

    def get(self):
        analise_vertical = AnaliseVertical.query.all()
        response = [{
            'id': i.id,
            'receita_base': i.receita_base,
            'custo_base': i.custo_base,
            'periodo_base': i.periodo_base,
            'receita_atual': i.receita_atual,
            'custo_atual': i.custo_atual,
            'periodo_atual': i.periodo_atual,
            'resultado_bruto': i.resultado_bruto,
            'variacao_receita': i.variacao_receita,
            'variacao_custo': i.variacao_custo,
        } for i in analise_vertical]
        return response

    def post(self):
        dados = request.json
        if dados['receita_base'] and dados['custo_base'] and dados['periodo_base'] > 0:
            analise_vertical = AnaliseVertical(
                id=dados['id'],
                receita_base=dados['receita_base'],
                custo_base=dados['custo_base'],
                periodo_base=dados['periodo_base'],
                receita_atual=dados['receita_atual'],
                custo_atual=dados['custo_atual'],
                periodo_atual=dados['periodo_atual'],
                resultado_bruto=dados['receita_base'] - dados['custo_base'],
                variacao_receita=(dados['receita_base'] / dados['custo_base']) * 100,
                variacao_custo=(dados['receita_atual'] / dados['custo_atual']) * 100
            )

        analise_vertical.save()
        response = {
            'id': analise_vertical.id,
            'receita_base': analise_vertical.receita_base,
            'custo_base': analise_vertical.custo_base,
            'periodo_base': analise_vertical.periodo_base,
            'receita_atual': analise_vertical.receita_atual,
            'custo_atual': analise_vertical.custo_atual,
            'periodo_atual': analise_vertical.periodo_atual,
            'resultado_bruto': analise_vertical.resultado_bruto,
            'variacao_receita': analise_vertical.variacao_receita,
            'variacao_custo': analise_vertical.variacao_custo
        }
        return response


class CalculoLiquidezImediata(Resource):
    def get(self, liquidezimediata):
        liquidez_imediata = LiquidezImediata.query.filter_by(
            id=liquidezimediata).first()
        try:
            response = {
                'caixa': liquidez_imediata.caixa,
                'equivalentes_caixa': liquidez_imediata.equivalentes_caixa,
                'liquidez_imediata': liquidez_imediata.liquidez_imediata,
                'passivo_circulante': liquidez_imediata.passivo_circulante,
                'resultado': liquidez_imediata.resultado
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'liquidez imediata não encontrada'
            }
        return response

    def put(self, liquidezimediata):
        liquidez_imediata = LiquidezImediata.query.filter_by(
            liquidezimediata=liquidezimediata).first()
        dados = request.json

        if 'caixa' in dados:
            liquidez_imediata.caixa = dados['caixa']

        if 'equivalentes_caixa' in dados:
            liquidez_imediata.equivalentes_caixa = dados['equivalentes_caixa']

        if 'liquidez_imediata' in dados:
            liquidez_imediata.liquidez_imediata = dados['liquidez_imediata']

        if 'passivo_circulante' in dados:
            liquidez_imediata.passivo_circulante = dados['passivo_circulante']

        if 'resultado' in dados:
            liquidez_imediata.resultado = dados['resultado']

        liquidez_imediata.save()
        response = {
            'id': liquidez_imediata.id,
            'caixa': liquidez_imediata.caixa,
            'equivalentes_caixa': liquidez_imediata.equivalentes_caixa,
            'liquidez_imediata': liquidez_imediata.liquidez_imediata,
            'passivo_circulante': liquidez_imediata.passivo_circulante,
            'resultado': liquidez_imediata.resultado
        }

        return response

    def delete(self, liquidezimediata):
        liquidez_imediata = LiquidezImediata.query.filter_by(id=liquidezimediata).first()
        mensagem = 'Liquidez imediata {} excluida com sucesso'.format(liquidez_imediata)
        liquidez_imediata.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaLiquidezImediata(Resource):

    def get(self):
        liquidez_imediata = LiquidezImediata.query.all()
        response = [{
            'id': i.id,
            'caixa': i.caixa,
            'equivalentes_caixa': i.equivalentes_caixa,
            'liquidez_imediata': i.liquidez_imediata,
            'passivo_circulante': i.passivo_circulante,
            'resultado': i.resultado

        } for i in liquidez_imediata]
        return response

    def post(self):
        dados = request.json
        if dados['passivo_circulante'] > 0 < dados['caixa']:
            liquidez_imediata = LiquidezImediata(
                id=dados['id'],
                caixa=dados['caixa'],
                equivalentes_caixa=dados['equivalentes_caixa'],
                liquidez_imediata=(dados['caixa'] + dados['equivalentes_caixa']) / dados['passivo_circulante'] * 100,
                passivo_circulante=dados['passivo_circulante'],
                resultado="Bom grau de liquidez" if ((dados['caixa'] + dados['equivalentes_caixa']) / dados[
                    'passivo_circulante'] * 100) >= 100 else "Não tem como quitar dividas"
            )

        liquidez_imediata.save()
        response = {
            'id': liquidez_imediata.id,
            'caixa': liquidez_imediata.caixa,
            'equivalentes_caixa': liquidez_imediata.equivalentes_caixa,
            'liquidez_imediata': liquidez_imediata.liquidez_imediata,
            'passivo_circulante': liquidez_imediata.passivo_circulante,
            'resultado': liquidez_imediata.resultado
        }
        return response


class CalculoLiquidezCorrente(Resource):
    def get(self, liquidezcorrente):
        liquidez_corrente = LiquidezCorrente.query.filter_by(
            id=liquidezcorrente).first()
        try:
            response = {
                'ativo_circulante': liquidez_corrente.ativo_circulante,
                'liquidez_corrente': liquidez_corrente.liquidez_corrente,
                'passivo_circulante': liquidez_corrente.passivo_circulante,
                'resultado': liquidez_corrente.resultado
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'liquidez corrente não encontrada'
            }
        return response

    def put(self, liquidezcorrente):
        liquidez_corrente = LiquidezCorrente.query.filter_by(
            liquidezcorrente=liquidezcorrente).first()
        dados = request.json

        if 'ativo_circulante' in dados:
            liquidez_corrente.ativo_circulante = dados['ativo_circulante']

        if 'liquidez_corrente' in dados:
            liquidez_corrente.liquidez_corrente = dados['liquidez_corrente']

        if 'passivo_circulante' in dados:
            liquidez_corrente.passivo_circulante = dados['passivo_circulante']

        if 'resultado' in dados:
            liquidez_corrente.resultado = dados['resultado']

        liquidez_corrente.save()
        response = {
            'id': liquidez_corrente.id,
            'ativo_circulante': liquidez_corrente.ativo_circulante,
            'liquidez_corrente': liquidez_corrente.liquidez_corrente,
            'passivo_circulante': liquidez_corrente.passivo_circulante,
            'resultado': liquidez_corrente.resultado
        }

        return response

    def delete(self, liquidezcorrente):
        liquidez_corrente = LiquidezCorrente.query.filter_by(id=liquidezcorrente).first()
        mensagem = 'Liquidez corrente {} excluida com sucesso'.format(liquidez_corrente)
        liquidez_corrente.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaLiquidezCorrente(Resource):

    def get(self):
        liquidez_corrente = LiquidezCorrente.query.all()
        response = [{
            'id': i.id,
            'ativo_circulante': i.ativo_circulante,
            'liquidez_corrente': i.liquidez_corrente,
            'passivo_circulante': i.passivo_circulante,
            'resultado': i.resultado

        } for i in liquidez_corrente]
        return response

    def post(self):
        dados = request.json
        if dados['passivo_circulante'] > 0 < dados['ativo_circulante']:
            liquidez_corrente = LiquidezCorrente(
                id=dados['id'],
                ativo_circulante=dados['ativo_circulante'],
                liquidez_corrente=dados['ativo_circulante'] / dados['passivo_circulante'],
                passivo_circulante=dados['passivo_circulante'],
                resultado="Bom grau de liquidez corrente" if (dados['ativo_circulante'] / dados[
                    'passivo_circulante']) >= 1 else "Não tem como quitar dividas"
            )

        liquidez_corrente.save()
        response = {
            'id': liquidez_corrente.id,
            'ativo_circulante': liquidez_corrente.ativo_circulante,
            'liquidez_corrente': liquidez_corrente.liquidez_corrente,
            'passivo_circulante': liquidez_corrente.passivo_circulante,
            'resultado': liquidez_corrente.resultado
        }
        return response


class CalculoLiquidezSeca(Resource):
    def get(self, liquidezseca):
        liquidez_seca = LiquidezSeca.query.filter_by(
            id=liquidezseca).first()
        try:
            response = {
                'ativo_circulante': liquidez_seca.ativo_circulante,
                'estoques': liquidez_seca.estoques,
                'liquidez_seca': liquidez_seca.liquidez_seca,
                'passivo_circulante': liquidez_seca.passivo_circulante,
                'resultado': liquidez_seca.resultado
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'liquidez seca não encontrada'
            }
        return response

    def put(self, liquidezseca):
        liquidez_seca = LiquidezSeca.query.filter_by(
            liquidezseca=liquidezseca).first()
        dados = request.json

        if 'ativo_circulante' in dados:
            liquidez_seca.ativo_circulante = dados['ativo_circulante']

        if 'estoques' in dados:
            liquidez_seca.estoques = dados['estoques']

        if 'liquidez_seca' in dados:
            liquidez_seca.liquidez_seca = dados['liquidez_seca']

        if 'passivo_circulante' in dados:
            liquidez_seca.passivo_circulante = dados['passivo_circulante']

        if 'resultado' in dados:
            liquidez_seca.resultado = dados['resultado']

        liquidez_seca.save()
        response = {
            'id': liquidez_seca.id,
            'ativo_circulante': liquidez_seca.ativo_circulante,
            'estoques': liquidez_seca.estoques,
            'liquidez_seca': liquidez_seca.liquidez_seca,
            'passivo_circulante': liquidez_seca.passivo_circulante,
            'resultado': liquidez_seca.resultado
        }

        return response

    def delete(self, liquidezseca):
        liquidez_seca = LiquidezSeca.query.filter_by(id=liquidezseca).first()
        mensagem = 'Liquidez seca {} excluida com sucesso'.format(liquidez_seca)
        liquidez_seca.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaLiquidezSeca(Resource):

    def get(self):
        liquidez_seca = LiquidezSeca.query.all()
        response = [{
            'id': i.id,
            'ativo_circulante': i.ativo_circulante,
            'estoques': i.estoques,
            'liquidez_seca': i.liquidez_seca,
            'passivo_circulante': i.passivo_circulante,
            'resultado': i.resultado

        } for i in liquidez_seca]
        return response

    def post(self):
        dados = request.json
        if dados['passivo_circulante'] > 0 < dados['ativo_circulante']:
            liquidez_seca = LiquidezSeca(
                id=dados['id'],
                ativo_circulante=dados['ativo_circulante'],
                estoques=dados['estoques'],
                liquidez_seca=(dados['ativo_circulante'] - dados['estoques']) / dados['passivo_circulante'],
                passivo_circulante=dados['passivo_circulante'],
                resultado="Bom grau de liquidez seca" if ((dados['ativo_circulante'] - dados['estoques']) / dados[
                    'passivo_circulante']) >= 1 else "Não tem como quitar dividas"
            )

        liquidez_seca.save()
        response = {
            'id': liquidez_seca.id,
            'ativo_circulante': liquidez_seca.ativo_circulante,
            'estoques': liquidez_seca.estoques,
            'liquidez_seca': liquidez_seca.liquidez_seca,
            'passivo_circulante': liquidez_seca.passivo_circulante,
            'resultado': liquidez_seca.resultado
        }
        return response


class CalculoLiquidezGeral(Resource):
    def get(self, liquidezgeral):
        liquidez_geral = LiquidezGeral.query.filter_by(
            id=liquidezgeral).first()
        try:
            response = {
                'ativo_circulante': liquidez_geral.ativo_circulante,
                'realizavel_longo_prazo': liquidez_geral.realizavel_longo_prazo,
                'liquidez_geral': liquidez_geral.liquidez_geral,
                'passivo_circulante': liquidez_geral.passivo_circulante,
                'exigivel_longo_prazo': liquidez_geral.exigivel_longo_prazo,
                'resultado': liquidez_geral.resultado
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'liquidez geral não encontrada'
            }
        return response

    def put(self, liquidezgeral):
        liquidez_geral = LiquidezGeral.query.filter_by(
            liquidezgeral=liquidezgeral).first()
        dados = request.json

        if 'ativo_circulante' in dados:
            liquidez_geral.ativo_circulante = dados['ativo_circulante']

        if 'realizavel_longo_prazo' in dados:
            liquidez_geral.realizavel_longo_prazo = dados['realizavel_longo_prazo']

        if 'liquidez_geral' in dados:
            liquidez_geral.liquidez_geral = dados['liquidez_geral']

        if 'passivo_circulante' in dados:
            liquidez_geral.passivo_circulante = dados['passivo_circulante']

        if 'exigivel_longo_prazo' in dados:
            liquidez_geral.exigivel_longo_prazo = dados['exigivel_longo_prazo']

        if 'resultado' in dados:
            liquidez_geral.resultado = dados['resultado']

        liquidez_geral.save()
        response = {
            'id': liquidez_geral.id,
            'ativo_circulante': liquidez_geral.ativo_circulante,
            'realizavel_longo_prazo': liquidez_geral.realizavel_longo_prazo,
            'liquidez_geral': liquidez_geral.liquidez_geral,
            'passivo_circulante': liquidez_geral.passivo_circulante,
            'exigivel_longo_prazo': liquidez_geral.exigivel_longo_prazo,
            'resultado': liquidez_geral.resultado
        }

        return response

    def delete(self, liquidezgeral):
        liquidez_geral = LiquidezSeca.query.filter_by(id=liquidezgeral).first()
        mensagem = 'Liquidez geral {} excluida com sucesso'.format(liquidez_geral)
        liquidez_geral.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaLiquidezGeral(Resource):

    def get(self):
        liquidez_geral = LiquidezGeral.query.all()
        response = [{
            'id': i.id,
            'ativo_circulante': i.ativo_circulante,
            'realizavel_longo_prazo': i.realizavel_longo_prazo,
            'liquidez_geral': i.liquidez_geral,
            'passivo_circulante': i.passivo_circulante,
            'exigivel_longo_prazo': i.exigivel_longo_prazo,
            'resultado': i.resultado

        } for i in liquidez_geral]
        return response

    def post(self):
        dados = request.json
        if dados['passivo_circulante'] > 0 < dados['ativo_circulante']:
            liquidez_geral = LiquidezGeral(
                id=dados['id'],
                ativo_circulante=dados['ativo_circulante'],
                realizavel_longo_prazo=dados['realizavel_longo_prazo'],
                liquidez_geral=(dados['ativo_circulante'] + dados['realizavel_longo_prazo']) / (
                        dados['passivo_circulante'] + dados['exigivel_longo_prazo']),
                passivo_circulante=dados['passivo_circulante'],
                exigivel_longo_prazo=dados['exigivel_longo_prazo'],
                resultado="Bom grau de liquidez geral" if (dados['ativo_circulante'] + dados[
                    'realizavel_longo_prazo']) / (dados['passivo_circulante'] + dados[
                    'exigivel_longo_prazo']) >= 1 else "Não tem como quitar dividas"
            )

        liquidez_geral.save()
        response = {
            'id': liquidez_geral.id,
            'ativo_circulante': liquidez_geral.ativo_circulante,
            'realizavel_longo_prazo': liquidez_geral.realizavel_longo_prazo,
            'liquidez_geral': liquidez_geral.liquidez_geral,
            'passivo_circulante': liquidez_geral.passivo_circulante,
            'exigivel_longo_prazo': liquidez_geral.exigivel_longo_prazo,
            'resultado': liquidez_geral.resultado
        }
        return response


class CalculoMargemLiquida(Resource):
    def get(self, margemliquida):
        margem_liquida = LiquidezGeral.query.filter_by(
            id=margemliquida).first()
        try:
            response = {
                'lucro_liquido': margem_liquida.lucro_liquido,
                'receita_liquida': margem_liquida.receita_liquida,
                'margem_liquida': margem_liquida.margem_liquida,
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Margem liquida não encontrada'
            }
        return response

    def put(self, margemliquida):
        margem_liquida = MargemLiquida.query.filter_by(
            margemliquida=margemliquida).first()
        dados = request.json

        if 'lucro_liquido' in dados:
            margem_liquida.lucro_liquido = dados['lucro_liquido']

        if 'receita_liquida' in dados:
            margem_liquida.receita_liquida = dados['receita_liquida']

        if 'margem_liquida' in dados:
            margem_liquida.margem_liquida = dados['margem_liquida']

        margem_liquida.save()
        response = {
            'id': margem_liquida.id,
            'lucro_liquido': margem_liquida.lucro_liquido,
            'receita_liquida': margem_liquida.receita_liquida,
            'margem_liquida': margem_liquida.margem_liquida
        }

        return response

    def delete(self, margemliquida):
        margem_liquida = MargemLiquida.query.filter_by(id=margemliquida).first()
        mensagem = 'Margem liquida {} excluida com sucesso'.format(margem_liquida)
        margem_liquida.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}


class ListaMargemLiquida(Resource):

    def get(self):
        margem_liquida = MargemLiquida.query.all()
        response = [{
            'id': i.id,
            'lucro_liquido': i.lucro_liquido,
            'receita_liquida': i.receita_liquida,
            'margem_liquida': i.margem_liquida

        } for i in margem_liquida]
        return response

    def post(self):
        dados = request.json
        if dados['lucro_liquido'] > 0 < dados['receita_liquida']:
            margem_liquida = MargemLiquida(
                id=dados['id'],
                lucro_liquido=dados['lucro_liquido'],
                receita_liquida=dados['receita_liquida'],
                margem_liquida=(dados['lucro_liquido'] / dados['receita_liquida']) * 100,
            )

        margem_liquida.save()
        response = {
            'id': margem_liquida.id,
            'lucro_liquido': margem_liquida.lucro_liquido,
            'receita_liquida': margem_liquida.receita_liquida,
            'margem_liquida': margem_liquida.margem_liquida
        }
        return response

class CalculoGiroAtivo(Resource):
    def get(self, giroativo):
        giro_ativo = GiroAtivo.query.filter_by(
            id=giroativo).first()
        try:
            response = {
                'giro_ativo': giro_ativo.giro_ativo,
                'receita_liquida': giro_ativo.receita_liquida,
                'ativo': giro_ativo.ativo,
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Giro ativo não encontrada'
            }
        return response

    def put(self, giroativo):
        giro_ativo = GiroAtivo.query.filter_by(
            giroativo=giroativo).first()
        dados = request.json

        if 'giro_ativo' in dados:
            giro_ativo.giro_ativo = dados['giro_ativo']

        if 'receita_liquida' in dados:
            giro_ativo.receita_liquida = dados['receita_liquida']

        if 'ativo' in dados:
            giro_ativo.ativo = dados['ativo']

        giro_ativo.save()
        response = {
            'id': giro_ativo.id,
            'giro_ativo': giro_ativo.giro_ativo,
            'receita_liquida': giro_ativo.receita_liquida,
            'ativo': giro_ativo.ativo
        }

        return response

    def delete(self, giroativo):
        giro_ativo = GiroAtivo.query.filter_by(id=giroativo).first()
        mensagem = 'Giro do ativo {} excluido com sucesso'.format(giro_ativo)
        giro_ativo.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}

class ListaGiroAtivo(Resource):

    def get(self):
        giro_ativo = GiroAtivo.query.all()
        response = [{
            'id': i.id,
            'giro_ativo': i.giro_ativo,
            'receita_liquida': i.receita_liquida,
            'ativo': i.ativo

        } for i in giro_ativo]
        return response

    def post(self):
        dados = request.json
        if dados['ativo'] > 0 < dados['receita_liquida']:
            giro_ativo = GiroAtivo(
                id=dados['id'],
                ativo=dados['ativo'],
                receita_liquida=dados['receita_liquida'],
                giro_ativo=(dados['receita_liquida'] / dados['ativo']) * 100
            )

        giro_ativo.save()
        response = {
            'id': giro_ativo.id,
            'ativo': giro_ativo.ativo,
            'receita_liquida': giro_ativo.receita_liquida,
            'giro_ativo': giro_ativo.giro_ativo
        }
        return response

class CalculoRentabilidadeAtivo(Resource):
    def get(self, rentabilidadeativo):
        rentabilidade_ativo = RentabilidadeAtivo.query.filter_by(
            id=giroativo).first()
        try:
            response = {
                'lucro_liquido': rentabilidade_ativo.lucro_liquido,
                'rentabilidade_ativo': rentabilidade_ativo.rentabilidade_ativo,
                'ativo': rentabilidade_ativo.ativo,
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Rentabilidade do ativo não encontrada'
            }
        return response

    def put(self, rentabilidadeativo):
        rentabilidade_ativo = RentabilidadeAtivo.query.filter_by(
            rentabilidadeativo=rentabilidadeativo).first()
        dados = request.json

        if 'lucro_liquido' in dados:
            rentabilidade_ativo.lucro_liquido = dados['lucro_liquido']

        if 'rentabilidade_ativo' in dados:
            rentabilidade_ativo.rentabilidade_ativo = dados['rentabilidade_ativo']

        if 'ativo' in dados:
            rentabilidade_ativo.ativo = dados['ativo']

        rentabilidade_ativo.save()
        response = {
            'id': rentabilidade_ativo.id,
            'lucro_liquido': rentabilidade_ativo.lucro_liquido,
            'rentabilidade_ativo': rentabilidade_ativo.rentabilidade_ativo,
            'ativo': rentabilidade_ativo.ativo
        }

        return response

    def delete(self, rentabilidadeativo):
        rentabilidade_ativo = RentabilidadeAtivo.query.filter_by(id=rentabilidadeativo).first()
        mensagem = 'Rentabilidade do ativo {} excluido com sucesso'.format(rentabilidade_ativo)
        rentabilidade_ativo.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}

class ListaRentabilidadeAtivo(Resource):

    def get(self):
        rentabilidade_ativo = RentabilidadeAtivo.query.all()
        response = [{
            'id': i.id,
            'lucro_liquido': i.lucro_liquido,
            'rentabilidade_ativo': i.rentabilidade_ativo,
            'ativo': i.ativo

        } for i in rentabilidade_ativo]
        return response

    def post(self):
        dados = request.json
        if dados['ativo'] > 0 < dados['lucro_liquido']:
            rentabilidade_ativo = RentabilidadeAtivo(
                id=dados['id'],
                ativo=dados['ativo'],
                lucro_liquido=dados['lucro_liquido'],
                rentabilidade_ativo=(dados['lucro_liquido'] / dados['ativo']) * 100
            )

        rentabilidade_ativo.save()
        response = {
            'id': rentabilidade_ativo.id,
            'ativo': rentabilidade_ativo.ativo,
            'lucro_liquido': rentabilidade_ativo.lucro_liquido,
            'rentabilidade_ativo': rentabilidade_ativo.rentabilidade_ativo
        }
        return response


class CalculoRentabilidadePl(Resource):
    def get(self, rentabilidadepl):
        rentabilidade_pl = RentabilidadePl.query.filter_by(
            id=giroativo).first()
        try:
            response = {
                'lucro_liquido': rentabilidade_pl.lucro_liquido,
                'patrimonio_liquido': rentabilidade_pl.patrimonio_liquido,
                'rentabilidade_pl': rentabilidade_pl.rentabilidade_pl,
            }
        except AttributeError:
            response = {
                'status': 'error',
                'message': 'Rentabilidade do patrimonio liquido não encontrada'
            }
        return response

    def put(self, rentabilidadepl):
        rentabilidade_pl = RentabilidadePl.query.filter_by(
            rentabilidadepl=rentabilidadepl).first()
        dados = request.json

        if 'lucro_liquido' in dados:
            rentabilidade_pl.lucro_liquido = dados['lucro_liquido']

        if 'patrimonio_liquido' in dados:
            rentabilidade_pl.patrimonio_liquido = dados['patrimonio_liquido']

        if 'rentabilidade_pl' in dados:
            rentabilidade_pl.rentabilidade_pl = dados['rentabilidade_pl']

        rentabilidade_pl.save()
        response = {
            'id': rentabilidade_pl.id,
            'lucro_liquido': rentabilidade_pl.lucro_liquido,
            'patrimonio_liquido': rentabilidade_pl.patrimonio_liquido,
            'rentabilidade_pl': rentabilidade_pl.rentabilidade_pl
        }

        return response

    def delete(self, rentabilidadepl):
        rentabilidade_pl = RentabilidadePl.query.filter_by(id=rentabilidadepl).first()
        mensagem = 'Rentabilidade do patrimonio liquido {} excluida com sucesso'.format(rentabilidade_pl)
        rentabilidade_pl.delete()
        return {'status': 'sucesso', 'mensagem': mensagem}

class ListaRentabilidadePl(Resource):

    def get(self):
        rentabilidade_pl = RentabilidadePl.query.all()
        response = [{
            'id': i.id,
            'lucro_liquido': i.lucro_liquido,
            'patrimonio_liquido': i.patrimonio_liquido,
            'rentabilidade_pl': i.rentabilidade_pl

        } for i in rentabilidade_pl]
        return response

    def post(self):
        dados = request.json
        if dados['lucro_liquido'] > 0 < dados['patrimonio_liquido']:
            rentabilidade_pl = RentabilidadePl(
                id=dados['id'],
                lucro_liquido=dados['lucro_liquido'],
                patrimonio_liquido=dados['patrimonio_liquido'],
                rentabilidade_pl=(dados['lucro_liquido'] / dados['patrimonio_liquido']) * 100
            )

        rentabilidade_pl.save()
        response = {
            'id': rentabilidade_pl.id,
            'lucro_liquido': rentabilidade_pl.lucro_liquido,
            'patrimonio_liquido': rentabilidade_pl.patrimonio_liquido,
            'rentabilidade_pl': rentabilidade_pl.rentabilidade_pl
        }
        return response



api.add_resource(JuroComposto, '/jurocomposto/<int:juroscompostos>/')
api.add_resource(ListaJurosCompostos, '/listajuroscompostos/')
api.add_resource(Operacao, '/jurosimples/<int:id>/')
api.add_resource(ListaOperacoes, '/listajurossimples/')
api.add_resource(TaxaNominal, '/taxanominal/<int:id>/')
api.add_resource(ListaTaxaNominal, '/listataxanominal/')
api.add_resource(TaxaEfetiva, '/taxaefetiva/<int:id>/')
api.add_resource(ListaTaxaEfetiva, '/listataxaefetiva/')
api.add_resource(TaxaJurosReal, '/taxareal/<int:id>/')
api.add_resource(ListaTaxaReal, '/listataxareal/')
api.add_resource(FormacaoCapital, '/formacaocapitalac/<int:id>/')
api.add_resource(ListaFormacaoCapital, '/listaformacaocapitalac/')
api.add_resource(CalculoDescSimples, '/descontosimples/<int:id>/')
api.add_resource(ListaDescontoSimples, '/listadescontosimples/')
api.add_resource(CalculoDescComposto, '/descontocomposto/<int:descontocomposto>/')
api.add_resource(ListaDescontoComposto, '/listadescontocomposto/')
api.add_resource(CalculoPrestacaoConstante, '/prestacaoconstante/<int:prestacaoconstante>/')
api.add_resource(ListaPrestacaoConstante, '/listaprestacaoconstante/')
api.add_resource(CalculoAmortizacaoConstante, '/amortizacaoconstante/<int:amortizacaoconstante>/')
api.add_resource(ListaAmortizacaoConstante, '/listaamortizacaoconstante/')
api.add_resource(CalculoAnaliseHorizontal, '/analisehorizontal/<int:analisehorizontal>/')
api.add_resource(ListaAnaliseHorizontal, '/listaanalisehorizontal/')
api.add_resource(CalculoAnaliseVertical, '/analisevertical/<int:analisevertical>/')
api.add_resource(ListaAnaliseVertical, '/listaanalisevertical/')
api.add_resource(CalculoLiquidezImediata, '/liquidezimediata/<int:liquidezimediata>/')
api.add_resource(ListaLiquidezImediata, '/listaliquidezimediata/')
api.add_resource(CalculoLiquidezCorrente, '/liquidezcorrente/<int:liquidezcorrente>/')
api.add_resource(ListaLiquidezCorrente, '/listaliquidezcorrente/')
api.add_resource(CalculoLiquidezSeca, '/liquidezseca/<int:liquidezseca>/')
api.add_resource(ListaLiquidezSeca, '/listaliquidezseca/')
api.add_resource(CalculoLiquidezGeral, '/liquidezgeral/<int:liquidezgeral>/')
api.add_resource(ListaLiquidezGeral, '/listaliquidezgeral/')
api.add_resource(CalculoMargemLiquida, '/margemliquida/<int:margemliquida>/')
api.add_resource(ListaMargemLiquida, '/listamargemliquida/')
api.add_resource(CalculoGiroAtivo, '/giroativo/<int:giroativo>/')
api.add_resource(ListaGiroAtivo, '/listagiroativo/')
api.add_resource(CalculoRentabilidadeAtivo, '/rentabilidadeativo/<int:rentabilidadeativo>/')
api.add_resource(ListaRentabilidadeAtivo, '/listarentabilidadeativo/')
api.add_resource(CalculoRentabilidadePl, '/rentabilidadepl/<int:rentabilidadepl>/')
api.add_resource(ListaRentabilidadePl, '/listarentabilidadepl/')

if __name__ == '__main__':
    app.run(debug=True)
