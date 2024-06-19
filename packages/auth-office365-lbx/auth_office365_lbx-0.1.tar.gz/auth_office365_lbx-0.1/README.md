# auth_office365_lbx

Biblioteca para autenticação e verificação de grupos no Office 365.

## Instalação

pip install auth_office365_lbx

## Uso

from auth_office365_lbx.auth import auth_office365_lbx

client_id = 'SEU_CLIENT_ID'
client_secret = 'SEU_CLIENT_SECRET'
tenant_id = 'SEU_TENANT_ID'

auth = auth_office365_lbx(client_id, client_secret, tenant_id, timeout=60, log_file='auth_office365_lbx.log')  ## timeout e log_file são opcionais e se omitidos, os valores aqui atribuídos serão adotados como padrão
auth.valida_grupo('Nome do Grupo de Distribuição')

print(f"Response: {auth.response}")  
print(f"Status Code: {auth.status_code}") ## auth.status_code = 200, usuário pertence ao grupo informado. auth.status_code = 299, grupo existe mas usuário NÃO pertence à ele. Erros retornam 4xx.