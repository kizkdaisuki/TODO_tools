
class TaskInfo:
    def __init__(self):
        pass

    @staticmethod
    def static_method_get_task_info_json_dict_format(uid: str = '') -> dict:
        local_var_task_info: dict = {
            'task_id': 0,
            'task_name': '',
            'start_time': '',
            'end_time': '',
            'task_len': 0,
            'task_status': '',
            'importance': 'mid',
            'statisfaction': 3, # 满意度
            'feeling': 'None',
        }

        return local_var_task_info

