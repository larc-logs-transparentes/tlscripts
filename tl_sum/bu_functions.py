from dataclasses import dataclass
from bu_class import BU, resultado_candidato_type

@dataclass
class soma:
    soma_por_cargo: dict[str, dict[int, resultado_candidato_type]]
    
def soma_votos(bu_file, cargo=None):
    soma_obj = soma(
        soma_por_cargo={}
    )
    
    for bu in bu_file:
        resultados = BU(bu).get_resultados_por_eleicao()
        for eleicao_type in resultados.eleicoes:
            for resultado_cargo in eleicao_type.resultados.keys():            
                if cargo is not None and cargo != resultado_cargo:
                    continue
                if resultado_cargo not in soma_obj.soma_por_cargo:
                    soma_obj.soma_por_cargo[resultado_cargo] = {}
                
                for codigo_candidato in eleicao_type.resultados[resultado_cargo]:
                    resultado_candidato = eleicao_type.resultados[resultado_cargo][codigo_candidato]
                    
                    if str(codigo_candidato) not in soma_obj.soma_por_cargo[resultado_cargo]:
                        soma_obj.soma_por_cargo[resultado_cargo][str(codigo_candidato)] = resultado_candidato
                    else:
                        soma_obj.soma_por_cargo[resultado_cargo][str(codigo_candidato)].quantidade_votos += resultado_candidato.quantidade_votos

    return soma_obj 