import requests

def check_status():
    server = "http://localhost:3000"
    try:
        r = requests.get(f"{server}/api/Challenges")
        if r.status_code != 200:
            print("Failed to fetch challenges")
            return
            
        challenges = r.json().get("data", [])
        print(f"{'Challenge Key':<45} | Status")
        print("-" * 60)
        
        # Sort by key
        challenges.sort(key=lambda x: x['key'])
        
        for ch in challenges:
            if ch['solved']:
                print(f"{ch['key']:<45} | SOLVED")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_status()
