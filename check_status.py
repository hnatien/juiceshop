import requests

challenges_to_check = [
    'typosquattingNpmChallenge',      
    'typosquattingAngularChallenge',  
    'killChatbotChallenge',           
    'dlpPasswordSprayingChallenge',   
    'retrieveBlueprintChallenge',     
    'supplyChainAttackChallenge',     
    'twoFactorAuthUnsafeSecretStorageChallenge',
    'jwtUnsignedChallenge',           
    'dataExportChallenge',            
    'dlpPastebinDataLeakChallenge',   
    'hiddenImageChallenge',           
    'knownVulnerableComponentChallenge'
]

r = requests.get('http://localhost:3000/api/Challenges')
data = r.json().get('data', [])

print("Challenge Status:")
print("=" * 60)
for key in challenges_to_check:
    for c in data:
        if c['key'] == key:
            status = "SOLVED" if c['solved'] else "NOT SOLVED"
            print(f"{key}: {status}")
            break
