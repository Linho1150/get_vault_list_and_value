import json

import hvac

from secret import get_secret_key

secret_data = get_secret_key()
url=secret_data["url"]
token=secret_data["token"]
variable_mount_point=secret_data["variable_mount_point"]
connection_mount_point=secret_data["connection_mount_point"]

def connection_vault(url:str, token:str) -> hvac.Client:
    return hvac.Client(
        url=url,
        token=token,
    )

def get_all_keys_by_vault(client:hvac.Client,mount_point:str) -> list[str]:
    return client.secrets.kv.v2.list_secrets(
        mount_point=mount_point,
        path=''
    )["data"]["keys"]

def get_value_by_key_from_vault(client:hvac.Client,mount_point:str, key:str):
    return client.secrets.kv.v2.read_secret_version(
        mount_point=mount_point,
        path=key
        )["data"]["data"]

def get_all_data_by_path(key_list:list,mount_point:str)->dict:
    all_dict={}
    for key in key_list:
        all_dict[key] = get_value_by_key_from_vault(
            client=vault_client,
            mount_point=mount_point,
            key=key,
        )
    return all_dict

def json_by_list(data:list,filename:str):
    json_data = open(f"{filename}.json", "w",encoding='utf-8')
    json_data.write(json.dumps(data, indent=4, sort_keys=True,ensure_ascii=False))
    json_data.close()


if __name__ == "__main__":
    vault_client = connection_vault(url,token)
    connection_list = get_all_keys_by_vault(vault_client,connection_mount_point)
    variable_list = get_all_keys_by_vault(vault_client,variable_mount_point)
    all_variable_data = get_all_data_by_path(variable_list,variable_mount_point)
    all_connection_data = get_all_data_by_path(connection_list,connection_mount_point)

    json_by_list(data=all_connection_data,filename="connection_data")
    json_by_list(data=all_variable_data,filename="variable_data")
    print("Success")