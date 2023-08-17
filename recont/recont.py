import ijson
import json
from dataclasses import dataclass

""" Definição de tipos """

@dataclass
class dados_secao_type:
    secao: str
    municipio: str
    zona: str
    
@dataclass
class resultado_candidato_type:
    identificacao_votavel: str
    quantidade_votos: int
    tipo_voto: str

@dataclass
class eleicao_type:
    id_eleicao: str
    resultados: dict[str, resultado_candidato_type]
        
@dataclass
class boletim_urna_type:
    dados_secao: dados_secao_type
    eleicoes: list[eleicao_type]

""" --------------------- """    

def get_json_data(filename):
    with open(filename, 'r') as f:
        objects = ijson.items(f, 'item')
        rows = list(objects)
    return rows

    
def get_dados_secao(bu):
    identificacao_secao = bu['identificacaoSecao']
    municipio_zona = identificacao_secao['municipioZona']
    
    return dados_secao_type(
        secao=identificacao_secao['secao'],
        municipio=municipio_zona['municipio'],
        zona=municipio_zona['zona']
    )

def resultados_votacao_agrupado_por_eleicao_e_cargo(bu):
    
    boletim_urna_obj = boletim_urna_type(
        dados_secao=get_dados_secao(bu),
        eleicoes=[]
    )
    
    resultados_votacao_por_eleicao = bu['resultadosVotacaoPorEleicao']
    for eleicao in resultados_votacao_por_eleicao:
        eleicao_obj = eleicao_type(
            id_eleicao=eleicao['idEleicao'],
            resultados={}
        )
    
        for resultado_eleicao in eleicao['resultadosVotacao']:
            for resultado_cargo in resultado_eleicao['totaisVotosCargo']:
                cargo = resultado_cargo['codigoCargo'][1]
                
                for resultado_candidato in resultado_cargo['votosVotaveis']:
                    try:
                        votos = resultado_candidato_type(
                            identificacao_votavel=resultado_candidato['identificacaoVotavel'],
                            quantidade_votos=resultado_candidato['quantidadeVotos'],
                            tipo_voto=resultado_candidato['tipoVoto']
                        )
                    except KeyError:
                        votos = resultado_candidato_type(
                            identificacao_votavel=None,
                            quantidade_votos=resultado_candidato['quantidadeVotos'],
                            tipo_voto=resultado_candidato['tipoVoto']
                        )
                    print(cargo, votos)
                
                    if cargo in eleicao_obj.resultados:
                        eleicao_obj.resultados[cargo].append(votos)
                    else:
                        eleicao_obj.resultados[cargo] = [votos]
                        
            boletim_urna_obj.eleicoes.append(eleicao_obj)

    return boletim_urna_obj 

bu_json = get_json_data('recont/bu_1t.json')[6]
print(get_dados_secao(bu_json))

resultados = resultados_votacao_agrupado_por_eleicao_e_cargo(bu_json)

for eleicao_type in resultados.eleicoes:
    print(eleicao_type.id_eleicao)
    for cargo in eleicao_type.resultados.keys():
        print(cargo)
        for votos in eleicao_type.resultados[cargo]:
            print(f'\t{votos}')
    print('-----------------------')