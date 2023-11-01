from utils.args_parser_utils import parser
from utils.json_utils import get_json_data_from_file, get_json_data_from_dir, print_dict
from timeit import default_timer as timer
from bu_functions import soma_votos

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
        
    print_dict(resultado, args.output)
    
    print(f"Tempo de execução: {int(timer() - timer_start)} segundos")