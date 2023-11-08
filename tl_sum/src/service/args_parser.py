import argparse
import pathlib

parser = argparse.ArgumentParser(description='Soma os votos de um ou mais arquivos BU')
parser.add_argument('bu_path', help='Arquivo ou diretório de arquivos BU', type=pathlib.Path)
parser.add_argument('--cargo', help='Cargo que será realizado a soma dos votos', type=str, choices=['presidente', 'governador', 'senador', 'deputadoFederal', 'deputadoEstadual', 'prefeito'])
parser.add_argument('--estado', help='Define o estado que se deseja realizar a soma dos votos', type=str, choices=['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO', 'ZZ'])
parser.add_argument('--municipio', help='Código TSE do município que se deseja realizar a soma dos votos', type=int)
parser.add_argument('--output', help='Arquivo de saída', type=pathlib.Path)
parser.add_argument('--timeline_frequencia', help='Frequência de atualização do estado da soma no arquivo de timeline', type=int)