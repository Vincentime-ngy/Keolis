
import json

def filter_configurations(config_list, keep_project_id, keep_subsidiary_id, remove_project_id):
    '''
    Filters the configurations based on specified criteria: keeps configurations matching
    the keep_projectId and keep_subsidiaryId, and removes configurations matching the remove_project_id.

    Args:
    - config_list: List of configuration dictionaries.
    - keep_project_id: Project ID to keep.
    - keep_subsidiary_id: Subsidiary ID to keep.
    - remove_project_id: Project ID to remove.

    Returns:
    - Filtered list of configurations.
    '''
    return [
        config for config in config_list
        if (('projectId' in config and config['projectId'] == keep_project_id and
            'subsidiaryId' in config and config['subsidiaryId'] == keep_subsidiary_id) or
            ('projectId' in config and config['projectId'] != remove_project_id))
    ]

def organize_json_data_with_filter(json_path, keep_project_id, keep_subsidiary_id, remove_project_id):
    '''
    Organizes JSON data by basePath including its configurations such as codeQualiacMaintainer,
    paramDisplay, paramExchange, and paramPlanning, with additional filtering based on projectId and subsidiaryId.

    Args:
    - json_path: Path to the JSON file.
    - keep_project_id: Project ID to keep in configurations.
    - keep_subsidiary_id: Subsidiary ID to keep in configurations.
    - remove_project_id: Project ID to remove from configurations.

    Returns:
    - A dictionary with organized and filtered data.
    '''
    with open(json_path, 'r') as file:
        data = json.load(file)['_embedded']['credentials']
    
    organized_data = {}
    for credential in data:
        for subsidiary in credential['credentialSubsidiaries']:
            base_path = subsidiary['subsidiary']['basePath']
            code_qualiac_maintainer = subsidiary['subsidiary'].get('codeQualiacMaintainer', '')
            # Apply filtering to the configuration lists
            param_display = filter_configurations(subsidiary['subsidiary'].get('paramDisplay', []), keep_project_id, keep_subsidiary_id, remove_project_id)
            param_exchange = filter_configurations(subsidiary['subsidiary'].get('paramExchange', []), keep_project_id, keep_subsidiary_id, remove_project_id)
            param_planning = filter_configurations(subsidiary['subsidiary'].get('paramPlanning', []), keep_project_id, keep_subsidiary_id, remove_project_id)
            
            organized_data[base_path] = {
                'codeQualiacMaintainer': code_qualiac_maintainer,
                'paramDisplay': param_display,
                'paramExchange': param_exchange,
                'paramPlanning': param_planning
            }
    
    return organized_data

def save_organized_data(organized_data, output_path):
    with open(output_path, 'w') as file:
        json.dump(organized_data, file, indent=4)

# Example usage
json_path = 'C:/Users/Vincent/Documents/Keolis/exportSocle.json'  # Replace with the path to your input JSON file
output_path = 'C:/Users/Vincent/Documents/Keolis/organise_exportSocle.json'  # Replace with your desired output path
keep_project_id = "a84b23e3-cab7-4156-8ecf-24b8d6502fa7"
keep_subsidiary_id = "941b286c-a442-49d3-ae64-99cbe6a7d82b"
remove_project_id = "abf15fac-97df-46d7-a2e7-7c91700f255b"

# Organize and filter the JSON data
organized_data = organize_json_data_with_filter(json_path, keep_project_id, keep_subsidiary_id, remove_project_id)

# Save the organized and filtered data
save_organized_data(organized_data, output_path)
