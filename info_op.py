import json_op
import taskinfo
from main import GLOBAL_VAR_FILEPATH_ROOT, GLOBAL_VAR_COUNT, GLOBAL_VAR_NOW_TASK_FILEPATH
class InfoOp:
    def __init__(self, task_start_time, task_end_time, task_len, importance, feeling, sfc, task_status, task_id, task_name, filename):
        self.my_task_start_time = task_start_time
        self.my_task_end_time = task_end_time
        self.my_task_len = task_len
        self.my_importance = importance
        self.my_feeling = feeling
        self.my_sfc = sfc
        self.my_task_status = task_status
        self.my_task_id = task_id

        self.my_task_name = task_name
        self.my_file_path = filename.replace('txt', 'json')
        self.my_task_info_dict = self.method_init_dict()
        self.method_op_dict()


        self.method_save_to_json()

    def method_init_dict(self) ->dict:
        lv_task_info_dict = taskinfo.TaskInfo.static_method_get_task_info_json_dict_format()
        return lv_task_info_dict
    def method_op_dict(self):
        self.my_task_info_dict['task_id'] = self.my_task_id
        self.my_task_info_dict['task_name'] = self.my_task_name
        self.my_task_info_dict['start_time'] = self.my_task_start_time
        self.my_task_info_dict['end_time'] = self.my_task_end_time
        self.my_task_info_dict['task_len'] = self.my_task_len
        self.my_task_info_dict['importance'] = self.my_importance
        self.my_task_info_dict['feeling'] = self.my_feeling
        self.my_task_info_dict['statisfaction'] = self.my_sfc
        self.my_task_info_dict['task_status'] = self.my_task_status

    def method_save_to_json(self):
        lv_today_task_info_dict = {}
        try:
            lv_today_task_info_dict: dict = json_op.JsonOp.static_method_read_from_json(json_file_name=self.my_file_path)
        except:
            print('error')
        lv_today_task_info_dict[self.my_task_id] = self.my_task_info_dict
        json_op.JsonOp.static_method_save_to_json(json_file_name=self.my_file_path, save_dict=lv_today_task_info_dict)
