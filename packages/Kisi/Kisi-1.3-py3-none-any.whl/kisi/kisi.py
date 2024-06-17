import requests


class UserAction:
    def __init__(self , api_key):
        self.api_key = api_key

    def fetch_users(self , confirmed=None , group_id=None , ids=None , limit=50 , offset=0 , place_id=None ,
                    query=None , sort=None , user_id=None):
        url = 'https://api.kisi.io/users'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        params = {
            "confirmed": confirmed ,
            "group_id": group_id ,
            "ids": ids ,
            "limit": limit ,
            "offset": offset ,
            "place_id": place_id ,
            "query": query ,
            "sort": sort ,
            "user_id": user_id
        }
        response = requests.get(url , headers=headers , params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error while fetching users: {response.text}')
            return None

    def create_user(self , name , email , image=None , send_emails=None , confirm=None , access_enabled=None ,
                    password_flow_enabled=None , metadata=None , notes=None):
        url = 'https://api.kisi.io/users'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        data = {
            "user": {
                "name": name ,
                "email": email ,
                "image": image ,
                "send_emails": send_emails ,
                "confirm": confirm ,
                "access_enabled": access_enabled ,
                "password_flow_enabled": password_flow_enabled ,
                "metadata": metadata ,
                "notes": notes
            }
        }
        response = requests.post(url , headers=headers , json=data)

        if response.status_code == 200:
            print('User created successfully.')
            return response.json()
        else:
            print(f'Error while creating user: {response.text}')

    def fetch_user(self , user_id):
        url = f'https://api.kisi.io/users/{user_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        response = requests.get(url , headers=headers)

        if response.status_code == 200:
            print('User fetched successfully.')
            return response.json()
        else:
            print(f'Error while fetching user: {response.text}')
            return None

    def update_user(self , user_id , name=None , image=None , access_enabled=None , password_flow_enabled=None ,
                    metadata=None , notes=None):
        url = f'https://api.kisi.io/users/{user_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        data = {
            "user": {
                "name": name ,
                "image": image ,
                "access_enabled": access_enabled ,
                "password_flow_enabled": password_flow_enabled ,
                "metadata": metadata ,
                "notes": notes
            }
        }
        data["user"] = {k: v for k , v in data["user"].items() if v is not None}

        response = requests.patch(url , headers=headers , json=data)

        if response.status_code == 200:
            print('User updated successfully.')
            return response.json()
        else:
            print(f'Error while updating user: {response.text}')
            return None

    def delete_user(self , user_id):
        url = f'https://api.kisi.io/users/{user_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        response = requests.delete(url , headers=headers)

        if response.status_code == 204:
            print('User deleted successfully.')
            return True
        else:
            print(f'Error while deleting user: {response.text}')
            return False

    def fetch_current_user(self):
        url = 'https://api.kisi.io/user'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        response = requests.get(url , headers=headers)

        if response.status_code == 200:
            print('Current user fetched successfully.')
            return response.json()
        elif response.status_code == 401:
            print('Unauthorized request. Please check your API key.')
            return None
        else:
            print(f'Error while fetching current user: {response.text}')
            return None

    def update_current_user(self , name=None , image=None , last_read_at=None , locale=None , current_password=None ,
                            password=None , password_confirmation=None):
        url = 'https://api.kisi.io/user'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        data = {
            "user": {
                "name": name ,
                "image": image ,
                "last_read_at": last_read_at ,
                "locale": locale ,
                "current_password": current_password ,
                "password": password ,
                "password_confirmation": password_confirmation
            }
        }
        # Remove keys with None values to avoid updating with null
        data["user"] = {k: v for k , v in data["user"].items() if v is not None}

        response = requests.patch(url , headers=headers , json=data)

        if response.status_code == 200:
            print('Current user updated successfully.')
            return response.json()
        else:
            print(f'Error while updating current user: {response.text}')
            return None

    def delete_current_user(self):
        url = 'https://api.kisi.io/user'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        response = requests.delete(url , headers=headers)

        if response.status_code == 200:
            print('Current user deleted successfully.')
            return True
        else:
            print(f'Error while deleting current user: {response.text}')
            return False

    def register_user(self , name ,email, password , terms_and_conditions , token=None , image=None):
        url = 'https://api.kisi.io/users/sign_up'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        data = {
            "user": {
                "name": name ,
                "email": email,
                "password": password ,
                "terms_and_conditions": terms_and_conditions ,
                "token": token ,
                "image": image
            }
        }
        # Remove keys with None values to avoid including them in the payload
        data["user"] = {k: v for k , v in data["user"].items() if v is not None}

        response = requests.post(url , headers=headers , json=data)

        if response.status_code == 200:
            print('User registered successfully.')
            return response.json()
        else:
            print(f'Error while registering user: {response.text}')
            return None


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

        if response.status_code == 200:
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
        data = {
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
        data["group"] = {k: v for k , v in data["group"].items() if v is not None}
        response = requests.patch(url , headers=headers , json=data)
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

class CardAction:
    def __init__(self , api_key):
        self.api_key = api_key

    def fetch_cards(self , card_id=None , card_number=None , facility_code=None , ids=None , limit=10 , offset=0 ,
                    sort=None , token=None , uid=None , user_id=None):
        url = 'https://api.kisi.io/cards'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        params = {
            "card_id": card_id ,
            "card_number": card_number ,
            "facility_code": facility_code ,
            "ids": ids ,
            "limit": limit ,
            "offset": offset ,
            "sort": sort ,
            "token": token ,
            "uid": uid ,
            "user_id": user_id
        }
        # Remove keys with None values to avoid sending them in the query parameters
        params = {k: v for k , v in params.items() if v is not None}

        response = requests.get(url , headers=headers , params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error while fetching cards: {response.text}')
            return None

    def create_card(self , token , card_type):
        url = 'https://api.kisi.io/cards'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        data = {
            "card": {
                "token": token ,
                "type": card_type
            }
        }

        response = requests.post(url , headers=headers , json=data)

        if response.status_code == 200:
            print('Card created successfully.')
            return response.json()
        else:
            print(f'Error while creating card: {response.text}')
            return None

    def fetch_card(self , cardIdentifier):
        url = f'https://api.kisi.io/cards/{cardIdentifier}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }

        response = requests.get(url , headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error while fetching card: {response.text}')
            return None

    def delete_card(self , card_id):
        url = f'https://api.kisi.io/cards/{card_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }

        response = requests.delete(url , headers=headers)

        if response.status_code == 204:
            print('Card deleted successfully.')
            return True
        else:
            print(f'Error while deleting card: {response.text}')
            return False

    def update_card(self , card_id , two_factor_pin=None , send_two_factor_pin_notification=None):
        url = f'https://api.kisi.io/cards/{card_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }

        data = {}
        if two_factor_pin is not None:
            data['two_factor_pin'] = two_factor_pin
        if send_two_factor_pin_notification is not None:
            data['send_two_factor_pin_notification'] = send_two_factor_pin_notification

        response = requests.patch(url , headers=headers , json={"card": data})

        if response.status_code == 204:
            print('Card updated successfully.')
            return True
        else:
            print(f'Error while updating card: {response.text}')
            return False


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


class CameraAction:
    def __init__(self , base_url , api_key):
        self.base_url = base_url
        self.api_key = api_key

    def fetch_cameras(self , floor_id=None , ids=None , place_id=None , sort='name'):
        url = f"{self.base_url}/cameras"
        headers = {
            "Content-Type": "application/json" ,
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "ids": ids ,
            "floor_id": floor_id ,
            "place_id": place_id ,
            "sort": sort
        }
        response = requests.patch(url , json=data , headers=headers)
        return response.json()

    def create_camera(self , lock_id , remote_id , name=None , clip_duration=None , description=None , enabled=True ,
                      number_of_snapshots=None , supports_thumbnails=True , place_id=None , snapshot_offset=None ,
                      supports_clips=True , supports_images=True):
        url = f"{self.base_url}/cameras"
        headers = {
            "Content-Type": "application/json" ,
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "camera": {
                "clip_duration": clip_duration ,
                "description": description ,
                "enabled": enabled ,
                "lock_id": lock_id ,
                "name": name ,
                "number_of_snapshots": number_of_snapshots ,
                "place_id": place_id ,
                "remote_id": remote_id ,
                "snapshot_offset": snapshot_offset ,
                "supports_clips": supports_clips ,
                "supports_images": supports_images ,
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

    def update_camera(self , camera_id , clip_duration=None , description=None , lock_id=None , name=None ,
                      number_of_snapshots=None ,
                      snapshot_offset=None , supports_clips=True , supports_images=True , supports_thumbnails=True ,
                      enabled=True):
        url = f"{self.base_url}/cameras/{camera_id}"
        headers = {
            "Content-Type": "application/json" ,
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "camera": {
                "clip_duration": clip_duration ,
                "description": description ,
                "enabled": enabled ,
                "lock_id": lock_id ,
                "name": name ,
                "number_of_snapshots": number_of_snapshots ,
                "snapshot_offset": snapshot_offset ,
                "supports_clips": supports_clips ,
                "supports_images": supports_images ,
                "supports_thumbnails": supports_thumbnails
            }
        }
        data["user"] = {k: v for k , v in data["user"].items() if v is not None}
        response = requests.patch(url , json=data , headers=headers)
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


class LockAction:
    def __init__(self , api_key):
        self.api_key = api_key

    def fetch_locks(self , configured=None , favorite=None , floor_id=None , ids=None ,
                    limit=50 , locked_down=None , offset=0 , online=None ,
                    place_id=None , query=None , sort=None):
        url = 'https://api.kisi.io/locks'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        params = {
            "configured": configured ,
            "favorite": favorite ,
            "floor_id": floor_id ,
            "ids": ids ,
            "limit": limit ,
            "locked_down": locked_down ,
            "offset": offset ,
            "online": online ,
            "place_id": place_id ,
            "query": query ,
            "sort": sort
        }
        response = requests.get(url , headers=headers , params=params)
        locks = response.json()

        if response.status_code == 200:
            return locks
        else:
            print(f'Error while fetching locks: {response.text}')

    def create_lock(self , name , place_id , description=None , latitude=None , longitude=None ,
                    geofence_restriction_enabled=None , reader_restriction_enabled=None ,
                    time_restriction_enabled=None , order_id=None , integration_id=None ,
                    floor_id=None , favorite=None):
        url = 'https://api.kisi.io/locks'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        data = {
            "lock": {
                "name": name ,
                "description": description ,
                "latitude": latitude ,
                "longitude": longitude ,
                "geofence_restriction_enabled": geofence_restriction_enabled ,
                "reader_restriction_enabled": reader_restriction_enabled ,
                "time_restriction_enabled": time_restriction_enabled ,
                "order_id": order_id ,
                "integration_id": integration_id ,
                "floor_id": floor_id ,
                "place_id": place_id ,
                "favorite": favorite
            }
        }
        response = requests.post(url , headers=headers , json=data)

        if response.status_code == 200:
            print('Lock created successfully.')
            return response.json()
        else:
            print(f'Error while creating lock: {response.text}')

    def fetch_lock(self , lock_id , favorite=None):
        url = f'https://api.kisi.io/locks/{lock_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        params = {
            "favorite": favorite
        }
        response = requests.get(url , headers=headers , params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Error while fetching lock: {response.text}')

    def update_lock(self , lock_id , name=None , description=None , latitude=None , longitude=None ,
                    geofence_restriction_enabled=None , reader_restriction_enabled=None ,
                    time_restriction_enabled=None , order_id=None , integration_id=None ,
                    floor_id=None , favorite=None):
        url = f'https://api.kisi.io/locks/{lock_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        data = {
            "lock": {
                "name": name ,
                "description": description ,
                "latitude": latitude ,
                "longitude": longitude ,
                "geofence_restriction_enabled": geofence_restriction_enabled ,
                "reader_restriction_enabled": reader_restriction_enabled ,
                "time_restriction_enabled": time_restriction_enabled ,
                "order_id": order_id ,
                "integration_id": integration_id ,
                "floor_id": floor_id ,
                "favorite": favorite
            }
        }
        data["lock"] = {k: v for k , v in data["lock"].items() if v is not None}
        response = requests.patch(url , headers=headers , json=data)

        if response.status_code == 200:
            print('Lock updated successfully.')
            return response.json()
        else:
            print(f'Error while updating lock: {response.text}')

    def delete_lock(self , lock_id):
        url = f'https://api.kisi.io/locks/{lock_id}'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}"
        }
        response = requests.delete(url , headers=headers)

        if response.status_code == 200:
            print('Lock deleted successfully.')
            return response.status_code
        else:
            print(f'Error while deleting lock: {response.text}')

    def unlock_lock(self , lock_id , latitude , longitude , proximity_proof=None):
        url = f'https://api.kisi.io/locks/{lock_id}/unlock'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        data = {
            "context": {
                "location": {
                    "latitude": latitude ,
                    "longitude": longitude
                }
            } ,
            "lock": {
                "proximity_proof": proximity_proof
            }
        }
        response = requests.post(url , headers=headers , json=data)

        if response.status_code == 200:
            print('Lock unlocked successfully.')
            return response.json()
        else:
            print(f'Error while unlocking lock: {response.text}')

    def lock_down_lock(self , lock_id):
        url = f'https://api.kisi.io/locks/{lock_id}/lock_down'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        response = requests.post(url , headers=headers)

        if response.status_code == 200:
            print('Lock locked down successfully.')
            return response.json()
        else:
            print(f'Error while locking down lock: {response.text}')

    def cancel_lockdown(self , lock_id):
        url = f'https://api.kisi.io/locks/{lock_id}/cancel_lockdown'
        headers = {
            "Accept": "application/json" ,
            "Authorization": f"KISI-LOGIN {self.api_key}" ,
            "Content-Type": "application/json"
        }
        response = requests.post(url , headers=headers)

        if response.status_code == 200:
            print('Lockdown cancelled successfully.')
            return response.json()
        else:
            print(f'Error while cancelling lockdown: {response.text}')


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
        self.camera = CameraAction(base_url , api_key)
        self.lock = LockAction(api_key)
        self.user = UserAction(api_key)
