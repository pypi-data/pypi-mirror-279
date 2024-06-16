import yaml


def check_yaml_structure(file_path, required_structure):
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(f"Error parsing YAML file: {exc}")
            return False

    return validate_structure(data, required_structure)


def validate_structure(data, required_structure):
    if not isinstance(data, dict):
        print("The YAML root structure is not a dictionary.")
        return False

    for key, expected_type in required_structure.items():
        if key not in data:
            print(f"Key '{key}' is missing from the YAML file.")
            return False

        if not isinstance(data[key], expected_type):
            print(f"Key '{key}' is not of type {expected_type.__name__}.")
            return False

    return True


# Example usage
required_structure = {
    'name': str,
    'age': int,
    'address': dict
}

file_path = 'path/to/your/file.yaml'
is_valid = check_yaml_structure(file_path, required_structure)
print(f"YAML file structure is valid: {is_valid}")