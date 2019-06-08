import re
import requests
import bs4
import crawler

url = 'http://www.dxsxs.com/mingzhu/1126/'
res = requests.get(url)
soup = bs4.BeautifulSoup(res.text, 'html.parser')

links = [tag['href'] for tag in soup.findAll('a', {'href':True})]
sepURL = url.split('/')
home = '/'.join(sepURL[:3])

for link in links:
    if '/'+sepURL[-2] not in link: continue # '/BOOKNUMBER' must in link
    if link[0] is not '/': continue # link must be relative address
    name = re.findall('[0-9]+', link)[-1] # find webpage index
    crawler._getText(home+link,
                     'utf-8',
                     '/Users/wlt/Desktop/BWBJ/{0}.txt'.format(name),
                     False)
    print(link)
