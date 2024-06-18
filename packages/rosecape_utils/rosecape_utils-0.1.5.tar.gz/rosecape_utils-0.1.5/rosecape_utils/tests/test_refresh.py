from dotenv import load_dotenv
from oauth.refresh_token import CloudProvider, AWSProvider

load_dotenv()



def test_create_efresh_token():
    awsprovider = AWSProvider()
    check = awsprovider.create_efresh_token('test', 'test')
    assert check

def test_get_refresh_token():
    awsprovider = AWSProvider()
    refresh_token = awsprovider.get_refresh_token('test')
    assert refresh_token == 'test'

def test_store_refresh_token():
    awsprovider = AWSProvider()
    check = awsprovider.store_refresh_token('test', 'test2')
    assert check

def test_get_refresh_token2():
    awsprovider = AWSProvider()
    refresh_token = awsprovider.get_refresh_token('test')
    assert refresh_token == 'test2'

def test_store_refresh_token2():
    awsprovider = AWSProvider()
    check = awsprovider.store_refresh_token('test', 'done')
    assert check