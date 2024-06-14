import requests


class GroupAction:
    def __init__(self , api_key):
        self.api_key = api_key

    def fetch_groups(self , ids=None , query=None , limit=10 , offset=0 , scope=None , place_id=None ,
                     elevator_stop_id=None , lock_id=None , sort=None):
        url = 'https://api.kisi.io/groups'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        params = {
            "ids": ids ,
            "query": query ,
            "limit": limit ,
            "offset": offset ,
            "scope": scope ,
            "place_id": place_id ,
            "elevator_stop_id": elevator_stop_id ,
            "lock_id": lock_id ,
            "sort": sort
        }
        response = requests.get(url , headers=headers , params=params)
        groups = response.json()

        if response.status_code == 200:
            return groups
        else:
            print('Error while fetching groups')

    def create_group(self , name , description=None , place_id=None , login_enabled=False ,
                     geofence_restriction_enabled=False , primary_device_restriction_enabled=False ,
                     managed_device_restriction_enabled=False , reader_restriction_enabled=False ,
                     time_restriction_enabled=False):
        url = 'https://api.kisi.io/groups'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        payload = {
            "group": {
                "name": name ,
                "description": description ,
                "place_id": place_id ,
                "login_enabled": login_enabled ,
                "geofence_restriction_enabled": geofence_restriction_enabled ,
                "primary_device_restriction_enabled": primary_device_restriction_enabled ,
                "managed_device_restriction_enabled": managed_device_restriction_enabled ,
                "reader_restriction_enabled": reader_restriction_enabled ,
                "time_restriction_enabled": time_restriction_enabled
            }
        }
        response = requests.post(url , headers=headers , json=payload)
        group = response.json()

        if response.status_code == 201:  # 201 Created
            return group
        else:
            print('Error while creating group')
            print(group)

    def fetch_group(self , group_id):
        url = f'https://api.kisi.io/groups/{group_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        response = requests.get(url , headers=headers)
        group = response.json()

        if response.status_code == 200:
            return group
        else:
            print('Error while fetching group')

    def update_group(self , group_id , name=None , description=None , login_enabled=None ,
                     geofence_restriction_enabled=None , primary_device_restriction_enabled=None ,
                     managed_device_restriction_enabled=None , reader_restriction_enabled=None ,
                     time_restriction_enabled=None):
        url = f'https://api.kisi.io/groups/{group_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        payload = {
            "group": {
                "name": name ,
                "description": description ,
                "login_enabled": login_enabled ,
                "geofence_restriction_enabled": geofence_restriction_enabled ,
                "primary_device_restriction_enabled": primary_device_restriction_enabled ,
                "managed_device_restriction_enabled": managed_device_restriction_enabled ,
                "reader_restriction_enabled": reader_restriction_enabled ,
                "time_restriction_enabled": time_restriction_enabled
            }
        }
        response = requests.patch(url , headers=headers , json=payload)
        if response.status_code == 204:
            return f'Group {group_id} updated successfully'
        else:
            print('Error while updating group')
            print(response.json())

    def delete_group(self , group_id):
        url = f'https://api.kisi.io/groups/{group_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        response = requests.delete(url , headers=headers)
        if response.status_code == 204:
            return f'Group {group_id} deleted successfully'
        else:
            print('Error while deleting group')

class CalendarAction:
    def __init__(self , api_key):
        self.api_key = api_key

    def fetch_summary(self , around , consequence , elevator_stop_id=None , group_id=None , lock_id=None):
        url = 'https://api.kisi.io/calendar/summary'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        params = {
            "around": around ,
            "consequence": consequence ,
            "elevator_stop_id": elevator_stop_id ,
            "group_id": group_id ,
            "lock_id": lock_id
        }
        response = requests.get(url , headers=headers , params=params)
        summary = response.json()

        if response.status_code == 200:
            return summary

        if response.status_code != 200:
            print('Error while fetching summary')
            print(summary)

class Camera:
    def __init__(self , base_url , api_key):
        self.base_url = base_url
        self.api_key = api_key

    def fetch_cameras(self,floor_id=None,ids=None,place_id=None,sort='name'):
        url = f"{self.base_url}/cameras"
        headers = {
            "Content-Type": "application/json" ,
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "ids": ids,
            "floor_id": floor_id,
            "place_id": place_id,
            "sort": sort
        }
        response = requests.patch(url , json=data , headers=headers)
        return response.json()


    def create_camera(self , lock_id , remote_id , name=None , clip_duration=None , description=None , enabled=True , number_of_snapshots=None , supports_thumbnails=True , place_id=None , snapshot_offset=None , supports_clips=True , supports_images=True):
        url = f"{self.base_url}/cameras"
        headers = { 
            "Content-Type": "application/json" ,
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "camera": {
                "clip_duration": clip_duration,
                "description": description,
                "enabled": enabled,
                "lock_id": lock_id,
                "name": name,
                "number_of_snapshots": number_of_snapshots,
                "place_id": place_id,
                "remote_id": remote_id,
                "snapshot_offset":snapshot_offset,
                "supports_clips": supports_clips,
                "supports_images": supports_images,
                "supports_thumbnails": supports_thumbnails
                }
        }
        response = requests.post(url , json=data , headers=headers)
        return response.json()

    def fetch_camera(self , camera_id):
        url = f"{self.base_url}/cameras/{camera_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url , headers=headers)
        return response.json()

    def update_camera(self , camera_id , clip_duration=None , description=None , lock_id=None , name=None , number_of_snapshots=None ,
                      snapshot_offset=None , supports_clips=True , supports_images=True , supports_thumbnails=True ,
                      enabled=True):
        url = f"{self.base_url}/cameras/{camera_id}"
        headers = {
            "Content-Type": "application/json" ,
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "camera": {
                "clip_duration": clip_duration ,
                "description": description,
                "enabled": enabled ,
                "lock_id": lock_id ,
                "name": name ,
                "number_of_snapshots": number_of_snapshots ,
                "snapshot_offset": snapshot_offset,
                "supports_clips": supports_clips ,
                "supports_images": supports_images ,
                "supports_thumbnails": supports_thumbnails
                }
        }
        response = requests.patch(url , json=payload , headers=headers)
        return response.status_code

    def delete_camera(self , camera_id):
        url = f"{self.base_url}/cameras/{camera_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.delete(url , headers=headers)
        return response.status_code

    def fetch_video_link(self , camera_id , timestamp=None):
        url = f"{self.base_url}/cameras/{camera_id}/video_link"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        params = {"timestamp": timestamp} if timestamp else {}
        response = requests.get(url , headers=headers , params=params)
        return response.json()


class Connect:
    def __init__(self , api_key):
        base_url = 'https://api.kisi.io'
        url = f'{base_url}/organizations'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {api_key}"
        }
        response = requests.get(url , headers=headers)
        data = response.json()

        if response.status_code == 200:
            pass

        if response.status_code != 200:
            print('Error while authenticating')
            print(data)

        self.group = GroupAction(api_key)
        self.calendar = CalendarAction(api_key)
        self.camera = Camera(base_url, api_key)
