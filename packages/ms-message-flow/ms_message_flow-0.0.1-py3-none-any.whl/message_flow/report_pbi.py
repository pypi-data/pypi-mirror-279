import os
import json
from msal import PublicClientApplication
import logging
import requests
import time
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request


class export_report__to_image:
    def __init__(self, client_id, tenant_id, username, password):
        # Atributos da classe
        self.client_id = client_id
        self.tenant_id = tenant_id
        self.authority_url = 'https://login.microsoftonline.com/' + tenant_id
        self.scope = ['https://analysis.windows.net/powerbi/api/.default']
        self.url_groups = 'https://api.powerbi.com/v1.0/myorg/groups'
        self.username = username
        self.password = password
        self.access_token = None
        # Obtendo o token de acesso
        self.__obter_token()

    # Método para obter o token de acesso
    def __obter_token(self):
        app = PublicClientApplication(
            self.client_id, authority=self.authority_url)
        result = app.acquire_token_by_username_password(
            username=self.username, password=self.password, scopes=self.scope)
        if 'access_token' in result:
            self.access_token = result['access_token']
            return True
        else:
            logging.error(result.get("error"))
            logging(result.get("error_description"))
            return

    # Método para obter o token de acesso
    def __post_export_to_file_api(self, url, payload):
        # Definindo os cabeçalhos da requisição
        headers = {
            "Content-Type": "application/json",
            'Authorization': f"Bearer {self.access_token}"
        }
        # Convertendo o payload em uma string JSON
        json_payload = json.dumps(payload)
        # Codificando o payload em bytes
        post_payload = json_payload.encode("utf-8")
        # Criando um objeto Request com o url, os cabeçalhos e o payload
        request_post = Request(url, headers=headers, data=post_payload)
        # Abrindo a requisição e lendo a resposta
        with urlopen(request_post, timeout=10) as response:
            body_post = response.read()
        # Retornando a resposta como um dicionário Python
        return json.loads(body_post)

    # Método para verificar o status de uma requisição
    def __get_status(self, url):
        # Definindo os cabeçalhos da requisição
        headers = {
            "Content-Type": "application/json",
            'Authorization': f"Bearer {self.access_token}"
        }
        # Criando um objeto Request com o url e os cabeçalhos
        request_status = Request(url, headers=headers)
        # Abrindo a requisição e lendo a resposta
        with urlopen(request_status, timeout=10) as response:
            body_status = response.read()
        # Retornando a resposta como um dicionário Python
        return json.loads(body_status)

    # Método para baixar um arquivo
    def __download_file_exported(self, url):
        # Definindo os cabeçalhos da requisição
        headers = {
            "Content-Type": "application/json",
            'Authorization': f"Bearer {self.access_token}"
        }
        # Fazendo uma requisição GET com o url e os cabeçalhos
        response_download = requests.request("GET", url=url, headers=headers)
        # Retornando a resposta como um objeto Response
        return response_download

    def get_report_image(self, report_id, visual_name, page_name, filter):
        url = "https://api.powerbi.com/v1.0/myorg/reports/" + report_id + "/ExportTo"
        payload = {
                    "format": "PNG", 
                    "powerBIReportConfiguration": {
                        "pages": [{"visualName": visual_name, "pageName": page_name}],
                        "reportLevelFilters": [{"filter": filter}]
                    }
                } 

        # Postando a requisição de exportação e obtendo o id da exportação
        data = self.__post_export_to_file_api(url, payload)
        export_id = data['id']

        # Definindo o url para verificar o status da exportação
        exportstatusurl = 'https://api.powerbi.com/v1.0/myorg/reports/' + \
            report_id + '/exports/' + export_id

        # Criando um loop para verificar o status da exportação
        while True:
            try:
                # Verificando o status da exportação
                response_status = self.__get_status(exportstatusurl)
                status = response_status['status']
                logging.warning(status)
                if status == 'Succeeded':
                    # Se o status for Succeeded, sair do loop
                    logging.warning('A exportação foi concluída com sucesso')
                    break
                else:
                    # Se o status for diferente de Succeeded, esperar 10 segundos e repetir o loop
                    logging.warning('A exportação ainda está em andamento')
                    time.sleep(10)
            except URLError as e:
                # Se ocorrer um erro de URL, imprimir o erro e sair do loop
                logging.warning('Ocorreu um erro na requisição:', e)
                break
            except ValueError as e:
                # Se ocorrer um erro de decodificação JSON, imprimir o erro e sair do loop
                logging.warning('Ocorreu um erro na decodificação JSON:', e)
                break
            except HTTPError as error:
                # Se ocorrer um erro HTTP, imprimir o status e a razão e sair do loop
                logging.warning(error.status, error.reason)
                break

        # Definindo o url para baixar o arquivo
        download_url = exportstatusurl + '/file'
        # Baixando o arquivo e obtendo a resposta
        response_download = self.__download_file_exported(download_url)

        # Pegando data e hora atual
        data_hora_atual = datetime.now()
        # Convertendo em string
        timestemp = data_hora_atual.strftime('%Y-%m-%d-%H-%M-%S')

        # Gerando nome do arquivo
        filename = timestemp + '-' + page_name + visual_name + '.png'

        # Escrevendo o conteúdo da resposta em um arquivo local
        with open(filename, 'wb') as output_file:
            output_file.write(response_download.content)
        return filename
