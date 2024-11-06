from pathlib import Path
from time import sleep
from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import sqlite3
import sys
import os

def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Browser:
    ROOT_FOLDER = Path(__file__).parent
    CHROME_DRIVER_PATH = ROOT_FOLDER / 'src' / 'drivers' / 'chromedriver.exe'
    SELECTOR_TABLE = '#td-precos_taxas-tab_1 > div > div.td-mercado-titulos__content > table'
    LINK = 'https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm'

    def __init__(self, hide=True) -> None:
        self.titulos = ['titulo','ano','rentabilidade_anual','investimento_minimo','preco_unitario', 'vencimento']

        self.driver = self.make_chrome_browser()
        if hide == True:
            self.driver.set_window_position(-10000,0)
        self.driver.get(self.LINK)
        pass

    def make_chrome_browser(self,*options: str) -> webdriver.Chrome:
        chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_argument('--headless')
        if options is not None:
            for option in options:
                chrome_options.add_argument(option)

        chrome_service = Service(
            executable_path=str(self.CHROME_DRIVER_PATH),
        )

        browser = webdriver.Chrome(
            service=chrome_service,
            options=chrome_options
        )

        return browser
    
    
    def search(self) -> list[dict]:
        tabela = self.driver.find_element(By.CSS_SELECTOR, self.SELECTOR_TABLE)

        linhas = tabela.find_elements(By.TAG_NAME, 'tbody')

        conteudos = [
            linha.find_elements(By.TAG_NAME, 'span') for linha in linhas
        ]

        lista_nova = []
        for conteudo in conteudos:
            lista_nova.append(
                dict(zip(
                        self.titulos, 
                        [x.text for x in conteudo if x.text != '']
                        )
                    )
                )

        return lista_nova
    
class Email:
    def __init__(self) -> None:
        self.addresse = ['']
        self.email_sender = ''
        self.passwrd_sender = ''

        self.base_html = '''



        '''
        pass

    def create_message(self, list):
        ...

    def send(self):
        ...

class DataBase:
    NOME_DB = 'tesouro_db.sqlite3'
    FOLDER_DB = resource_path(f'src\\db\\{NOME_DB}')
    TABLE_LATE = 'Infos_Late'
    TABLE_CONST = 'Infos_Const'

    def __init__(self) -> None:
        self.query_columns = (
            'PRAGMA table_info({0});'
        )

        self.query_late = (
            'SELECT * FROM {0}'
        )

        self.insert_late = (
            'INSERT INTO {0} '
            '(Titulo, Ano, Rentabilidade_Anual, Investimento_Minimo, Preco_Unitario, Vencimento)'
            ' VALUES '
            '(:titulo, :ano, :rentabilidade_anual, :investimento_minimo, :preco_unitario, :vencimento)'
        )



        self.insert_const = (
            f'INSERT INTO {self.TABLE_CONST}'
            '* VALUES '
            '(:titulo, :rentabilidade_anual)'
        )

        self.connection = sqlite3.connect(self.FOLDER_DB)
        self.cursor = self.connection.cursor()
        pass

    def filter_moveless(self, contents: list[dict]):
        self.cursor.execute(
            self.query_late.format(self.TABLE_LATE)
        )
        lates_moves = self.cursor.fetchall()
        print(lates_moves)
        # filtred_moves = []
        # for move in lates_moves:
        #     for content in contents:
        #         if content['Titulo'] == move['Titulo']\
        #             and content['rentabilidade_anual'] == move['rentabilidade_anual']:
        #             filtred_moves.append(content)

        # return filtred_moves


    def update(self, move: list[dict]):
        self.cursor.executemany(
            self.insert_late.format(
                self.TABLE_LATE
            ),
            (x.values for x in x for x in move)
        )

if __name__ == '__main__':
    try:
        browser = Browser()
        email = Email()
        db = DataBase()
        content = [
            {
                'a': 'b'
            }
        ]

        # content = browser.search()
        move = db.filter_moveless(content)

        # email.create_message(content)
        # email.send()
        
        
        db.update(content)
    except Exception as err:
        print(err)