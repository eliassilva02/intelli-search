from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from time import sleep
import time

import urllib
import requests
import re
import tensorflow as tf
import os 

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

tf.get_logger().setLevel('ERROR')

class WebClient:
    def __init__(self):
        self.chrome_options = ChromeOptions()
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument("window-size=1,1")
        self.chrome_options.add_argument("window-position=0,0")

        self.web_driver = Chrome(options=self.chrome_options)
        self.base_url: str = "https://www.google.com/search?q={descricao_produto}&gs_lcrp=EgZjaHJvbWUqBggAEEUYOzIGCAAQRRg7MgYIARBFGDkyBggCEEUYOzIGCAMQRRg70gEIMjA2OWowajeoAgCwAgA&sourceid=chrome&ie=UTF-8"
        self.headers: dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
        }


    def search(self, descricao_produto: str, max_results: int):
        descricao_produto: str = urllib.parse.quote_plus(descricao_produto)

        self.web_driver.get(self.base_url.format(descricao_produto=descricao_produto))

        sleep(0.5)

        html_content = self.web_driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        data = []

        for result in soup.find("div",{"class":"dURPMd"}).find_all("div",{"class":"Ww4FFb"})[:max_results]:
            title = result.select_one('h3').text if result.select_one('h3') else "Sem título"
            link = result.select_one('a')['href'] if result.select_one('a') else "Sem link"
            snippet = result.select_one('.VwiC3b').text if result.select_one('.VwiC3b') else "Sem descrição"

            data.append({
                'title': title,
                'link': link,
                'snippet': snippet
            })

        return data


    def extract(self, url: str):
        """
        Extrai dados de uma URL e retorna o resultado em formato JSON,
        ignorando textos em menus de navegação.
        
        Args:
            url (str): URL do produto da Coca-Cola
            
        Returns:
            str: JSON com os dados extraídos
        """
        start_time = time.time()
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remover elementos de navegação e menus antes de extrair o texto
            elementos_navegacao = soup.find_all(['nav', 'header', 'footer'])
            elementos_navegacao += soup.find_all(class_=lambda c: c and ('menu' in c.lower() or 
                                                                        'nav' in c.lower() or 
                                                                        'header' in c.lower() or 
                                                                        'footer' in c.lower()))
            
            # Remover elementos de navegação identificados
            for elemento in elementos_navegacao:
                elemento.decompose()
            
            for script in soup(['script', 'style']):
                script.decompose()
                
            # Extrair o conteúdo de texto da página sem menus
            raw_content = soup.get_text(separator="\n", strip=True)
            
            # Limpar linhas vazias múltiplas
            raw_content = re.sub(r'\n\s*\n', '\n\n', raw_content)
            
            # Extrair imagens do produto
            images = []
            # Tentativa para encontrar imagens do produto
            img_tags = soup.select('img[src*="arquivos/ids"]')
            for img in img_tags:
                if 'src' in img.attrs:
                    images.append(img['src'])
            
            # Montar o resultado
            result = {
                "results": [
                    {
                        "url": url,
                        "raw_content": raw_content,
                        "images": images
                    }
                ],
                "failed_results": [],
                "response_time": round(time.time() - start_time, 2)
            }
            
            return result
        
        except Exception as e:
            # Em caso de erro
            result = {
                "results": [],
                "failed_results": [
                    {
                        "url": url,
                        "error": str(e)
                    }
                ],
                "response_time": round(time.time() - start_time, 2)
            }
            
            return result