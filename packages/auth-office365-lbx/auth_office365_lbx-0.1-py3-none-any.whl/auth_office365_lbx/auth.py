import msal
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
import logging
import sys
import os

class auth_office365_lbx:
    def __init__(self, client_id, client_secret, tenant_id, timeout=60, log_file='auth_office365_lbx.log'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.timeout = timeout
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        self.redirect_uri = "http://localhost:8000"
        self.response = ""
        self.status_code = 0
        self.server = None

        # Configura o logger
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def valida_grupo(self, grupo):
        # Redireciona stdout e stderr para arquivos de log
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = open('stdout.log', 'a')
        sys.stderr = open('stderr.log', 'a')

        # Configurações do Selenium
        chrome_options = Options()
        chrome_options.add_argument("--incognito")

        # Inicializa a aplicação MSAL
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret,
        )

        # Inicia o fluxo de código de autorização
        flow = app.initiate_auth_code_flow(scopes=self.scope, redirect_uri=self.redirect_uri)
        auth_url = flow["auth_uri"]
        self.response = f"Autenticando, por favor, visite a URL: {auth_url}"
        self.logger.info(self.response)

        # Inicializa o ChromeDriver com redirecionamento de saída
        service = Service(ChromeDriverManager().install())
        service.start()
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(auth_url)

        class AuthHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                self.server.logger.info("%s - - [%s] %s\n" %
                                        (self.client_address[0],
                                         self.log_date_time_string(),
                                         format % args))

            def do_GET(self):
                parsed_path = urlparse.urlparse(self.path)
                query_params = urlparse.parse_qs(parsed_path.query)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Captura o código de autorização e o estado
                if 'code' in query_params and 'state' in query_params:
                    self.server.auth_code = query_params['code'][0]
                    self.server.state = query_params['state'][0]
                    self.wfile.write(b'''
                                    <!DOCTYPE html>
                                    <html lang="pt_BR">
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <style>
                                                body {
                                                    font-family: 'Arial', sans-serif;
                                                    background-color: #f8f9fa;
                                                    margin: 0;
                                                    font-size: 16px;
                                                    padding: 30px;
                                                    display: flex; *
                                                }

                                                .container {        
                                                    width: 100%;
                                                    margin: auto;
                                                    background-color: #ffffff;
                                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                                    padding: 16px;
                                                    text-align: center;
                                                    font-size: 12px;
                                                    border-radius: 8px;
                                                }

                                                h1 {    
                                                    font-size: 18px;
                                                    text-align: center;
                                                    color: #007bff;
                                                }
                                        </style>
                                     </head>
                                        <div class="container">
                                            <h1>Autentica&#231;&#227;o realizada com sucesso!</h1>
                                            Esta p&#225;gina ser&#225; fechada automaticamente.<br>
                                            Se isto n&#227;o acontecer, pode fech&#225;-la manualmente.
                                        </div>
                                     </body></html>
                                     ''')
                else:
                    self.wfile.write(b'''
                                    <!DOCTYPE html>
                                    <html lang="pt_BR">
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <style>
                                                body {
                                                    font-family: 'Arial', sans-serif;
                                                    background-color: #f8f9fa;
                                                    margin: 0;
                                                    font-size: 16px;
                                                    padding: 30px;
                                                    display: flex; *
                                                }

                                                .container {        
                                                    width: 100%;
                                                    margin: auto;
                                                    background-color: #ffffff;
                                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                                    padding: 16px;
                                                    text-align: center;
                                                    font-size: 12px;
                                                    border-radius: 8px;
                                                }

                                                h1 {    
                                                    font-size: 18px;
                                                    text-align: center;
                                                    color: red;
                                                }
                                        </style>
                                     </head>
                                        <div class="container">
                                            <h1>Falha na autentica&#231;&#227;o!</h1>
                                            Esta p&#225;gina ser&#225; fechada automaticamente.<br>
                                            Se isto n&#227;o acontecer, pode fech&#225;-la manualmente.
                                        </div>
                                     </body></html>
                                     ''')

        # Inicializa o servidor HTTP
        self.server = HTTPServer(('localhost', 8000), AuthHandler)
        self.server.logger = self.logger  # Passa o logger para o servidor

        # Função para monitorar o tempo limite
        def monitor_timeout():
            time.sleep(self.timeout)
            if not hasattr(self.server, 'auth_code'):
                self.response = "tempo limite para autenticação foi excedido"
                self.status_code = 490
                self.logger.error(self.response)
                driver.quit()
                self.server.server_close()

        # Inicia a thread para monitorar o tempo limite
        timeout_thread = threading.Thread(target=monitor_timeout)
        timeout_thread.start()

        # Espera pelo código de autorização
        self.response = "Esperando pela autenticação..."
        self.logger.info(self.response)
        self.server.handle_request()

        # Restaura stdout e stderr
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        # Verifica se o código de autorização foi obtido dentro do tempo limite
        if not hasattr(self.server, 'auth_code'):
            return

        # Obtém o código de autorização e o estado capturados pelo servidor HTTP
        auth_code = self.server.auth_code
        state = self.server.state

        # Adquire o token usando o código de autorização, verificando o estado
        try:
            result = app.acquire_token_by_auth_code_flow(flow, {"code": auth_code, "state": state})
        except ValueError as e:
            self.response = f"Erro ao obter o token de acesso: {e}"
            self.status_code = 401
            self.logger.error(self.response)
            driver.quit()
            return

        if "access_token" in result:
            access_token = result['access_token']
            headers = {
                'Authorization': 'Bearer ' + access_token
            }

            # Obtém o email do usuário autenticado
            me_response = requests.get(
                'https://graph.microsoft.com/v1.0/me',
                headers=headers
            )
            self.status_code = me_response.status_code
            if me_response.status_code == 200:
                me_data = me_response.json()
                user_email = me_data['userPrincipalName']
                self.response = f"Email do usuário autenticado: {user_email}"
                self.logger.info(self.response)

                # Verifica se o usuário pertence ao grupo
                group_name = grupo

                # Obtém o ID do usuário
                user_response = requests.get(
                    f'https://graph.microsoft.com/v1.0/users/{user_email}',
                    headers=headers
                )
                self.status_code = user_response.status_code
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    user_id = user_data['id']

                    # Pesquisa o grupo pelo nome
                    group_response = requests.get(
                        f"https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '{group_name}'",
                        headers=headers
                    )
                    self.status_code = group_response.status_code
                    if group_response.status_code == 200:
                        group_data = group_response.json()
                        if 'value' in group_data and len(group_data['value']) > 0:
                            group_id = group_data['value'][0]['id']

                            # Verifica se o usuário está no grupo
                            members_response = requests.get(
                                f'https://graph.microsoft.com/v1.0/groups/{group_id}/members',
                                headers=headers
                            )
                            self.status_code = members_response.status_code
                            if members_response.status_code == 200:
                                members_data = members_response.json()
                                if 'value' in members_data:
                                    user_in_group = any(member['id'] == user_id for member in members_data['value'])
                                    if user_in_group:
                                        self.response = f"O usuário {user_email} pertence ao grupo {group_name}."
                                    else:
                                        self.response = f"O usuário {user_email} NÃO pertence ao grupo {group_name}."
                                        self.status_code = 299
                                else:
                                    self.response = "Resposta da API de membros não contém a chave 'value'."
                                    self.status_code = 460
                            else:
                                self.response = f"Erro na resposta da API de membros: {members_response.status_code}"
                                self.response += f"\n{members_response.json()}"
                        else:
                            self.response = f"Grupo '{group_name}' não encontrado."
                            self.status_code = 470
                    else:
                        self.response = f"Erro na resposta da API de grupos: {group_response.status_code}"
                        self.response += f"\n{group_response.json()}"
                else:
                    self.response = f"Erro na resposta da API de usuário: {user_response.status_code}"
                    self.response += f"\n{user_response.json()}"
            else:
                self.response = f"Erro ao obter informações do usuário: {me_response.status_code}"
                self.response += f"\n{me_response.json()}"
        else:
            self.response = f"Erro ao obter o token de acesso: {result.get('error')}"
            self.response += f"\n{result.get('error_description')}"
            self.status_code = 480

        # Fecha o navegador
        driver.quit()
        service.stop()