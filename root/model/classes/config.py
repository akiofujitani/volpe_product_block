from os.path import normpath, abspath
from datetime import time

class Configuration:
    '''
    Configuration
    -------------
        - csv_in_path
        - csv_done_path
        - csv_block_list_path
        - csv_delimiter
        - csv_extension
        - before_start_time

    Methods
        - init_dict (classmethod)

    '''    
    def __init__(self, csv_in_path: str, csv_done_path: str, csv_block_list_path: str, csv_delimiter: str, csv_extension: str, batch_amount: int, table_insertion_time: float, before_start_time: int) -> None:
        self.csv_in_path = csv_in_path
        self.csv_done_path = csv_done_path
        self.csv_block_list_path = csv_block_list_path
        self.csv_delimiter = csv_delimiter
        self.csv_extension = csv_extension
        self.batch_amount = batch_amount
        self.table_insertion_time = table_insertion_time
        self.before_start_time = before_start_time

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True

    def add_printer(self, printer_name: str) -> bool:
        if not printer_name in self.printer_list:
            self.printer_list.append(printer_name)
            self.printer_list.sort()
            return True
        return False

    def remove_printer(self, printer_name: str) -> bool:
        if printer_name in self.printer_list:
            self.printer_list.remove(printer_name)
            return True
        return False

    @classmethod
    def init_dict(cls, setting_dict: dict[str, str]):
        csv_in_path = abspath(normpath(setting_dict.get('csv_in_path')))
        csv_done_path = abspath(normpath(setting_dict.get('csv_done_path')))
        csv_block_list_path = abspath(normpath(setting_dict.get('csv_block_list_path')))
        csv_delimiter = setting_dict.get('csv_delimiter')
        csv_extension = setting_dict.get('csv_extension')
        batch_amount = int(setting_dict.get('batch_amount'))
        table_insertion_time = float(setting_dict.get('table_insertion_time'))
        before_start_time = int(setting_dict.get('before_start_time'))
        return cls(csv_in_path, csv_done_path, csv_block_list_path, csv_delimiter, csv_extension, batch_amount, table_insertion_time, before_start_time)