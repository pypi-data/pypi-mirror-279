# Sazonal

[![Logo](https://github.com/framework-CPTEC/_static/blob/main/framework.png)](https://www.cptec.inpe.br/)


## Framework-Sazonal

É um pacote in Python para a distribuição de dados brutos de previsão subsazonal do CPTEC/INPE  produzidos com o modelo BAM-1.2. Os arquivos de dados contêm a média do conjunto (de 11 membros) para todos os produtos e variáveis mostradas no site https://subsazonal.cptec.inpe.br/.

Esses arquivos estão disponíveis como anomalias computadas referentes à climatologia 1999-2018.

support Python >= 3.10.

## Import

import CPTEC_SUB as SUB


## Inicialização

Ex. de Pedido
Durante a inicialização do construtor informações sobre os dados são exibidas

sub = SUB.model()


## Pedido

### Data  
date= '20240214'

### Variaveis 
var = 'prec'

Lista de variáveis disponíveis:
- prec -> precipitação
- t2mt -> temperatura de 2 metros
- psnm -> pressão ao nível do mar
- função -> radiação de onda longa de saída
- tp85 -> temperatura a 850 hPa
- gz50 -> altura geopotencial em 500 hPa
- uv85 -> vento zonal a 850 hPa
- uv20 -> vento zonal a 200 hPa
- vv85 -> vento meridional a 850 hPa
- vv20 -> vento meridional a 200 hPa

Arquivos de dados de previsão calibrados são gerados para valores totais de temperatura e precipitação de 2 metros, probabilidade do tercil mais provável, probabilidade de anomalia positiva e anomalias.

- prec_ca -> precipitação calibrada
- t2mt_ca -> temperatura de 2 metros calibrada


### Produto
product = 'week'

Lista de produtos disponíveis:
- week -> média ou acúmulo semanal (7 dias), para as semanas 01, 02, 03 e 04
- fort -> média ou acúmulo quinzenal (14 dias), para as quinzenas 01 e 02
- 3wks -> média de 21 dias ou acumulação
- mnth -> média ou acúmulo de 30 dias


### Campo
field='anomalies'

Lista de campos calibrados determinísticos e probabilísticos disponíveis:
- anomalies -> anomalias de previsão
- prob_positive_anomaly  -> probabilidade de previsão de anomalia positiva
- prob_terciles -> probabilidade de previsão do tercil mais provável
- totals -> valor total previsto


### Steps = Número da figura disponível por produto.

step = '01'
- week -> dado por semana (01, 02, 03 e 04)
- fort -> dado por quinzena (14 dias), para as quinzenas (01 e 02)
- 3wks -> dado médio de 21 dias ou acumulação (01)
- mnth -> dado médio ou acúmulo de 30 dias (01)


### Exemplo de solicitação do Pedido
f = sub.load(date='20240207', var='prec', step='01', product='week',field='anomalies')


support Python >= 3.10.


[(Documentacao completa do Projeto)](https://cptec-model.readthedocs.io/en/latest/index.html)