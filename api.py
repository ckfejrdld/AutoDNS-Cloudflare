import requests
import json

def create_a_record(name, target, zone_id, email, api_key):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/"
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": f"{name}",
        "content": f"{target}",
        "comment": "Registered by AutoDNS feat. Project nPerm.",
        "ttl": 3600
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        pass
    else:
        print(response.text)
    return response.status_code

# def create_aaaa_record(name, target, zone_id, email, api_key):
#     url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/"
#     headers = {
#         "X-Auth-Email": email,
#         "X-Auth-Key": api_key,
#         "Content-Type": "application/json"
#     }
#     data = {
#         "type": "AAAA",
#         "name": f"{name}",
#         "content": f"{target}",
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(data))
    
#     if response.status_code == 200:
#         return "A 레코드 등록 성공."
#     else:
#         return "A 레코드 등록 실패"

def create_cname_record(name, target, zone_id, email, api_key):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/"
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "type": "CNAME",
        "name": f"{name}",
        "content": f"{target}",
        "comment": "Registered by AutoDNS feat. Project nPerm.",
        "ttl": 3600
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        pass
    else:
        print(response.text)
    return response.status_code

def create_srv_record(name, target, port, zone_id, email, api_key):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/"
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    data = {"type": "SRV",
        "data": {
            "priority": 100,
            "weight": 100,
            "port": f"{port}",
            "target": f"{target}"},
        "name": f"_minecraft._tcp.{name}",
        "comment": "Registered by AutoDNS feat. Project nPerm."
        }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        pass
    else:
        print(response.text)
    return response.status_code
    
def get_json(zone_id, email, api_key):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers, params={'page': 1, 'per_page': 200})
    if response.status_code == 200:
        return response.json(), 200
    else:
        return "JSON 수집 실패", 400
    
def remove_record(id, zone_id, email, api_key):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{id}"
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        return "삭제 완료", 200
    else:
        return "삭제 실패", 400
    
def get_id(name, zone_id, email, api_key, domain):
    print(get_json(zone_id, email, api_key))
    try:
        data, status_code = get_json(zone_id, email, api_key)
        if status_code == 200:
            if domain in name:
                for record in data['result']:
                    if 'name' in record and record['name'] == name:
                        return record['id'], 200
                    elif 'name' in record and record['name'] == f"_minecraft._tcp.{name}":
                        return record['id'], 200
            else:
                for record in data['result']:
                    if 'name' in record and record['name'] == f"{name}.{domain}":
                        return record['id'], 200
                    elif 'name' in record and record['name'] == f"_minecraft._tcp.{name}.{domain}":
                        return record['id'], 200
        return None, 400
    except:
        return None, 400

