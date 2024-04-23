import argparse
import pathlib

parser = argparse.ArgumentParser(description='Preprocessamento de arquivos BUs.')
parser.add_argument('raw_bu_path', help='Arquivo ou diretório de arquivos BU', type=pathlib.Path)
parser.add_argument('results_path', help='Diretório para salvar os resultados', type=pathlib.Path)