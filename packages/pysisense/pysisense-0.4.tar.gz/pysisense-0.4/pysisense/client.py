import requests
import yaml
import pandas as pd

class SisenseClient:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.token = self.config['source_token']
        self.base_url = self.config['source_url']
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def load_config(self, path):
        with open(path, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def get_users_data(self):
        try:
            user_url = f"{self.base_url}/api/v1/users"
            group_param = {'expand': 'groups,role'}
            response = requests.get(user_url, headers=self.headers, params=group_param)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            return self.process_users(data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            return None

    def process_users(self, data):
        users_data = {
            'USER_ID': [],
            'ROLE': [],
            'IS_ACTIVE': [],
            'EMAIL': [],
            'USER_NAME': [],
            'FIRST_NAME': [],
            'LAST_NAME': [],
            'GROUP_ID': [],
            'GROUP_NAME': []
        }

        for dic in data:
            user_id = dic.get('_id', '')
            role_name = dic.get('role', {}).get('name', '')
            is_active = dic.get('active', '')
            email = dic.get('email', '')
            user_name = dic.get('userName', '')
            first_name = dic.get('firstName', '')
            last_name = dic.get('lastName', '')

            if role_name == 'consumer':
                role = 'viewer'
            elif role_name == 'super':
                role = 'sys.admin'
            else:
                role = role_name

            group_id = ''
            group_name = ''

            groups = dic.get('groups', [])
            if groups:
                group_id = groups[0].get('_id', '')
                group_name = groups[0].get('name', '')

            users_data['USER_ID'].append(user_id)
            users_data['ROLE'].append(role)
            users_data['IS_ACTIVE'].append(is_active)
            users_data['EMAIL'].append(email)
            users_data['USER_NAME'].append(user_name)
            users_data['FIRST_NAME'].append(first_name)
            users_data['LAST_NAME'].append(last_name if 'lastName' in dic else '')
            users_data['GROUP_ID'].append(group_id)
            users_data['GROUP_NAME'].append(group_name)

        df = pd.DataFrame(users_data)
        return df

    def export_users_to_csv(self, file_path):
        users_data = self.get_users_data()
        if users_data is not None:
            users_data.to_csv(file_path, encoding='utf-8', index=False)
            print(f"Data exported to {file_path}")
        else:
            print("Failed to export data. Check previous error messages.")

    def print_users_data(self):
        users_data = self.get_users_data()
        if users_data is not None:
            print(users_data.head(10))
        else:
            print("Failed to fetch data. Check previous error messages.")


