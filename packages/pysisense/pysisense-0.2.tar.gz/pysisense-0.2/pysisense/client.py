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

    def get_users(self):
        user_url = self.base_url + '/api/v1/users'
        group_param = {'expand': 'groups', 'role': 'name'}
        response = requests.get(user_url, headers=self.headers, params=group_param)
        data = response.json()
        return data

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
            if not dic['groups']:
                GROUP_ID = ''
                GROUP_NAME = ''
            else:
                groups = dic['groups'][0]
                GROUP_ID = groups['_id']
                GROUP_NAME = groups['name']

            USER_ID = dic['_id']
            ROLE = 'viewer' if dic['role']['name'] == 'consumer' else 'sys.admin' if dic['role']['name'] == 'super' else dic['role']['name']
            IS_ACTIVE = dic['active']
            EMAIL = dic['email']
            USER_NAME = dic['userName']
            FIRST_NAME = dic['firstName']
            LAST_NAME = dic.get('lastName', '')

            users_data['USER_ID'].append(USER_ID)
            users_data['ROLE'].append(ROLE)
            users_data['IS_ACTIVE'].append(IS_ACTIVE)
            users_data['EMAIL'].append(EMAIL)
            users_data['USER_NAME'].append(USER_NAME)
            users_data['FIRST_NAME'].append(FIRST_NAME)
            users_data['LAST_NAME'].append(LAST_NAME)
            users_data['GROUP_ID'].append(GROUP_ID)
            users_data['GROUP_NAME'].append(GROUP_NAME)

        df = pd.DataFrame(users_data)
        return df

    def save_to_csv(self, df, file_path):
        df.to_csv(file_path, encoding='utf-8', index=False)

    def export_users_to_csv(self, file_path):
        data = self.get_users()
        df = self.process_users(data)
        self.save_to_csv(df, file_path)
        print(df.head(10))
