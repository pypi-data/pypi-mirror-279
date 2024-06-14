# Kisi

## Overview
KISI: The go-to access control app.

This Python library provides convenient access to the Kisi API, allowing you to manage groups, calendars, and cameras programmatically.
Kisi is an easy to use cloud based software to manage access to your doors. For physical access use your smartphone's mobile App or secure badges to unlock and open door.


[Kisi Shop](https://www.getkisi.com/pricing)

[About Kisi](https://www.getkisi.com/about)

Request Feature/Suggestion: https://forms.gle/efGD5DuTpWsX96GG7

[//]: # (## Download stats)

[//]: # ([![Downloads]&#40;https://static.pepy.tech/badge/ActiveCollab&#41;]&#40;https://pepy.tech/project/ActiveCollab&#41;)

## Installation
```console
pip install kisi
```
Kisi supports Python 3+.

## Usage

### Default
```python
import kisi
```


### Authentication

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

### Groups

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
