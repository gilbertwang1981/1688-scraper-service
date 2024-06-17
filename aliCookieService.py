import json
import os


def updateCookie(userName, cookie):
    cookiePath = '/opt/apps/kp-aliWangWang-chat/'
    cookieFile = cookiePath + userName + '.cookie'

    if os.path.exists(cookieFile):
        os.remove(cookieFile)

    with open(cookieFile, 'w') as file:
        file.write(json.dumps(cookie))

    return "OK"

