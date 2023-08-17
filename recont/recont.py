import ijson
import json
from dataclasses import dataclass

""" Definição de tipos """

@dataclass
class dados_secao:
    secao: str
    municipio: str
    zona: str
    
@dataclass
class resultado_cargo:
    cargo: str
    votos: str
    
@dataclass
class resultados_votacao_agrupado_por_eleicao_e_cargo:
    idEleicao: str
    resultados: dict
    
""" --------------------- """    

def get_json_data(filename):
    with open(filename, 'r') as f:
        objects = ijson.items(f, 'item')
        rows = list(objects)
    return rows

def pretty_print_dict(dict):
    print(json.dumps(dict, indent=4, sort_keys=True))
    
def get_dados_secao(bu):
    identificacao_secao = bu['identificacaoSecao']
    municipio_zona = identificacao_secao['municipioZona']
    
    return dados_secao(
        secao=identificacao_secao['secao'],
        municipio=municipio_zona['municipio'],
        zona=municipio_zona['zona']
    )

def resultados_votacao_agrupado_por_eleicao_e_cargo(bu):
    resultados_por_cargo = []
    resultados_votacao_por_eleicao = bu['resultadosVotacaoPorEleicao']
    
    for eleicao in resultados_votacao_por_eleicao:
        dict_eleicao = {
            'idEleicao': eleicao['idEleicao'],
            'resultados': {}
        }

        for resultado_eleicao in eleicao['resultadosVotacao']:
            for resultado_cargo in resultado_eleicao['totaisVotosCargo']:
                cargo = resultado_cargo['codigoCargo'][1]
                votos = resultado_cargo['votosVotaveis']
                
                dict_eleicao['resultados'][cargo] = votos
        resultados_por_cargo.append(dict_eleicao)

    return resultados_por_cargo 

bu_json = get_json_data('recont/bu_1t.json')[6]
print(get_dados_secao(bu_json))
pretty_print_dict(resultados_votacao_agrupado_por_eleicao_e_cargo(bu_json))
