from bu_class import BU
from json_utils import get_json_data
from bu_functions import soma_votos

bus_json = get_json_data('recont/bu_1t.json')
bu = BU(bus_json[0])
print(bu.get_dados_secao())

resultados = bu.get_resultados_por_eleicao()

for eleicao_type in resultados.eleicoes:
    print(eleicao_type.id_eleicao)
    for cargo in eleicao_type.resultados.keys():
        print(cargo)
        for codigo_candidato in eleicao_type.resultados[cargo].keys():
            print(f'{codigo_candidato}: {eleicao_type.resultados[cargo][codigo_candidato]}')
    print('-----------------------')
     
resultado_presidente = soma_votos(bus_json).soma_por_cargo['presidente']
for codigo_presidente in resultado_presidente.keys():
    print(f'{codigo_presidente}: {resultado_presidente[codigo_presidente]}')