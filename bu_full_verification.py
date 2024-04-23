
from tl_downloader.src.download_bu import download_bu, ask_user_which_election
from termcolor import cprint
from tl_preprocessor.src.bu_preprocessor import preprocess_bus
from tl_verifier.src.verify_bus import verify_tree
import json
import datetime
from tl_sum.src.service.json_utils import get_json_data_from_file, get_json_data_from_dir, print_dict
from tl_sum.src.bu_functions import soma_votos
from pathlib import Path
# from tl_sum.tl_sum 




cprint('##########################################################', 'green')
cprint('Bem vindo ao script de verificação completa da eleição', 'green')
cprint('##########################################################', 'green')

tree_name = ask_user_which_election()

cprint('\n\nPasso 1: Baixar os arquivos BUs da eleição', 'green')
print(f'Iniciando download da eleição {tree_name}')
start_time = datetime.datetime.now()
download_bu(tree_name)
end_time = datetime.datetime.now()
print('Download finalizado')
print(end_time - start_time)



cprint('\n\nPasso 2: Verificar os arquivos BUs', 'green')
start_time = datetime.datetime.now()
result = verify_tree(tree_name)
end_time = datetime.datetime.now()
print(json.dumps(result, indent=4))
print(end_time - start_time)




cprint('\n\nPasso 3: Preprocessar os arquivos BUs', 'green')
start_time = datetime.datetime.now()
preprocess_bus('./res/trees/' + tree_name, './res/preprocessed_bu_jsons/' + tree_name)
end_time = datetime.datetime.now()
cprint('\nPreprocessamento finalizado')
print(end_time - start_time)



cprint('\n\nPasso 4: Calcular o resultado da eleição', 'green')
cargo = input("Digite o cargo: ")
start_time = datetime.datetime.now()
files, bus_json = get_json_data_from_dir(Path('./res/preprocessed_bu_jsons/' + tree_name))
resultado = soma_votos(bus_json, cargo)
for f in files:
    f.close()
print_dict(resultado)
end_time = datetime.datetime.now()
print(end_time - start_time)



cprint('\n\nFim do script', 'green')





