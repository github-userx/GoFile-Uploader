import requests
import os
import time
import re

logo = """
   ___          ,__     .                             .                      _             
 .'   \    __.  /  ` `  |     ___       ,   . \,___,  |     __.    ___    ___/   ___  .___ 
 |       .'   \ |__  |  |   .'   `      |   | |    \  |   .'   \  /   `  /   | .'   ` /   \\
 |    _  |    | |    |  |   |----'      |   | |    |  |   |    | |    | ,'   | |----' |   '
  `.___|  `._.' |    / /\__ `.___,      `._/| |`---' /\__  `._.' `.__/| `___,' `.___, /    
                /                             \                              `             
"""
prefix = '{~}'

def getServer():
    try:
        req = requests.get('https://api.gofile.io/getServer')
        res = req.json()
        return res['data']['server']
    except Exception as ex:
        print('{~} Unknown error at getServer: '+str(ex))
        print('{~} Response: '+str(res))

def uploadFile(server, usrfile, desc='', passw=''):
    try:
        files = {'file': (os.path.basename(usrfile), open(str(usrfile), 'rb'), 'multipart/form-data')}

        if desc != '' and passw == '':
            req = requests.post('https://{0}.gofile.io/uploadFile'.format(server), files=files, data={'description':desc})
        elif passw != '' and desc == '':
            req = requests.post('https://{0}.gofile.io/uploadFile'.format(server), files=files, data={'password':passw})
        elif passw != '' and desc != '':
            req = requests.post('https://{0}.gofile.io/uploadFile'.format(server), files=files, data={'description':desc, 'password':passw})
        else:
            req = requests.post('https://{0}.gofile.io/uploadFile'.format(server), files=files)

        res = req.json()
        if res['status'] == 'ok':
            if passw != '' and desc == '':
                return '\n{0} File uploaded successfully:\n File name: {1}\n Link: {2}\n File id: {3}\n MD5: {4}\n Password: {5}'.format(prefix, res['data']['fileName'], res['data']['downloadPage'], res['data']['fileId'], res['data']['md5'], passw)
            elif desc != '' and passw == '':
                return '\n{0} File uploaded successfully:\n File name: {1}\n Link: {2}\n Description: {3}\n File id: {4}\n MD5: {5}'.format(prefix, res['data']['fileName'], res['data']['downloadPage'], desc, res['data']['fileId'], res['data']['md5'])
            elif desc != '' and passw != '':
                return '\n{0} File uploaded successfully:\n File name: {1}\n Link: {2}\n Description: {3}\n File id: {4}\n MD5: {5}\n Password: {6}'.format(prefix, res['data']['fileName'], res['data']['downloadPage'], desc, res['data']['fileId'], res['data']['md5'], passw)
            else:
                return '\n{0} File uploaded successfully:\n File name: {1}\n Link: {2}\n File id: {3}\n MD5: {4}'.format(prefix, res['data']['fileName'], res['data']['downloadPage'], res['data']['fileId'], res['data']['md5'])
        else:
            return '\n{0} File uploaded unsuccessfully:\n Status: {1}\n Data: {2}'.format(prefix, res['status'], res['data'])
    except Exception as ex:
        print('{~} Unknown error at uploadFile: '+str(ex))

if __name__ == '__main__':
    try:
        print(logo)

        usrFile = input('{~} Enter path to the file, example C:\\Users\\Admin\\Desktop\\file.txt .\\file.txt:\n > ')

        if not os.path.exists(usrFile):
            while not os.path.exists(usrFile):
                usrFile = input('{~} Enter valid path to the file:\n > ')
        
        usrDesc = input('{~} Write description to the file, leave empty if you dont want add a description:\n > ')
        usrPass = input('{~} Enter password to the file, leave empty if you dont wand add a password:\n > ')

        if len(usrPass) <= 3 and re.search('[a-zA-Z0-9]', usrPass):
            while len(usrPass) <= 3 and re.search('[a-zA-Z0-9]', usrPass):
                usrPass = input('{~} Password length must be at least 4 characters:\n > ')

        print('\n{~} Getting best available server to upload ...')
        server = getServer()

        print('{~} Uploading file ...')
        starttime = time.time()

        usrFile = usrFile if re.search('[a-zA-Z0-9]', usrFile) else ''
        usrDesc = usrDesc if re.search('[a-zA-Z0-9]', usrDesc) else ''

        print(uploadFile(server, usrFile, usrDesc, usrPass))
        
        totaltime = time.time() - starttime
        print('{~} Estimated time: '+str(totaltime))
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt')
        quit()