import base64
import requests
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def aes_encrypt(data, key, iv):
    """
    AES暗号化を行う関数
    :param data: 暗号化したいデータ (str)
    :param key: 暗号化キー (bytes, 16, 24, 32バイト)
    :return: 暗号化されたデータ (bytes) とIV (bytes)
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return encrypted_data

def aes_decrypt(encrypted_data, key, iv):
    """
    AES復号化を行う関数
    :param encrypted_data: 暗号化されたデータ (bytes)
    :param key: 暗号化キー (bytes, 16, 24, 32バイト)
    :param iv: 初期化ベクトル (bytes, 16バイト)
    :return: 復号化されたデータ (str)
    """
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')

def get_key_and_iv():
    identity_endpoint = "http://169.254.169.254/metadata/identity/oauth2/token"
    resource_uri="https://vault.azure.net/"
    token_auth_uri = f"{identity_endpoint}?resource={resource_uri}&api-version=2018-02-01"
    head_msi = {"Metadata": "true"}
    resp = requests.get(token_auth_uri, headers=head_msi)
    access_token = resp.json()["access_token"]
    
    KeyURL = "https://python-test-key.vault.azure.net/secrets/python-aes-test-key?api-version=2016-10-01"
    key_data = requests.get(url = KeyURL, headers = {"Authorization": "Bearer " + access_token})
    IvURL = "https://python-test-key.vault.azure.net/secrets/python-aes-test-iv?api-version=2016-10-01"
    iv_data = requests.get(url = IvURL, headers = {"Authorization": "Bearer " + access_token})
    
    return key_data.json()["value"], iv_data.json()["value"]

if __name__ == '__main__':
    encoded_key, encoded_iv = get_key_and_iv()
    key = base64.b64decode(encoded_key.encode('utf-8'))
    iv = base64.b64decode(encoded_iv.encode('utf-8'))
    
    plaintext = "ここに暗号化されたメッセージが入る"
    encrypted_data = aes_encrypt(plaintext, key, iv)
    
    print(aes_decrypt(encrypted_data, key, iv))
    