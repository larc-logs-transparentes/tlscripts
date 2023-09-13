import argparse
import pathlib
from timeit import default_timer as timer
from json_utils import get_json_data_from_file, get_json_data_from_dir, print_dict
from bu_functions import soma_votos

parser = argparse.ArgumentParser(description='Soma os votos de um ou mais arquivos BU')
parser.add_argument('bu_path', help='Arquivo ou diretório de arquivos BU', type=pathlib.Path)
parser.add_argument('--cargo', help='Cargo que será realizado a soma dos votos', type=str, choices=['presidente', 'governador', 'senador', 'deputadoFederal', 'deputadoEstadual', 'prefeito'])
parser.add_argument('--municipio', help='Código TSE do município que se deseja realizar a soma dos votos', type=int)
parser.add_argument('--output', help='Arquivo de saída', type=pathlib.Path)

if __name__ == "__main__":
    timer_start = timer()
    
    args = parser.parse_args()

    if(args.bu_path.is_file()):
        f, bus_json = get_json_data_from_file(args.bu_path)
        resultado = soma_votos(bus_json, args.cargo, args.municipio)
        f.close()
        
    if(args.bu_path.is_dir()):
        files, bus_json = get_json_data_from_dir(args.bu_path)
        resultado = soma_votos(bus_json, args.cargo, args.municipio)
        for f in files:
            f.close()
        
    print_dict(resultado, args.output, False)
    
    print(f"Tempo de execução: {int(timer() - timer_start)} segundos")

""" TODO 
- Suporte a multiplos cargos
"""

""" Checklist
AC - OK
AL - OK
AP - OK
AM - 
"""