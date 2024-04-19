import argparse
import pathlib

parser = argparse.ArgumentParser(description='Preprocessamento de arquivos BUs.')
parser.add_argument('bu_path', help='Arquivo ou diretório de arquivos BU', type=pathlib.Path)