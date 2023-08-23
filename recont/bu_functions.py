from dataclasses import dataclass
from bu_class import BU, resultado_candidato_type

@dataclass
class soma:
    soma_por_cargo: dict[str, dict[int, resultado_candidato_type]]
    
def soma_votos(bus_list):
    soma_obj = soma(
        soma_por_cargo={}
    )
    
    for bu in bus_list:
        resultados = BU(bu).get_resultados_por_eleicao()
        for eleicao_type in resultados.eleicoes:
            for cargo in eleicao_type.resultados.keys():
                if cargo not in soma_obj.soma_por_cargo:
                    soma_obj.soma_por_cargo[cargo] = {}
                for codigo_candidato in eleicao_type.resultados[cargo]:
                    resultado_candidato = eleicao_type.resultados[cargo][codigo_candidato]
                    
                    if codigo_candidato not in soma_obj.soma_por_cargo[cargo]:
                        soma_obj.soma_por_cargo[cargo][codigo_candidato] = resultado_candidato
                    else:
                        soma_obj.soma_por_cargo[cargo][codigo_candidato].quantidade_votos += resultado_candidato.quantidade_votos

    return soma_obj 