import requests
site = ""
website = site if site != "" else input("website? ")
payload = {'inUserName': 'USERNAME/EMAIL', 'inUserPass': 'PASSWORD'}
r = requests.post(website, data=payload)
print(r.headers)
