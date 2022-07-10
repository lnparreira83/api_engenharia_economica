import math

from flask import Flask, request
from flask_restful import Resource, Api
from models import OperacaoJuroComposto
from models import Operacoes
from models import OperacaoTaxaNominal
from models import OperacaoTaxaEfetiva
from models import OperacaoTaxaJurosReal
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

if __name__ == '__main__':
    app.run(debug=True)
