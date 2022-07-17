# api_engenharia_economica
 Api desenvolvida em Python com Flask para processar os seguintes topicos de engenharia economica:
 
 * Juros Simples
 * Juros Compostos
 * Taxa Nominal
 * Taxa Efetiva
 * Taxa Juros Real
 * Formação de Capital
 * Desconto Simples
 * Desconto Composto
 * Sitema de Prestação Constante
 * Sistema de Amortização Constante
 * Analise Horizontal
 * Analise Vertical
 * Liquidez Imediata
 * Liquidez Corrente
 * Liquidez Seca
 * Liquidez Geral
 * Margem Liquida
 * Giro do Ativo
 * Rentabilidade do Ativo
 * Rentabilidade do Patrimonio Liquido
 * Prazo medio de estocagem
 * Prazo medio de pagamento
 * Prazo medio de recebimento
 * Ciclos (operacional e financeiro)


Lista de endpoints:

* JuroComposto : ip_server + /jurocomposto/<int:juroscompostos>/
* ListaJurosCompostos : ip_server + /listajuroscompostos/
* Operacao : ip_server + /jurosimples/<int:id>/
* ListaOperacoes : ip_server + /listajurossimples/
* TaxaNominal : ip_server + /taxanominal/<int:id>/
* ListaTaxaNominal : ip_server + /listataxanominal/
* TaxaEfetiva : ip_server + /taxaefetiva/<int:id>/
* ListaTaxaEfetiva ip_server + /listataxaefetiva/
* TaxaJurosReal : ip_server + /taxareal/<int:id>/
* ListaTaxaReal : ip_server + /listataxareal/
* FormacaoCapital : ip_server + /formacaocapitalac/<int:id>/
* ListaFormacaoCapital : ip_server + /listaformacaocapitalac/
* CalculoDescSimples : ip_server + /descontosimples/<int:id>/
* ListaDescontoSimples : ip_server + /listadescontosimples/
* CalculoDescComposto : ip_server + /descontocomposto/<int:descontocomposto>/
* ListaDescontoComposto : ip_server + /listadescontocomposto/
* CalculoPrestacaoConstante : ip_server + /prestacaoconstante/<int:prestacaoconstante>/
* ListaPrestacaoConstante : ip_server + /listaprestacaoconstante/
* CalculoAmortizacaoConstante : ip_server + /amortizacaoconstante/<int:amortizacaoconstante>/
* ListaAmortizacaoConstante : ip_server + /listaamortizacaoconstante/
* CalculoAnaliseHorizontal : ip_server + /analisehorizontal/<int:analisehorizontal>/
* ListaAnaliseHorizontal : ip_server + /listaanalisehorizontal/
* CalculoAnaliseVertical, '/analisevertical/<int:analisevertical>/
* ListaAnaliseVertical : ip_server + /listaanalisevertical/
* CalculoLiquidezImediata : ip_server + /liquidezimediata/<int:liquidezimediata>/
* ListaLiquidezImediata : ip_server + /listaliquidezimediata/
* CalculoLiquidezCorrente : ip_server + /liquidezcorrente/<int:liquidezcorrente>/
* ListaLiquidezCorrente : ip_server + /listaliquidezcorrente/
* CalculoLiquidezSeca : ip_server + /liquidezseca/<int:liquidezseca>/
* ListaLiquidezSeca : ip_server + /listaliquidezseca/
* CalculoLiquidezGeral : ip_server + /liquidezgeral/<int:liquidezgeral>/
* ListaLiquidezGeral : ip_server + /listaliquidezgeral/
* CalculoMargemLiquida : ip_server + /margemliquida/<int:margemliquida>/
* ListaMargemLiquida : ip_server + /listamargemliquida/
* CalculoGiroAtivo : ip_server + /giroativo/<int:giroativo>/
* ListaGiroAtivo : ip_server + /listagiroativo/
* CalculoRentabilidadeAtivo : ip_server + /rentabilidadeativo/<int:rentabilidadeativo>/
* ListaRentabilidadeAtivo : ip_server + /listarentabilidadeativo/
* CalculoRentabilidadePl : ip_server + /rentabilidadepl/<int:rentabilidadepl>/
* ListaRentabilidadePl : ip_server + /listarentabilidadepl/
* CalculoPrazoMedioEstocagem : ip_server + /prazomedioestocagem/<int:prazomedioestocagem>/
* ListaPrazoMedioEstocagem : ip_server + /listaprazomedioestocagem/
* CalculoPrazoMedioPagamento : ip_server + /prazomediopagamento/<int:prazomediopagamento>/
* ListaPrazoMedioPagamento : ip_server + /listaprazomediopagamento/
* CalculoPrazoMedioRecebimento : ip_server + /prazomediorecebimento/<int:prazomediorecebimento>/
* ListaPrazoMedioRecebimento : ip_server + /listaprazomediorecebimento/
* CalculoCiclos : ip_server + /ciclos/<int:ciclos>/
* ListaCiclos : ip_server + /listaciclos/


Observações:
* Para utilizar a api, basta executar o arquivo app.py
* Com o ip gerado pelo server, basta utilizar algum software que permita a manipulação dos endpoints atraves de json (ex: Insomnia)
* ip_server = numero de ip gerado pelo server após rodar o arquivo app.py