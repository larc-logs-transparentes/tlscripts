from dataclasses import dataclass
from bu_class import BU, resultado_candidato_type

@dataclass
class soma:
    soma_por_cargo: dict[str, dict[int, resultado_candidato_type]]
    
def soma_votos(bu_file, cargo_filtro=None, municipio_filtro=None):
    soma_obj = soma({}) # Dicionário que armazenará a soma dos votos por cargo
    qtd_bus_somados = 0

    for bu in bu_file:
        resultados = BU(bu).get_resultados_por_eleicao()
        if verificar_municipio_bu(bu, municipio_filtro) == False:
            continue #Município diferente do município passado como filtro, passa para o próximo BU

        qtd_bus_somados += 1
        for eleicao in resultados.eleicoes:
            # Para cada cargo contido nessa eleição desse BU
            for resultado_cargo in eleicao.resultados.keys():           
                if verificar_cargo_filtro(resultado_cargo, cargo_filtro) == False:
                    continue #Cargo diferente do cargo passado como filtro, passa para o próximo cargo
                
                # Se o cargo ainda não foi adicionado, o adiciona no dicionário da soma, sendo a chave o nome do cargo
                if resultado_cargo not in soma_obj.soma_por_cargo:
                    soma_obj.soma_por_cargo[resultado_cargo] = {}
                
                # Para cada candidato desse cargo
                for codigo_candidato in eleicao.resultados[resultado_cargo]:
                    resultado_candidato = eleicao.resultados[resultado_cargo][codigo_candidato]
                    if str(codigo_candidato) not in soma_obj.soma_por_cargo[resultado_cargo]: 
                        #Se o candidato ainda não foi adicionado no campo do cargo correspondente, o adiciona, sendo a chave o código do candidato
                        soma_obj.soma_por_cargo[resultado_cargo][str(codigo_candidato)] = resultado_candidato        
                    else: 
                        #Se o candidato já foi adicionado, soma os votos do BU atual com os votos anteriores contidos na chave de seu código, no campo do cargo correspondente
                        soma_obj.soma_por_cargo[resultado_cargo][str(codigo_candidato)].quantidade_votos += resultado_candidato.quantidade_votos
        print(f"Quantidade de arquivos BU processados: {qtd_bus_somados}", end='\r')
        
    print(f"Quantidade de arquivos BU processados: {qtd_bus_somados}")
    return soma_obj

""" 
    Retorna True se o BU for do município passado como parâmetro, False caso contrário.
    Caso o parâmetro município seja None, retorna True.
"""
def verificar_municipio_bu(bu, municipio):
    if municipio is None:
        return True
    
    dados_secao = BU(bu).get_dados_secao()
    return dados_secao.municipio == municipio

""" 
    Retorna True se o resultado do cargo for correspondente ao cargo passado como parâmetro, False caso contrário.
    Caso o parâmetro cargo seja None, retorna True.
"""
def verificar_cargo_filtro(resultado_cargo, cargo_filtro):
    if cargo_filtro is None:
        return True
    
    return resultado_cargo == cargo_filtro