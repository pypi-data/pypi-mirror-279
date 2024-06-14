import requests
import sys

class Connect:
    def __init__(self , host_url , login_email , login_password):
        self.host_url = host_url.rsplit('/' , (host_url.count('/') - 2))[0]
        url = f'{host_url}/api/v1/issue-token'
        headers = {"Content-Type": "application/json"}
        data = {
            "username": login_email ,
            "password": login_password ,
            "client_name": "My ActiveCollab App" ,
            "client_vendor": "ACME Inc"
        }
        response = requests.post(url , headers=headers , json=data)

        if response.status_code == 200:
            self.token = response.json()['token']
            # print(self.token)

        if response.status_code != 200:
            print('Error while authenticating')
            sys.exit()

    def list_projects(self):
        """
        :return: list of all projects you have with their project number
        """
        url = f'{self.host_url}/api/v1/projects'
        headers = {"Content-Type": "application/json" ,
                   "X-Angie-AuthApiToken": self.token}

        response = requests.get(url , headers=headers)

        if response.status_code == 200:
            projects = []
            projects_data = response.json()

        if response.status_code != 200:
            print(f'Error while fetching projects {response.status_code}')
            sys.exit()

        for i in projects_data:
            project = {}
            project['id'] = i['id']
            project['name'] = i['name']
            project['members'] = i['members']
            projects.append(project)
        return projects
    def list_project_tasklist(self,project_id):
        """
        :return: list of all projects you have with their project number
        """
        url = f'{self.host_url}/api/v1/projects/{project_id}/task-lists'
        headers = {"Content-Type": "application/json" ,
                   "X-Angie-AuthApiToken": self.token}

        response = requests.get(url , headers=headers)

        if response.status_code == 200:
            projects_tasklist = []
            projects_data = response.json()

        if response.status_code != 200:
            print(f'Error while fetching project {response.status_code}')
            sys.exit()

        for i in projects_data:
            projects_tasklist_data = {}
            projects_tasklist_data['id'] = i['id']
            projects_tasklist_data['name'] = i['name']
            projects_tasklist.append(projects_tasklist_data)
            print(projects_tasklist)
        return projects_tasklist

    def list_users(self):
        """
        :return: list of all users
        """
        url = f'{self.host_url}/api/v1/users'
        headers = {"Content-Type": "application/json" ,
                   "X-Angie-AuthApiToken": self.token}

        response = requests.get(url , headers=headers)

        if response.status_code == 200:
            users = []
            users_data = response.json()
            print(users_data)

        if response.status_code != 200:
            print('Error while fetching users')
            sys.exit()

        for i in users_data:
            user = {}
            user['id'] = i['id']
            user['name'] = i['first_name']
            user['email'] = i['email']
            users.append(user)
        return users

    def project_detail(self , project_id):
        """
        :return: list of all projects you have with their project number
        """
        url = f'{self.host_url}/api/v1/projects/{project_id}'
        headers = {"Content-Type": "application/json" ,
                   "X-Angie-AuthApiToken": self.token}

        response = requests.get(url , headers=headers)

        if response.status_code == 200:
            project_detail = []
            project = {}
            project_detail_data = response.json()['single']
            project['id'] = project_detail_data['id']
            project['name'] = project_detail_data['name']
            project['members'] = project_detail_data['members']
            project_detail.append(project)

        if response.status_code != 200:
            print('Error while fetching project detail')
            sys.exit()

        return project_detail

    def add_note_in_project(self , project_id , note_title , note_content):
        """
        :param note_title: Title of your note
        :param note_content: content of the note
        :param project_id: Project id in which you want to add the user
        :return: Notes added with note URL
        """
        url = f'{self.host_url}/api/v1/projects/{project_id}/notes'
        headers = {"Content-Type": "application/json" ,
                   "X-Angie-AuthApiToken": self.token}
        data = {
            "name": note_title ,
            "body": note_content
        }

        response = requests.post(url , headers=headers , json=data)

        if response.status_code == 200:
            note_response = response.json()['single']
            return self.host_url + note_response['url_path']

        if response.status_code != 200:
            print('Error while creating note')
            sys.exit()

    def add_task_in_project(self , project_id , task_title , task_description , task_assignee):
        """
        :param task_assignee: id of assignee (can be obtained from list_users())
        :param task_description: task description
        :param task_title: task title
        :param project_id: Project id in which you want to add the user
        :return: Task added with task URL
        """
        url = f'{self.host_url}/api/v1/projects/{project_id}/tasks'
        headers = {
            "Content-Type": "application/json" ,
            "X-Angie-AuthApiToken": self.token
        }
        data = {
            "name": task_title,
            "assignee_id": task_assignee,
            "body": task_description
        }

        response = requests.post(url , headers=headers , json=data)

        if response.status_code == 200:
            task_response = response.json()['single']
            return self.host_url + task_response['url_path']

        if response.status_code != 200:
            print('Error while creating task')
            sys.exit()








