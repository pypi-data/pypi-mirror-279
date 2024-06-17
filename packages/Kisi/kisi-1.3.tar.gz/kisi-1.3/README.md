# Kisi

KISI: The go-to access control app.

This Python library provides convenient access to the Kisi API, allowing you to manage groups, calendars, and cameras programmatically.
Kisi is an easy to use cloud based software to manage access to your doors. For physical access use your smartphone's mobile App or secure badges to unlock and open door.


[Kisi Shop](https://www.getkisi.com/pricing)<br>
[About Kisi](https://www.getkisi.com/about)

Request Feature/Suggestion: https://forms.gle/efGD5DuTpWsX96GG7

[![Downloads](https://static.pepy.tech/badge/kisi)](https://pepy.tech/project/kisi)
## Installation
```console
pip install kisi
```
Kisi supports Python 3+.

## Usage
#### Default
```python
import kisi
```

#### Authentication

Before making requests, you need to authenticate using your Kisi API key. Initialize the `Connect` class with your API key:

```python
from kisi import Connect

api_key = 'your_kisi_api_key'
ks = Connect(api_key)
```
OR
```python
import kisi 

api_key = 'your_kisi_api_key'
ks = kisi.Connect(api_key)
```
Generate Key from [Kisi API](https://web.kisi.io/user/api)

### Users
#### Fetch Users
```python
# Fetch users with optional parameters
users = ks.fetch_users(confirmed=True, group_id=1, limit=20, offset=0)
print(users)
```

#### Create User
```python
# Create a new user
new_user = ks.create_user(name='John Doe', email='john@example.com', password='securepassword')
print(new_user)
```
#### Fetch User
```python
# Fetch a specific user by user_id
user = ks.fetch_user(user_id=123)
print(user)
```
#### Update User
```python
# Update user details
updated_user = ks.update_user(user_id=123, name='John Doe Jr.')
print(updated_user)
```
#### Delete User
```python
# Delete a user by user_id
ks.delete_user(user_id=123)
```

#### Fetch Current User
```python
# Fetch details of the current authenticated user
current_user = ks.fetch_current_user()
print(current_user)
```

#### Update Current User
```python
# Update details of the current authenticated user
updated_current_user = ks.update_current_user(name='Jane Doe')
print(updated_current_user)
```

#### Delete Current User
```python
# Delete the current authenticated user
ks.delete_current_user()
```

#### Register User
```python
# Register a new user
register_user = ks.register_user(name='Jane Doe', email='jane@example.com', password='securepassword', terms_and_conditions=True)
print(register_user)
```
### Groups

#### Fetch Groups
```python
# Fetch groups with optional parameters
groups = ks.fetch_groups(limit=10, offset=0)
print(groups)
```

#### Create Group
```python
# Create a new group
new_group = ks.create_group(name='Engineering Team')
print(new_group)
```

#### Fetch Group
```python
# Fetch a specific group by group_id
group = ks.fetch_group(group_id=1)
print(group)
```

#### Update Group
```python
# Update group details
updated_group = ks.update_group(group_id=1, name='DevOps Team')
print(updated_group)
```

#### Delete Group
```python
# Delete a group by group_id
ks.delete_group(group_id=1)
```


### Cards

Fetch Cards
```python
# Fetch cards with optional parameters
cards = ks.fetch_cards(limit=10, offset=0)
print(cards)
```
#### Create Card
```python
# Create a new card
new_card = ks.create_card(token='token_value', card_type='rfid')
print(new_card)
```
#### Fetch Card
```python
# Fetch a specific card by card_id
card = ks.fetch_card(cardIdentifier='card_id_value')
print(card)
```
#### Update Card
```python
# Update card details
updated_card = ks.update_card(card_id='card_id_value', two_factor_pin='1234')
print(updated_card)
```
#### Delete Card
```python
# Delete a card by card_id
ks.delete_card(card_id='card_id_value')
```
### Locks

#### Fetch Locks
```python
# Fetch locks with optional parameters
locks = ks.fetch_locks(limit=10, offset=0)
print(locks)
```
#### Create Lock
```python
# Create a new lock
new_lock = ks.create_lock(name='Main Entrance', place_id=1)
print(new_lock)
```
#### Fetch Lock
```python
# Fetch a specific lock by lock_id
lock = ks.fetch_lock(lock_id=1)
print(lock)
```
#### Update Lock
```python
# Update lock details
updated_lock = ks.update_lock(lock_id=1, name='Back Door')
print(updated_lock)
```
#### Delete Lock
```python
# Delete a lock by lock_id
ks.delete_lock(lock_id=1)
```
### Cameras

#### Fetch Cameras
```python
# Fetch cameras with optional parameters
cameras = ks.fetch_cameras(limit=10, place_id=1)
print(cameras)
```
#### Create Camera
```python
# Create a new camera
new_camera = ks.create_camera(lock_id=1, remote_id='camera_001', name='Main Lobby Camera')
print(new_camera)
```
#### Fetch Camera
```python
# Fetch a specific camera by camera_id
camera = ks.fetch_camera(camera_id=1)
print(camera)
```
#### Update Camera
```python
# Update camera details
updated_camera = ks.update_camera(camera_id=1, name='Main Lobby Camera New')
print(updated_camera)
```
#### Delete Camera
```python
# Delete a camera by camera_id
ks.delete_camera(camera_id=1)
```
### Calendars

#### Fetch Summary
```python
# Fetch calendar summary with required parameters
summary = ks.fetch_summary(around='2024-06-17', consequence='consequence_value')
print(summary)### Groups
```

#### Fetching Groups
```python
groups = ks.group.fetch_groups()
print(groups)
```

#### Creating a Group

```python
new_group = ks.group.create_group(name='Engineering Team', description='Access to engineering floors')
print(new_group)
```

#### Fetching a Group

```python
group_info = ks.group.fetch_group(group_id=123)
print(group_info)
```

#### Updating a Group

```python
update_result = ks.group.update_group(group_id=123, name='New Name', description='New Description')
print(update_result)
```

#### Deleting a Group

```python
delete_result = ks.group.delete_group(group_id=123)
print(delete_result)
```

### Calendars

#### Fetching Calendar Summary

```python
summary = ks.calendar.fetch_summary(around='2024-06-14', consequence='upcoming')
print(summary)
```

### Cameras

#### Fetching Cameras

```python
cameras = ks.camera.fetch_cameras()
print(cameras)
```

#### Creating a Camera

```python
new_camera = ks.camera.create_camera(lock_id=456, remote_id='abc123', name='Office Camera')
print(new_camera)
```

#### Fetching a Camera

```python
camera_info = ks.camera.fetch_camera(camera_id=789)
print(camera_info)
```

#### Updating a Camera

```python
update_status = ks.camera.update_camera(camera_id=789, name='Updated Camera')
print(update_status)
```

#### Deleting a Camera

```python
delete_status = ks.camera.delete_camera(camera_id=789)
print(delete_status)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
```

This `README.md` provides a structured guide to using your library, including installation instructions, usage examples for each API action (groups, calendars, cameras), and licensing information. Adjust the examples as needed to match the specifics of your API client implementation and usage scenarios.
