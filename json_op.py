import json


class JsonOp:
    def __int__(self):
        pass

    @staticmethod
    def static_method_save_to_json(json_file_name: str, save_dict: dict):
        with open(json_file_name, 'w') as f:
            json.dump(save_dict, f, indent=4, ensure_ascii=False)

    @staticmethod
    def static_method_read_from_json(json_file_name: str) -> dict:
        with open(json_file_name, 'r', encoding='utf-8') as f:
            local_var_json_dict = json.load(f)
        return local_var_json_dict

