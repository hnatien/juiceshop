import requests
import json

r = requests.get('http://localhost:3000/api/Challenges').json()
unsolved = [c['key'] for c in r['data'] if not c['solved']]
print(json.dumps(unsolved, indent=2))
