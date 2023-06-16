from storage.data import *

def gen_deviceid():
    while True:
     
        uuid_ = uuid.uuid4()
        ztotwoone = random.randint(0, 2147483647)
        ixzto = 3 * ztotwoone
        length = 0 if None is None else len(None.encode()) + 4
        allo = bytearray(length + 64)
     
        arr = bytearray(16)
        arr[0:8] = struct.pack('!Q', uuid_.int >> 64)
        arr[8:16] = struct.pack('!Q', uuid_.int & (2 ** 64 - 1))
      
        stru = struct.pack('!i', ztotwoone)
        bArr = bytearray(len(arr))
    
        for i5 in range(len(arr)):
          
            if len(arr) <= len(stru):
                bArr[i5] = stru[i5] ^ (arr[i5] & 255)
       
            else:
                bArr[i5] = stru[i5 % len(stru)] ^ (arr[i5] & 255)
     
        allo[0:8] = struct.pack('!Q', ixzto)
        allo[8:12] = [random.randint(0, 255) for _ in range(4)]
        allo[12:16] = stru
        allo[16:20] = [random.randint(0, 255) for _ in range(4)]
        allo[20:28] = [random.randint(0, 255) for _ in range(8)]
        allo[28:44] = bArr
        allo[44:52] = [random.randint(0, 255) for _ in range(8)]
        allo[52:56] = [random.randint(0, 255) for _ in range(4)]
        allo[56:58] = (None.encode() if None is not None else b'')
        allo[58:] = [random.randint(0, 255) for _ in range(12)]
      
        barr = base64.urlsafe_b64encode(allo).decode()
     
        if "-" in str(barr) or "_" in str(barr) or "==" not in str(barr):
            continue
        
        else:
            return str(barr)
