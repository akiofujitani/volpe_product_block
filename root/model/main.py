import logging
from threading import Event, Thread
from .volpe_product_block import volpe_product_block
from .database import Database
from .scripts.json_config import load_json_config
from .templates import data_object_list


logger = logging.getLogger('main_model')

class Model():
    '''
    Model main class
    '''
    def __init__(self) -> None:
        try:
            self.database = Database.init_dict(load_json_config('./data/data_object_list.json', data_object_list))  
            # self.gui_configuration = GuiConfiguration.init_dict(load_json_config('./data/gui_configuration.json', gui_configuration))
        except Exception as error:
            logger.error(f'Could not load data_object_list.json due {error}')
            raise error
        self.routine_name = 'volpe_product_block'
        self.event = Event()
        self.thread = None
         

    def start_routine(self):
        '''
        Start routine
        '''
        logger.info('starting auto_calc')
        if not self.routine_active():
            self.event.clear()
            self.thread = Thread(target=volpe_product_block, args=(self.database, self.event, ), name=self.routine_name)
            self.thread.start()

    def stop_routine(self):  
        '''
        Stop routine
        '''             
        if self.routine_active():
            logger.info(f'stopping {self.routine_name}')
            self.event.set()
            self.thread.join()
        return

    def restart_routine(self):
        '''
        Restart routine
        '''
        self.stop_routine()
        self.start_routine()

    def routine_active(self):
        '''
        Check if current routine is running
        '''
        if not self.thread:
            logger.info('No thread created')
            return False
        if not self.thread.is_alive():
            logger.info('Thread is already stopped')
            return False
        return True  

    def on_close(self):
        '''
        Ends the routine on application close
        '''
        if not self.thread:
            return
        if not self.thread.is_alive():
            return
        self.stop_routine()
        self.thread.join()
        logger.info('Thread termination complete')