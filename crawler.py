import io
import sys
import requests
import json
import bs4
import csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'}

baseUrl = 'https://www.zhihu.com/api/v4/questions/66515131/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={0}&offset={1}' # from Inspect --> Network --> XHR
url = baseUrl.format('5', '0') # limit and offset, current max offset is 1075

answers = []
isEnd = False


while not isEnd:

    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    responseDict = json.loads(response.text)

    for answersHtml in responseDict['data']:

        answer = ''
        soup = bs4.BeautifulSoup(answersHtml['content'], 'html.parser')

        for paragraphHtml in soup.findAll('p'):

            answer += paragraphHtml.text
            answer += '\n\n'

        answers.append([answer]) # [] for csv writer use

    isEnd = responseDict['paging']['is_end']
    url = responseDict['paging']['next']


with open('rawAnswer.csv', 'w') as f:

    writer = csv.writer(f)

    for answer in answers:
        writer.writerow(answer)
