import hvac
client = hvac.Client(url='http://127.0.0.1:8200')
print(client.token)
print(client.is_authenticated())
client.secrets.azure.configure(
    subscription_id='4ab848f3-d313-4a10-9af0-44872afda1e2',
    tenant_id='c124053c-f078-4984-8f9d-35ae0f78c58a',
)
azure_secret_config = client.secrets.azure.read_config()
print('The Azure secret engine is configured with a subscription ID of {id}'.format(
    id=azure_secret_config['subscription_id'],
))
azure_roles = [
    {
        'role_name': "Contributor",
        'scope': "/4ab848f3-d313-4a10-9af0-44872afda1e2/95e675fa-307a-455e-8cdf-0a66aeaa35ae"
    },
]
client.secrets.azure.create_or_update_role(
    name='my-azure-secret-role',
    azure_roles= azure_roles,
)
azure_secret_engine_roles = client.secrets.azure.list_roles()
print("The following Azure secret roles are configured: {roles}".format(
    roles=','.join(roles['keys']),
))