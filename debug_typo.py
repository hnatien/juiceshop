import requests
session = requests.Session()

# Submit feedback với epilogue-js
captcha_res = session.get('http://localhost:3000/rest/captcha')
captcha_data = captcha_res.json()

feedback_res = session.post('http://localhost:3000/api/Feedbacks', json={
    'captchaId': captcha_data.get('captchaId'),
    'captcha': str(captcha_data.get('answer')),
    'comment': 'typosquatting: epilogue-js is malicious!',
    'rating': 3
})
print(f'Feedback: {feedback_res.status_code}')

# Trigger verify by accessing products
print('Triggering verify...')
session.get('http://localhost:3000/rest/products/search?q=')

# Check status
status_res = session.get('http://localhost:3000/api/Challenges')
challenges = status_res.json().get('data', [])
for c in challenges:
    if c.get('key') == 'typosquattingNpmChallenge':
        print(f"typosquattingNpmChallenge: solved={c.get('solved')}")
        break
