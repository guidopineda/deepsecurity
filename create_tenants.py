from __future__ import print_function
import sys
import warnings
import deepsecurity
import csv
import random
import string
from deepsecurity.rest import ApiException
from pprint import pprint


def gen_password():
    # This function generates a random password with a length of 20 characters
    lower = random.sample(string.ascii_lowercase, 6)  # It makes sure that the password contains 6 lower cases
    upper = random.sample(string.ascii_uppercase, 6)  # It makes sure that the password contains 6 upper cases
    num = random.sample(string.digits, 4)  # It makes sure that the password contains 4 digits
    symbols = random.sample(string.punctuation, 4)  # It makes sure that the password contains 4 symbols
    tmp_password = lower + upper + num + symbols
    random.shuffle(tmp_password)
    password = "".join(tmp_password)
    return password


def read_onboard_tenants_file(csv_file):
    # This function reads a CSV file which contains all the necessary information to create a Tenant
    v = open(csv_file)
    r = csv.reader(v)
    row0 = next(r)
    row0.append('Password')  # Adds a new column called "Password"
    new_row0 = ",".join(row0) + '\n'

    # Creates a file called "tenants_info.csv"
    with open('tenants_info.csv', 'w') as file_object:
        file_object.write(new_row0)

    # Appends in the new column a randomly generated password
    for item in r:
        item.append(gen_password())
        new_line = ",".join(item) + '\n'
        with open('tenants_info.csv', 'a') as file_object:
            file_object.write(new_line)


def read_csv(csv_file_to_open):
    # This function reads the new CSV file (tenants_info.csv), which contains the password for each Tenant
    with open(csv_file_to_open, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        csv_lines = []
        for row in csv_reader:
            csv_lines.append(row)

    return csv_lines


def create_tenant(api_host, api_key, admin_data, tenant_data):

    # Setup
    if not sys.warnoptions:
        warnings.simplefilter("ignore")

    configuration = deepsecurity.Configuration()
    configuration.host = api_host

    # Authentication
    configuration.api_key['api-secret-key'] = api_key

    # Initialization
    # Set Any Required Values
    api_instance = deepsecurity.TenantsApi(deepsecurity.ApiClient(configuration))
    api_version = 'v1'
    bypass_tenant_cache = False
    confirmation_required = False
    asynchronous = True

    # Define the administrator account
    admin = deepsecurity.Administrator()
    admin.username = admin_data[0]
    admin.password = admin_data[1]
    admin.email_address = admin_data[2]
    admin.receive_notifications = admin_data[3]
    admin.role_id = admin_data[4]

    # Create a tenant
    tenant = deepsecurity.Tenant(administrator=admin)

    # Set the visible modules
    modules = deepsecurity.Tenant.modules_visible = ["all"]
    tenant.modules_visible = modules

    # Set the account name
    tenant.name = tenant_data[0]

    # Set the locale and description
    tenant.locale = tenant_data[1]
    tenant.description = tenant_data[2]

    try:
        api_response = api_instance.create_tenant(tenant,
                                                  api_version,
                                                  bypass_tenant_cache=False,
                                                  confirmation_required=False,
                                                  asynchronous=True)
        pprint(api_response)

    except ApiException as e:
        print("An exception occurred when calling TenantsApi.create_tenant: %s\n" % e)


def main():

    # Read the Onboard Tenants file and create a password for each Tenant
    read_onboard_tenants_file('onboard_tenants.csv')

    # Host configuration
    api_host = '{API-HOST}'
    api_key = '{API-KEY}'

    # CSV file which contains the Tenant's configuration details
    csv_file = 'tenants_info.csv'

    print('The following Tenants will be created: \n')

    for lines in read_csv(csv_file):
        # For each line in the CSV file, it creates a Tenant in the DSM
        print('- ', lines.get('Tenant Name'))

        # Admin configuration
        admin_username = lines.get('Admin Username')
        admin_password = lines.get('Password')
        admin_email_address = lines.get('Email')
        admin_receive_notifications = 'false'
        admin_role_id = 1
        admin_data = [admin_username, admin_password, admin_email_address, admin_receive_notifications, admin_role_id]

        # Tenant configuration
        tenant_name = lines.get('Tenant Name')
        tenant_locale = 'en-US'
        tenant_description = lines.get('Tenant Description')
        tenant_data = [tenant_name, tenant_locale, tenant_description]

        # Call to create_tenant function
        create_tenant(api_host, api_key, admin_data, tenant_data)


if __name__ == '__main__':
    main()
