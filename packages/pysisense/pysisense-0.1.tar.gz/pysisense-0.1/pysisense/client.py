import requests
import yaml
import pandas as pd

class SisenseClient:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.token = self.config['token']
        self.base_url = f"http://{self.config['ip']}:30845/"
        self.headers = {'Authorization': f'Bearer {self.token}'}

    def load_config(self, path):
        with open(path, 'r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def get_users(self):
        user_url = self.base_url + 'api/v1/users'
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
            users_data['USER_ID'].append(dic['_id'])
            role = dic['role']['name']
            users_data['ROLE'].append('viewer' if role == 'consumer' else 'sys.admin' if role == 'super' else role)
            users_data['IS_ACTIVE'].append(dic['active'])
            users_data['EMAIL'].append(dic['email'])
            users_data['USER_NAME'].append(dic['userName'])
            users_data['FIRST_NAME'].append(dic['firstName'])
            users_data['LAST_NAME'].append(dic.get('lastName', ''))
            groups = dic.get('groups', [])
            users_data['GROUP_ID'].append(groups[0]['_id'] if groups else '')
            users_data['GROUP_NAME'].append(groups[0]['name'] if groups else '')

        df = pd.DataFrame(users_data)
        return df

    def save_to_csv(self, df, file_path):
        df.to_csv(file_path, encoding='utf-8', index=False)

    def export_users_to_csv(self, file_path):
        data = self.get_users()
        df = self.process_users(data)
        self.save_to_csv(df, file_path)
        print(df.head(10))

