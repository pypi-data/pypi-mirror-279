import os
import boto3
from abc import ABC, abstractmethod
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

def get_provider(provider_name):
    if provider_name == 'AWS':
        return AWSProvider()
    elif provider_name == 'AZURE':
        return AzureProvider()
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")

class CloudProvider(ABC):
    @abstractmethod
    def store_secret(self, parameter_name, secret_value):
        pass

    @abstractmethod
    def get_secret(self, parameter_name):
        pass

class AWSProvider(CloudProvider):
    def __init__(self):
        self.ssm_client = boto3.client('ssm')

    def store_secret(self, parameter_name, secret_value):
        response = self.ssm_client.put_parameter(
            Name=parameter_name,
            Value=secret_value,
            Type='SecureString',
            Overwrite=True
        )
        return response

    def get_secret(self, parameter_name):
        response = self.ssm_client.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )
        return response['Parameter']['Value']

class AzureProvider(CloudProvider):
    def __init__(self):
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')
        tenant_id = os.getenv('AZURE_TENANT_ID')
        key_vault_url = os.getenv('AZURE_KEY_VAULT_URL')
        self.credential = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
        self.secret_client = SecretClient(vault_url=key_vault_url, credential=self.credential)

    def store_secret(self, parameter_name, secret_value):
        response = self.secret_client.set_secret(parameter_name, secret_value)
        return response

    def get_secret(self, parameter_name):
        secret = self.secret_client.get_secret(parameter_name)
        return secret.value
