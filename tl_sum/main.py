import argparse
import pathlib
from json_utils import get_json_data, print_dict
from bu_functions import soma_votos

parser = argparse.ArgumentParser(description='Soma os votos de um ou mais arquivos BU')

parser.add_argument('bu_path', help='arquivo ou diretório de arquivos BU', type=pathlib.Path)
parser.add_argument('--cargo', help='Cargo que será realizado a soma dos votos', type=str, choices=['presidente', 'governador', 'senador', 'deputadoFederal', 'deputadoEstadual'])
parser.add_argument('--output', help='arquivo de saída', type=pathlib.Path)
args = parser.parse_args()

if(args.bu_path.is_file()):
    f, bus_json = get_json_data(args.bu_path)
    resultado = soma_votos(bus_json, args.cargo)
    f.close()
    
print_dict(resultado, args.output)

""" TODO
- Suporte a diretório de arquivos BU
- Suporte a multiplos cargos
"""