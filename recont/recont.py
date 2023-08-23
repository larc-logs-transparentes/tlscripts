from bu_class import BU
from json_utils import get_json_data
from bu_functions import soma_votos

f, bus_json = get_json_data('recont/results/bu_imgbu_logjez_rdv_vscmr_2022_1t_SP.json')
resultado_presidente = soma_votos(bus_json).soma_por_cargo['presidente']
for codigo_presidente in resultado_presidente.keys():
    print(f'{codigo_presidente}: {resultado_presidente[codigo_presidente]}')
f.close()