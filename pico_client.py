import sys
import http.client
import requests
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

def get_data(client_ip):
 
    response = requests.get(client_ip, headers=headers, timeout=10)
    return response.text


if __name__=="__main__":
    
    if len(sys.argv) > 1:
        data = get_data('http://'+sys.argv[1])
    else:
        data = get_data('http://192.168.2.1')
    now = datetime.datetime.now()
    
    print(now.strftime("%Y-%m-%d %H:%M:%S, ") + data)



