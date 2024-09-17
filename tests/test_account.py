"""
Test Cases TestAccountModel
"""
import json
from random import randrange
import pytest
from models import db, app
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  T E S T   C A S E S
######################################################################

def test_create_all_accounts():
    """ Test creating multiple Accounts """
    for data in ACCOUNT_DATA:
        account = Account(**data)
        account.create()
    assert len(Account.all()) == len(ACCOUNT_DATA)

def test_create_an_account():
    """ Test Account creation using known data """
    rand = randrange(0, len(ACCOUNT_DATA))
    data = ACCOUNT_DATA[rand]  # get a random account
    account = Account(**data)
    account.create()
    assert len(Account.all()) == 1

def test_repr():
    """Test the representation of an account"""
    account = Account()
    account.name = "Foo"
    assert str(account) == "<Account 'Foo'>"
    
def test_to_dict():
    """ Test account to dict """
    rand = randrange(0, len(ACCOUNT_DATA))  # Generate a random index
    data = ACCOUNT_DATA[rand]  # get a random account
    account = Account(**data)
    result = account.to_dict()

    assert account.name == result["name"]
    assert account.email == result["email"]
    assert account.phone_number == result["phone_number"]
    assert account.disabled == result["disabled"]
    assert account.date_joined == result["date_joined"]
    
def test_from_dict():
    """ Test Account creation from a dictionary """
    rand = randrange(0, len(ACCOUNT_DATA))  # Generate a random index
    data = ACCOUNT_DATA[rand]  # get a random account
    account = Account()
    account.from_dict(data)
    account.create()
    
    # Check that attributes were set correctly
    assert account.name == data.get("name")
    assert account.email == data.get("email")
    assert account.phone_number == data.get("phone_number")
    assert account.disabled == data.get("disabled")
    
    
def test_update():
    """ Test updating an account"""
    # Create an account manually 
    account_data = {
        "name": "John Test",
        "email": "john@test.com",
        "phone_number": "702-234-4456",
        "disabled": False
    }
    account = Account(**account_data)
    account.create()

    # Update the account
    account.name = "Update"
    account.update()

    # Verify the account was updated
    updated_account = Account.find(account.id)
    assert updated_account.name == "Update"
    
def test_delete():
    """ Test deleting an account"""
    # Create an account manually
    account_data = account_data = {
        "name": "John Test",
        "email": "john@test.com",
        "phone_number": "702-234-4456",
        "disabled": False
    }
    account = Account(**account_data)
    account.create()
    
    # Ensure account is created
    assert Account.find(account.id) is not None
    
    # Delete the account
    account.delete()
    
    # Verify the account was deleted
    assert Account.find(account.id) is None

    
       