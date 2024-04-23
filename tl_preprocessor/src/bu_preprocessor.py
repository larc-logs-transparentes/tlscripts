import asn1tools
import glob
import os
import base64
import time
import json
from utils.json_utils import get_json_data_from_file
from timeit import default_timer as timer
from .args_parser import parser

ASN1_SPECS_BU = "tl_preprocessor/gov_codes/specification_files/bu.asn1"
RESULT_FOLDER = "res/preprocessed_bu_jsons/eleicao_545/"

conv = asn1tools.compile_files(ASN1_SPECS_BU)


# Helper class to encode BU to JSON
# - Needed to convert fields of type bytes to type hex.
# - Once json is read, hex fields will have to be converted back to bytes
# - JSON does not support bytes
class DictWithBytesToJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (bytes, bytearray)):
            return obj.hex()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)



def create_preprocessed_bu_file(bu_object_file, bu_jsons):
    preprocessed_bu_file_name = os.path.basename(bu_object_file)
    preprocessed_bu_file_path = RESULT_FOLDER + preprocessed_bu_file_name

    with open(preprocessed_bu_file_path, 'w') as preprocessed_bu_file:
        first = True
        for bu_json in bu_jsons:
            if first:
                preprocessed_bu_file.write('[')
                first = False
            else:
                preprocessed_bu_file.write(',')
            preprocessed_bu_file.write(json.dumps(bu_json, cls=DictWithBytesToJsonEncoder, indent=4))
        preprocessed_bu_file.write(']')
    preprocessed_bu_file.close()


def get_bu_jsons(bu_object_file):
    bu_file, bu_objects = get_json_data_from_file(bu_object_file)
    bu_jsons = []
    for bu_object in bu_objects:
        raw_bu = base64.b64decode(bu_object.get('bu').encode('ascii'))
        bu_json = convert_raw_bu_to_json(raw_bu)
        bu_jsons.append(bu_json)
    bu_file.close()
    return bu_jsons


def convert_raw_bu_to_json(raw_bu):
    envelope_decoded = conv.decode("EntidadeEnvelopeGenerico", raw_bu)
    bu_encoded = envelope_decoded['conteudo']
    bu_decoded = conv.decode('EntidadeBoletimUrna', bu_encoded)
    return bu_decoded


def get_list_files_with_extension_in_directory(extension, path):
    files_list = glob.glob(f'{path}/*.{extension}')
    return files_list


def get_bu_object_files(path):
    raw_bus_list = get_list_files_with_extension_in_directory("json", path)
    return raw_bus_list


def preprocess_bus(all_bus_path):
    bu_object_files = get_bu_object_files(all_bus_path)

    if not os.path.exists(RESULT_FOLDER):
        os.makedirs(RESULT_FOLDER)

    counter = 0
    for bu_object_file in bu_object_files:
        bu_jsons = get_bu_jsons(bu_object_file)
        create_preprocessed_bu_file(bu_object_file, bu_jsons)
        counter += 1
        print(f"Preprocessando arquivos BU... {counter}/{len(bu_object_files)}", end="\r")
        

        
if __name__ == '__main__':
    args = parser.parse_args()
    print("Iniciando Preprocessamento...")
    preprocess_bus(args.bu_path)
    print("Preprocessing Terminado. Os arquivos estão disponíveis em", RESULT_FOLDER)
 
