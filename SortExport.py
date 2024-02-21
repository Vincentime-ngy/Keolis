import re
import json

# Chemin du fichier d'entrée et de sortie
input_file_path = 'C:/Users/Vincent/Documents/Keolis/exportSocle.json'
output_file_path = 'C:/Users/Vincent/Documents/Keolis/data.txt'

def extract_and_write_information(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Extraction des informations de base
    basePath = re.findall(r'"basePath"\s*:\s*"([^"]+)"', content)
    codeQualiacMaintainer = re.findall(r'"codeQualiacMaintainer"\s*:\s*"([^"]+)"', content)
    
    # Fonction pour filtrer les données basées sur l'id et supprimer la clé _links
    def filter_by_id_and_remove_links(data_section, id_value):
        filtered = []
        for item in json.loads(data_section[0]) if data_section else []:
            if item.get('id') == id_value:
                item.pop('_links', None)  # Supprime la clé _links si elle existe
                filtered.append(item)
        return filtered

    # Extraction et filtrage de paramDisplay, paramExchange, et paramPlanning
    paramDisplay_filtered = filter_by_id_and_remove_links(re.findall(r'"paramDisplay"\s*:\s*(\[[\s\S]*?\])', content), "941b286c-a442-49d3-ae64-99cbe6a7d82b")
    paramExchange_filtered = filter_by_id_and_remove_links(re.findall(r'"paramExchange"\s*:\s*(\[[\s\S]*?\])', content), "941b286c-a442-49d3-ae64-99cbe6a7d82b")
    paramPlanning_filtered = filter_by_id_and_remove_links(re.findall(r'"paramPlanning"\s*:\s*(\[[\s\S]*?\])', content), "941b286c-a442-49d3-ae64-99cbe6a7d82b")
    

    # Préparation des données à écrire
    data_to_write = {
        "basePath": basePath,
        "codeQualiacMaintainer": codeQualiacMaintainer,
        "paramDisplay": paramDisplay_filtered,
        "paramExchange": paramExchange_filtered,
        "paramPlanning": paramPlanning_filtered
    }

    # Écriture dans le fichier de sortie
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for key, values in data_to_write.items():
            file.write(f'{key}:[\n')
            for value in values:
                file.write(f'{json.dumps(value, ensure_ascii=False, indent=4)}\n')
            file.write(']\n\n')

# Exécution de la fonction
extract_and_write_information(input_file_path, output_file_path)
