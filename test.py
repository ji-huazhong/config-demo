def dict_to_args(dictionary):
    result = []

    def flatten_dict(current_dict, prefix=""):
        for key, value in current_dict.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flatten_dict(value, new_prefix)
            else:
                if isinstance(value, bool):
                    value = str(value).lower()
                result.append(f"--{new_prefix}={value}")

    flatten_dict(dictionary)
    return result


nested_dict = {
    'model': {
        'network': {
            'use_mcore_models': True,
            'num_layers': 28,
            'hidden_size': 3584,
            'ffn_hidden_size': 18944
        }
    },
    'data': {
        'global_batch_size': 1
    },
    'trainer': {
        'precision': 'bf16'
    },
    'actor': {
        'model': {
            'network': {
                'num_layers': 14
            }
        }
    }
}
print(nested_dict)
print('-' * 20)
print(dict_to_args(nested_dict))