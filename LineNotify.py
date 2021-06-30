import requests

def SendMessageToLineNotify(message,Token):
        Token = Token
        url = "https://notify-api.line.me/api/notify"    
        payload = {'message':message,
                   
                }
        header = {'Content-Type':'application/x-www-form-urlencoded',
               'Authorization':'Bearer ' + Token
                 }
        resp=requests.post(url, headers=header, data=payload)
        print ("Line Notify \a :" + message)
def main():
        message = ""
        picurl = ''
        token = ""
        SendMessageToLineNotify(message,token)
if __name__ == '__main__':
        main()
