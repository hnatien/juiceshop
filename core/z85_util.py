# ZeroMQ Z85 implementation

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#"

def encode(data: bytes) -> str:
    if len(data) % 4 != 0:
        raise ValueError("Data length must be multiple of 4")
    
    chars = []
    for i in range(0, len(data), 4):
        value = (data[i] << 24) + (data[i+1] << 16) + (data[i+2] << 8) + data[i+3]
        divisor = 85**4
        while divisor >= 1:
            char_idx = (value // divisor) % 85
            chars.append(ALPHABET[char_idx])
            divisor //= 85
    return "".join(chars)

def decode(data: str) -> bytes:
    if len(data) % 5 != 0:
        raise ValueError("Data length must be multiple of 5")
    
    res = bytearray()
    for i in range(0, len(data), 5):
        value = 0
        for j in range(5):
            char_idx = ALPHABET.index(data[i+j])
            value = value * 85 + char_idx
        
        res.append((value >> 24) & 0xFF)
        res.append((value >> 16) & 0xFF)
        res.append((value >> 8) & 0xFF)
        res.append(value & 0xFF)
    return bytes(res)
