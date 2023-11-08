from dataclasses import dataclass
from .model.bu_model import BU, resultado_candidato_type
from .converter.map_county_code_to_state import get_state_from_code

@dataclass
class Soma:
    soma_por_cargo: dict[str, dict[str, resultado_candidato_type]]


def soma_votos(bu_file, cargo_filtro=None, estado_filtro=None, municipio_filtro=None, timeline_freq=None):
    soma_obj = Soma({})  # Dicionário que armazenará a soma dos votos por cargo
    qtd_bus_somados = 0

    for bu in bu_file:
        resultados = BU(bu).get_resultados_por_eleicao()
        if not verificar_municipio_bu(bu, municipio_filtro) or not verificar_estado_bu(bu, estado_filtro):
            continue  # Município diferente do município passado como filtro, passa para o próximo BU

        qtd_bus_somados += 1
        for eleicao in resultados.eleicoes:
            # Para cada cargo contido nessa eleição desse BU
            for resultado_cargo in eleicao.resultados.keys():
                if not verificar_cargo_filtro(resultado_cargo, cargo_filtro):
                    continue  # Cargo diferente do cargo passado como filtro, passa para o próximo cargo

                # Se o cargo ainda não foi adicionado, o adiciona no dicionário da soma, sendo a chave o nome do cargo
                if resultado_cargo not in soma_obj.soma_por_cargo:
                    soma_obj.soma_por_cargo[resultado_cargo] = {}

                # Para cada candidato desse cargo
                for codigo_candidato in eleicao.resultados[resultado_cargo]:
                    resultado_candidato = eleicao.resultados[resultado_cargo][codigo_candidato]
                    if str(codigo_candidato) not in soma_obj.soma_por_cargo[resultado_cargo]:
                        # Se o candidato ainda não foi adicionado no campo do cargo correspondente, o adiciona,
                        # sendo a chave o código do candidato
                        soma_obj.soma_por_cargo[resultado_cargo][str(codigo_candidato)] = resultado_candidato
                    else:
                        # Se o candidato já foi adicionado, soma os votos do BU atual com os votos anteriores
                        # contidos na chave de seu código, no campo do cargo correspondente
                        soma_obj.soma_por_cargo[resultado_cargo][
                            str(codigo_candidato)].quantidade_votos += resultado_candidato.quantidade_votos
        print(f"Quantidade de arquivos BU somados: {qtd_bus_somados}", end='\r')
        if timeline_freq is not None and qtd_bus_somados % timeline_freq == 0:
            _concatena_no_arquivo_timeline(soma_obj, qtd_bus_somados, timeline_freq)

    print(f"Quantidade de arquivos BU somados: {qtd_bus_somados}")
    return soma_obj


def verificar_estado_bu(bu, estado):
    """
        Retorna True se o BU for do estado passado como parâmetro, false caso contrário.
        Caso o parâmetro estado seja None, retorna True.
    """
    if estado is None:
        return True

    return get_state_from_code(BU(bu).get_dados_secao().municipio) == estado


def verificar_municipio_bu(bu, municipio):
    """
        Retorna True se o BU for do município passado como parâmetro, false caso contrário.
        Caso o parâmetro município seja None, retorna True.
    """
    if municipio is None:
        return True

    dados_secao = BU(bu).get_dados_secao()
    return dados_secao.municipio == municipio


def verificar_cargo_filtro(resultado_cargo, cargo_filtro):
    """
        Retorna True se o resultado do cargo for correspondente ao cargo passado como parâmetro, false caso contrário.
        Caso o parâmetro cargo seja None, retorna True.
    """
    if cargo_filtro is None:
        return True

    return resultado_cargo == cargo_filtro


def _concatena_no_arquivo_timeline(soma_obj, qtd_bus, timeline_freq):
    """
    Concatena a soma dos votos contida no objeto soma_obj no arquivo timeline.csv.
    O arquivo timeline.csv é um arquivo que contém a soma dos votos de todos os arquivos BU processados até o momento.
    """

    # Cria o arquivo timeline.csv caso ele não exista e escreve o cabeçalho
    if qtd_bus == timeline_freq:
        with open("./timeline.csv", "w") as f:
            f.write("quantidade_bus_somados,cargo,codigo_candidato,quantidade_votos\n")

    with open("./timeline.csv", "a") as f:
        for cargo in soma_obj.soma_por_cargo:
            for codigo_candidato in soma_obj.soma_por_cargo[cargo]:
                resultado_candidato = soma_obj.soma_por_cargo[cargo][codigo_candidato]
                f.write(f"{qtd_bus},{cargo},{codigo_candidato},{resultado_candidato.quantidade_votos}\n")
