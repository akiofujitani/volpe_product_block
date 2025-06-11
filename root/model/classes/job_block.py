import logging
from datetime import datetime


logger = logging.getLogger('job_block')


class JobBlock:
    r'''
    JobBlock
    --------

    Args
        - job_number -> int
        - insertion_date -> datetime
    '''
    def __init__(self, job_number: int, insertion_date: datetime) -> None:
        self.job_number = job_number
        self.insertion_date = insertion_date

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(__o, key):
                    return False
            return True


    @classmethod
    def init_dict(cls, dict_values: dict[str, str]) -> object:
        job_number = int(dict_values.get('job_number'))
        insertion_date = datetime.strptime(dict_values.get('insertion_date'), '%Y/%m/%d %H:%M:%S')
        return cls(job_number, insertion_date)
   

class JobList:
    r'''
    JobList
    -------

    Args
        - job_list -> list[JobBlock]
    
    '''
    def __init__(self, job_list: list[JobBlock]) -> None:
        self.job_list = job_list

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(__o, key):
                    return False
            return True

    def add_job(self, job_number: int) -> bool:
        try:
            job_number = int(job_number)
            if isinstance(job_number, int):
                if not job_number in self.get_job_list():
                    self.job_list.append(JobBlock(job_number, datetime.now()))
                    return True
            return False
        except Exception as error:
            logger.error(f'Error {error}')
            return False
    
    def remove_job(self, job_number: int) -> bool:
        if isinstance(job_number, int):
            for index, job_block in enumerate(self.job_list):
                if int(job_number) == job_block.job_number:
                    self.job_list.pop(index)
                    return True
        return False

    def get_job_list(self) -> list[int]:
        return [job.job_number for job in self.job_list]

    def remove_older_than(self, date_value: datetime) -> None:
        for job in self.job_list:
            if job.insertion_date < date_value:
                self.remove_job(job.job_number)

    @classmethod
    def init_dict(cls, dict_values: dict[str, str]) -> object:
        job_list = []
        if dict_values.get('job_list'):
            for job_value in dict_values.get('job_list'):
                job_list.append(JobBlock.init_dict(job_value))
        return cls(job_list)    