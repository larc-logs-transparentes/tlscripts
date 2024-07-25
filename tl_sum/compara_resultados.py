# get json from files and compare them

import json
import sys
import os

def get_json_from_file(file):
    with open(file, encoding="utf8") as f:
        return json.load(f)

def compare_jsons(calculated, official):
    for candidate_number in calculated["soma_por_cargo"]["deputadoEstadual"]:
        for i in official["cand"]:
            if i["n"] == candidate_number:
                if int(i["vap"]) != calculated["soma_por_cargo"]["deputadoEstadual"][candidate_number]["quantidade_votos"]:
                    print("Candidate %s has different number of votes" % candidate_number)
                    print("Official: %s" % i["vap"])
                    print("Calculated: %s" % calculated["soma_por_cargo"]["deputadoEstadual"][candidate_number]["quantidade_votos"])
                    #print("Candidate %s found in official file" % candidate_number)
                break
        else:
            print("Candidate %s not found in official file" % candidate_number)
       

def main():
    if len(sys.argv) != 3:
        print("Usage: python compara_resultados.py file1 file2")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    if not os.path.exists(file1):
        print("File %s does not exist" % file1)
        sys.exit(1)

    if not os.path.exists(file2):
        print("File %s does not exist" % file2)
        sys.exit(1)

    json1 = get_json_from_file(file1)
    json2 = get_json_from_file(file2)

    compare_jsons(json1, json2)

if __name__ == "__main__":
    main()
