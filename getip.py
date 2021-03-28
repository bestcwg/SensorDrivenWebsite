import socket
import platform
import re

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    
    match = re.match(r"cs-itwot-(\d+)\.uni\.au\.dk", platform.node())
    if match:
        IP = "127.0.0.1"
    return IP