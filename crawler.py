import io
import sys
import requests
import bs4

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'}

url = 'https://www.zhihu.com/question/66515131'

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

soup = bs4.BeautifulSoup(response.text, 'html.parser')

print(soup)
