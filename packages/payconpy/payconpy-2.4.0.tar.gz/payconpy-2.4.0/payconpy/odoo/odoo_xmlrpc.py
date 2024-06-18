import ssl
from payconpy.fpython.fpython import *
from xmlrpc import client
from src.base.base import *
import xmlrpc.client as client

def insert_odoo(model:str, data:dict|list, auth:dict, uid:int = None) -> int:
    """
    ## Inserts data into an Odoo model and returns the ID of the created record.


    Args:
        model (str): The name of the Odoo model to insert data into.
        data (dict | list): The data to insert into the Odoo model.
        auth (dict): Dict with auth for Odoo.
        uid (int, optional): UID from a retrieved auth. Defaults to None.
        

    Returns:
        int: Returns the ID of the created record

    Example for use:
    ```
    model = 'res.partner'
    data = {
        'name': 'John Doe',
        'phone': '555-555-5555'
        }
    auth = {
        'URL_RPC': 'https://your.odoo.com',
        'DB_RPC': 'your_db',
        'USERNAME_RPC': 'your_username',
        'PASSWORD_RPC': 'your_password'
        }
    insert_odoo(model, data, auth)
    12
    ```
    """
    URL_RPC = auth['URL_RPC']
    DB_RPC = auth['DB_RPC']
    USERNAME_RPC = auth['USERNAME_RPC']
    PASSWORD_RPC = auth['PASSWORD_RPC']
    context = ssl._create_unverified_context()

    common = client.ServerProxy(f'{URL_RPC}xmlrpc/2/common', context=context)
    if uid is None:
        uid = common.authenticate(DB_RPC, USERNAME_RPC, PASSWORD_RPC, {})
    models = client.ServerProxy('{}/xmlrpc/2/object'.format(URL_RPC), context=context)
    record_id = models.execute_kw(DB_RPC, uid, PASSWORD_RPC, model, 'create', [data])

    return record_id

def insert_odoo_if_not_exists(model:str, data:dict, domain:tuple, auth:dict, uid:int = None) -> int:
    """
    This function inserts a record into an Odoo model if a record with the specified domain does not already exist. 
    If a record exists, it returns the ID of the existing record.

    Args:
        model (str): The name of the Odoo model where the record will be inserted.
        data (dict): A dictionary containing the data for the new record to be inserted.
        domain (tuple): A tuple specifying the domain to check for existing records.
        auth (dict): A dictionary containing authentication information including URL, database name, username, and password
        uid (int): UID from a retrieved auth

    Returns:
        int: The ID of the newly inserted record if it didn't already exist. If a record with the specified domain exists,
            it returns the ID of the existing record.

    Example:
    ```
    model = "res.partner"
    data = {"name": "John Doe", "email": "johndoe@example.com"}
    domain = [("name", "=", "John Doe")]
    auth = {
        "URL_RPC": "http://example.com/",
        "DB_RPC": "mydb",
        "USERNAME_RPC": "admin",
        "PASSWORD_RPC": "admin_password"
    }
    print(insert_odoo_if_not_exists(model, data, domain, auth))
    7
    ```
    """
    URL_RPC = auth['URL_RPC']
    DB_RPC = auth['DB_RPC']
    USERNAME_RPC = auth['USERNAME_RPC']
    PASSWORD_RPC = auth['PASSWORD_RPC']
    context = ssl._create_unverified_context()

    common = client.ServerProxy(f'{URL_RPC}xmlrpc/2/common', context=context)
    if uid is None:
        uid = common.authenticate(DB_RPC, USERNAME_RPC, PASSWORD_RPC, {})
    models = client.ServerProxy(f'{URL_RPC}xmlrpc/2/object', context=context)

    if len(domain) >= 1:
        partner_ids = models.execute_kw(DB_RPC, uid, PASSWORD_RPC, model, 'search', [domain])
    else:
        partner_ids = models.execute_kw(DB_RPC, uid, PASSWORD_RPC, model, 'search', [])

    # Verify if the register already exists
    if not partner_ids:
        new_data_id = models.execute_kw(DB_RPC, uid, PASSWORD_RPC, model, 'create', [data])
        faz_log(f'New register created with id: {new_data_id} on model: {model}')
        return new_data_id
    else:
        faz_log(f'Resister already exists on model: {model} with id(s): {partner_ids}')
        return partner_ids[-1]

def update_record_odoo(model: str, data: dict, record_id: int, auth: dict, uid: int = None) -> int:
    """
    This function updates a record in an Odoo model if a record with the specified ID exists.

    Parameters:
    model (str): The name of the Odoo model where the record will be updated.
    data (dict): A dictionary containing the data to update the existing record.
    record_id (int): The ID of the existing record to be updated.
    auth (dict): A dictionary containing authentication information including URL, database name, username, and password
                for connecting to the Odoo instance.
    uid (int): UID from a retrieved auth

    Returns:
    int: The ID of the updated record.

    Example:
    ```
    model = "res.partner"
    data = {"name": "John Doe (Updated)"}
    record_id = 7  # ID of the existing record to update
    auth = {
        "URL_RPC": "http://example.com/",
        "DB_RPC": "mydb",
        "USERNAME_RPC": "admin",
        "PASSWORD_RPC": "admin_password"
    }
    print(update_odoo_record_if_exists(model, data, record_id, auth))
    7
    ```
    """
    URL_RPC = auth['URL_RPC']
    DB_RPC = auth['DB_RPC']
    USERNAME_RPC = auth['USERNAME_RPC']
    PASSWORD_RPC = auth['PASSWORD_RPC']
    context = ssl._create_unverified_context()

    common = client.ServerProxy(f'{URL_RPC}xmlrpc/2/common', context=context)
    if uid is None:
        uid = common.authenticate(DB_RPC, USERNAME_RPC, PASSWORD_RPC, {})
    models = client.ServerProxy(f'{URL_RPC}xmlrpc/2/object', context=context)

    # Verify if the record with the specified ID exists
    if models.execute_kw(DB_RPC, uid, PASSWORD_RPC, model, 'search', [[('id', '=', record_id)]]):
        models.execute_kw(DB_RPC, uid, PASSWORD_RPC, model, 'write', [[record_id], data])
        faz_log(f'Record updated with ID: {record_id} on model: {model}')
        return record_id
    else:
        faz_log(f'Record with ID {record_id} does not exist on model: {model}')
        return None

def get_odoo(model: str, data: dict, auth: dict, domains: list = [], uid: int = None, limit: int = None) -> list[dict]:
    """
    Retrieves data from an Odoo model using XML-RPC, applying domains.

    Args:
        model (str): The name of the Odoo model to retrieve data from.
        data (dict): A dictionary containing additional arguments to pass to the XML-RPC call.
        auth (dict): A dictionary containing authentication information including URL, database name, username, and password
        domains (list): A list of tuples representing the domains to apply. Each tuple should contain
                        the field name, the operator, and the value to domain by.
        uid (int): UID from a retrieved auth
        limit (int): Limit of records to retrieve.
    Returns:
        list[dict]: A list of dictionaries containing the retrieved data.

    Example:
    ```
    model = 'res.partner'
    data = {'fields': ['name', 'email']}  # or without values into list for get all fields
    domains = [('email', '=', 'example@domain.com')]
    auth = {
        "URL_RPC": "http://example.com/",
        "DB_RPC": "mydb",
        "USERNAME_RPC": "admin",
        "PASSWORD_RPC": "admin_password"
    }
    get_odoo(model, data, auth, domains, limit=10) 
    [{'name': 'John Doe', 'email': 'example@domain.com'}]
    
    ```
    """
    URL_RPC = auth['URL_RPC']
    DB_RPC = auth['DB_RPC']
    USERNAME_RPC = auth['USERNAME_RPC']
    PASSWORD_RPC = auth['PASSWORD_RPC']
    context = ssl._create_unverified_context()

    common = client.ServerProxy(f'{URL_RPC}xmlrpc/2/common', context=context)
    if uid is None:
        uid = common.authenticate(DB_RPC, USERNAME_RPC, PASSWORD_RPC, {})
    models = client.ServerProxy('{}/xmlrpc/2/object'.format(URL_RPC), context=context)

    # Apply filters to the search call
    domain = []
    for dom in domains:
        domain.append(dom)
    
    # If a limit is provided, use it in the data argument for search_read
    if limit is not None:
        if 'limit' in data:
            # Respect the lower of the two limits if 'limit' was already in 'data'
            data['limit'] = min(data['limit'], limit)
        else:
            data['limit'] = limit

    values = models.execute_kw(DB_RPC, uid, PASSWORD_RPC, model, 'search_read', [domain], data)
    return values


def insert_odoo_lots(model, data, auth, uid=None):
    """
    ### Alert! No verify if records exists
    Inserts a batch of records into a specified Odoo model using XML-RPC and returns the IDs of the newly created records. This function is 
    particularly useful for inserting multiple records in a single call, enhancing performance when dealing with large datasets.

    Args:
        model (str): The name of the Odoo model where the records will be inserted. 
                    For example, 'res.partner' for the Partner model.
        data (list): A list of dictionaries, where each dictionary represents the data for a record to be inserted into the model. 
                    Each key in the dictionary should correspond to a field name in the Odoo model.
        auth (dict): A dictionary containing authentication information for the Odoo instance. 
                    It should include the following keys: 'URL_RPC' (the base URL for the Odoo instance), 
                    'DB_RPC' (the database name), 'USERNAME_RPC' (the username), and 'PASSWORD_RPC' (the password).

    Returns:
        list: A list of integers representing the IDs of the newly created records in the Odoo model. If the insertion is successful, 
            this list will contain the IDs of all inserted records. If an error occurs during insertion, an XML-RPC fault may be raised.

    Example:
        ```
        model = 'res.partner'
        data = [
            {'name': 'John Doe', 'email': 'john@example.com'},
            {'name': 'Jane Doe', 'email': 'jane@example.com'}
        ]
        auth = {
            'URL_RPC': 'http://example.odoo.com',
            'DB_RPC': 'odoo_db',
            'USERNAME_RPC': 'admin',
            'PASSWORD_RPC': 'admin_password or api_key'
        }
        record_ids = insert_odoo_lots(model, data, auth)
        print(record_ids) # [1, 2]
        ```
    """
    URL_RPC = auth['URL_RPC']
    DB_RPC = auth['DB_RPC']
    USERNAME_RPC = auth['USERNAME_RPC']
    PASSWORD_RPC = auth['PASSWORD_RPC']
    context = ssl._create_unverified_context()

    common = client.ServerProxy(f'{URL_RPC}xmlrpc/2/common', context=context)
    if uid is None:
        uid = common.authenticate(DB_RPC, USERNAME_RPC, PASSWORD_RPC, {})
    models = client.ServerProxy('{}/xmlrpc/2/object'.format(URL_RPC), context=context)

    if not isinstance(data, list):
        data = [data]

    record_ids = models.execute_kw(DB_RPC, uid, PASSWORD_RPC, model, 'create', [data])
    return record_ids

def authenticate_odoo(auth: dict) -> int:
    """Return the UID of the authenticated user.

    Args:
        auth (dict): dictionary with the following keys: 'URL_RPC', 'DB_RPC', 'USERNAME_RPC', 'PASSWORD_RPC'

    Returns:
        int: UID of the authenticated user
    """
    URL_RPC = auth['URL_RPC']
    DB_RPC = auth['DB_RPC']
    USERNAME_RPC = auth['USERNAME_RPC']
    PASSWORD_RPC = auth['PASSWORD_RPC']
    context = ssl._create_unverified_context()
    
    common = client.ServerProxy(f'{URL_RPC}xmlrpc/2/common', context=context)
    uid = common.authenticate(DB_RPC, USERNAME_RPC, PASSWORD_RPC, {})
    return uid