from dotenv import load_dotenv
from rosecape_utils.secrets.secrets import CloudProvider, AWSProvider, get_provider

load_dotenv()


def test_store_refresh_token_aws():
    awsprovider = get_provider("AWS")
    check = awsprovider.store_secret('test', 'test')
    assert check

def test_get_refresh_token_aws():
    awsprovider = get_provider("AWS")
    refresh_token = awsprovider.get_secret('test')
    assert refresh_token == 'test'



def test_store_refresh_token_azure():
    awsprovider = get_provider("AZURE")
    check = awsprovider.store_secret('test', 'test')
    assert check

def test_get_refresh_token_azure():
    awsprovider = get_provider("AZURE")
    refresh_token = awsprovider.get_secret('test')
    assert refresh_token == 'test'
