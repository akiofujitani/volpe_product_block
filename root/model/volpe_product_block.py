import logging
import pyautogui
import keyboard
from os.path import join
from threading import Event
from time import sleep
from datetime import datetime
from .scripts.file_handler import file_list, csv_to_list, listToCSV
from .scripts import erp_volpe_handler
from .scripts import win_handler
from .database import Database
from .classes.config import Configuration


logger = logging.getLogger('volpe_product_block')


IMG_PATH = 'Images/Registry'


def load_csv(csv_in_path: str, csv_extension: str, csv_delimiter: str) -> list[dict[str, str]]:
    '''
    load_csv
    --------

    Get csv files in path and loads it in list    
    '''
    csv_path = csv_in_path
    files_list = file_list(csv_path, csv_extension)
    csv_contents_list = []
    if len(files_list) > 0:
        for file in files_list:
            csv_contents = csv_to_list(join(csv_path, file), csv_delimiter)
            if csv_contents:
                csv_contents_list += csv_contents
    return csv_contents_list


def subtract_list(main_list: list[dict[str, str]], remove_list: list[dict[str, str]]) -> list[dict[str, str]]:
    '''
    subtract_list
    -------------

    get two lists of code/customer type en subtract eachother
    
    '''
    update_list = []
    code_list = [customer.get('CODE') for customer in remove_list]
    for customer in main_list:
        if not customer.get('CODE') in code_list:
            update_list.append(customer)    
    return update_list


def set_insert_customer_list(customer_list: list[dict[str, str]], done_list: list[dict[str, str]], batch_amount: int=30) -> list[dict[str, str]]:
    '''
    Set Insert Customer List
    ------------------------

    Update customer_list removing values in the done_list
    Create list of customers based on the batch_amount
    '''
    update_list = subtract_list(customer_list, done_list)
    batch_list = []
    for i, customer in enumerate(update_list):
        batch_list.append(customer)
        i += 1
        if i == batch_amount:
            break
    return batch_list


def insert_customer_list(customer_list: list[str]) -> None:
    '''
    Insert Customer List
    --------------------

    Insert each customer code in customer list in the list
    
    '''
    sleep(2.0)
    customer_win = win_handler.image_search("Title_select_customer.png", path=IMG_PATH)
    if customer_win:
        customer_amount = len(customer_list) - 1
        for i, customer in enumerate(customer_list):
            logger.info(f'{i: >3} CODE {customer.get("CODE")} - {customer.get("CUSTOMER")}')
            pyautogui.write(customer.get('CODE'))
            sleep(0.3)
            send_tab(3)
            pyautogui.press('space')
            sleep(0.5)
            send_tab(4)
            pyautogui.press('space')
            sleep(0.5)  
            send_tab(3)
            if i == customer_amount:
                pyautogui.press('space')
                sleep(1.0)
                return
            send_tab(3)
            sleep(0.5)     
    return 


def clear_field() -> None:
    '''
    Clear Fiels
    -----------

    Clear product field
    '''
    keyboard.press_and_release('ctrl + a')
    sleep(0.5)
    pyautogui.press('backspace')
    sleep(0.5)
    return


def show_inactive() -> None:
    '''
    Show Inactive
    -------------

    Ativate checkbox to show deactivated products

    '''
    for _ in range(3):
        pyautogui.press('tab')
        sleep(0.3)
    pyautogui.press('space')
    for _ in range(3):
        keyboard.press_and_release('shift + tab')
        sleep(0.3)
    return


def send_tab(tab_times: int, sleep_time: float=0.2) -> None:
    '''
    Send Tab
    --------

    Send tab the number of times set.

    '''
    for _ in range(tab_times):
        pyautogui.press('tab')
        sleep(sleep_time)
    return

def insert_product_block(product_block_list: list[dict[str, str]], inactive: bool=False) -> None:
    '''
    Insert Product Block
    --------------------

    Automation to insert products in list to be blocked.
    '''
    sleep(2.0)
    product_win = win_handler.image_search("Title_select_product.png", path=IMG_PATH)
    if product_win:
        if inactive:
            show_inactive()
        product_count = len(product_block_list) - 1
        for i, product in enumerate(product_block_list):
            logger.info(f'{i: >3} PRODUCT {product.get("CODE")} - {product.get("PRODUCT")}')
            pyautogui.write(product.get('CODE'))
            sleep(0.3)
            send_tab(2)
            sleep(0.5)
            pyautogui.press('space')
            sleep(0.3)
            send_tab(6)
            sleep(0.3)
            pyautogui.press('space')
            sleep(0.3)
            send_tab(2)
            if i == product_count:
                pyautogui.press('space')
                sleep(1.0)
                return
            sleep(0.3)
            send_tab(2)
            clear_field()
    return


def product_configuration() -> None:
    '''
    product_configuration
    ---------------------

    Set insertion window
    '''
    header_pos = win_handler.image_search("Product_bloc_Table_headers.png", path=IMG_PATH)
    win_handler.click_field(header_pos, 'Bellow')
    sleep(0.5)
    pyautogui.press('i')
    sleep(1.0)
    pyautogui.press('space')
    return


def product_block_main(event: Event, configuration: Configuration) -> None:
    '''
    Prdocut Block Main
    ------------------

        - event
        - configuration

    1. load and proccess csv getting customer list with the following format:
    customer_list : list[
        Dict[CODE: int, CUSTOMER: str]
    ]
    customer_done_list : list[
        Dict[CODE: int, CUSTOMER: str]
    ]
    products_block_list : list[
        Dict[CODE: int, PRODUCT: str]
    ]

    2. Set Volpe to start automation routine

    3. Main automation routine

    '''
    # 1. load and proccess csv
    if event.is_set():
        logger.info('Terminating routine')
        return

    customer_list = load_csv(configuration.csv_in_path, configuration.csv_extension, configuration.csv_delimiter)
    customer_done_list = load_csv(configuration.csv_done_path, configuration.csv_extension, configuration.csv_delimiter)
    product_block_list = load_csv(configuration.csv_block_list_path, configuration.csv_extension, configuration.csv_delimiter)
    if event.is_set():
        logger.info('Terminating routine')
        return

    # 2. Set volpe routine
    try:
        # erp_volpe_handler.volpe_back_to_main()
        erp_volpe_handler.volpe_load_tab('Tab_reg', 'Icon_Reg_par.png')
        erp_volpe_handler.volpe_open_window('Icon_Products_block.png', 'Title_products_block.png', path=IMG_PATH)
        if event.is_set():
            logger.info('Terminating routine')
            return        
    except Exception as error:
        logger.warning(f'Volpe error or not found {error}')
        event.set()
        return
    
    # 3. Main automation routine
    try: 
        while len(customer_list) > 0:
            if event.is_set():
                logger.info('Terminating routine')
                return
            logger.info('Starting...')
            product_configuration()
            batch_list = set_insert_customer_list(customer_list, customer_done_list, configuration.batch_amount)
            if event.is_set():
                logger.info('Terminating routine')
                return            
            insert_customer_list(batch_list)
            pyautogui.press('tab')
            sleep(0.5)
            pyautogui.press('space')
            if event.is_set():
                logger.info('Terminating routine')
                return            
            insert_product_block(product_block_list, True)
            pyautogui.press('tab')
            sleep(0.5)
            pyautogui.press('space')

            listToCSV(batch_list, join(configuration.csv_done_path, f'{datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")}.{configuration.csv_extension}'))
            wait_time = len(product_block_list) * 0.05 * len(batch_list)
            logger.info(f'Waiting... {wait_time}')
            sleep(wait_time)
            customer_list = subtract_list(customer_list, batch_list)
            customer_done_list += batch_list
            if event.is_set():
                logger.info('Terminating routine')
                return
    except Exception as error:
        logger.warning(f'Error in automation due {error}')
        event.set()
        return


def volpe_product_block(database: Database, event: Event) -> None:
    '''
    Start main function to block products in the ERP Volpe
    '''
    logger.info('Print Manager')

    if event.is_set():
        return
    try:
        config = database.config.get('config')
    except Exception as error:
        logger.critical(f'Could not load config file due {error}')
        event.set()
        return
    
    if config.before_start_time:
        logger.info(f'Initialization delay: {config.before_start_time} seconds...')
        for _ in range(config.before_start_time):
            if event.is_set():
                return
            sleep(1)
    product_block_main(event, config)