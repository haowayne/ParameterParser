import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
}


def auto_send_packet(domin: str, data: dict):
    if data['url'][0] != '/':
        data['url'] = '/' + data['url']
    url = domin + data['url']
    if data['method'].upper() == 'POST':
        r = requests.post(url, params=data['parameter'], headers=headers)
    elif data['method'].upper() == 'GET':
        r = requests.get(url, params=data['parameter'], headers=headers)


if __name__ == '__main__':
    auto_send_packet('http://www.baidu.com',
                     {'url': '/cgi-bin/UploadCfg', 'method': 'POST', 'parameter': {'filename': ''}}
                     )
