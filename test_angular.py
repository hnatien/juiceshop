import requests

session = requests.Session()
BASE = 'http://localhost:3000'

# Get captcha
captcha_res = session.get(f'{BASE}/rest/captcha')
captcha_data = captcha_res.json()

# Submit feedback với ngy-cookie
payload = {
    "captchaId": captcha_data.get("captchaId"),
    "captcha": str(captcha_data.get("answer")),
    "comment": "Frontend uses ngy-cookie which is malicious!",
    "rating": 3
}
res = session.post(f'{BASE}/api/Feedbacks', json=payload)
print(f"Feedback: {res.status_code}")

# Trigger verify
session.get(f'{BASE}/rest/products/search?q=')

# Check
r = requests.get(f'{BASE}/api/Challenges')
for c in r.json()['data']:
    if c['key'] == 'typosquattingAngularChallenge':
        print(f"typosquattingAngularChallenge: solved={c['solved']}")
