import hvac
import os
client = hvac.Client(url='http://127.0.0.1:8200')
print(client.token)
print(client.is_authenticated())
the_path = str(input("Enter secret path: "))

secrets_dicts = {}

tuple_list = []
client.secrets.kv.v2.configure(
    max_versions=20,
    mount_point='kv',
)
repeat = 1
while repeat != 0:
    keys = input("Enter the key for your secret: ")
    values = input("Enter the key value: ")
    pair = (keys, values)
    tuple_list.append(pair)
    print(tuple_list)
    repeat = int(input("Enter 0 to exit 1 to continue adding secrets: "))
secrets_dicts.update(tuple_list)
print(secrets_dicts)
create_response=client.secrets.kv.v2.create_or_update_secret(
    path=the_path,
    secret=dict(secrets_dicts)
)
create_response=client.secrets.kv.v2.create_or_update_secret(
    path='foo',
    secret=dict(email='jimmy@johns.com', password='bazinga', username='Admin', message='Hellow World')
)
client.secrets.kv.v2.patch(
    path='foo',
    secret=dict(pssst='patched secret'),
)
hvac_path_metadata = client.secrets.kv.v2.read_secret_metadata(
    path='foo',
)
print('Secret under path foo is on version {cur_ver}, with an oldest version of {old_ver}'.format(
    cur_ver=hvac_path_metadata['data']['oldest_version'],
    old_ver=hvac_path_metadata['data']['current_version'],
))

read_secrets = client.secrets.kv.read_secret_version(path='foo')
print(read_secrets)
print(".......\n", client.read('kv/hello'))
#client.secrets.kv.v2.delete_metadata_and_all_versions(
#    path='foo'
#)

client.secrets.kv.v2.create_or_update_secret(
    path='python/snake',
    secret=dict(Type='Snake', Long="Really long")
)

print(client.secrets.kv.v2.list_secrets(
    path='python',
))
