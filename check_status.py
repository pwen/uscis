import click
import requests
from bs4 import BeautifulSoup as bs

def check_status(receipt_number):
    url = "https://egov.uscis.gov/casestatus/mycasestatus.do"
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language':
        'en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3',
        'Cache-Control': 'no-cache',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'egov.uscis.gov',
        'Referer': 'https://egov.uscis.gov/casestatus/mycasestatus.do',
    }
    data = {
        "changeLocale": "",
        "appReceiptNum": receipt_number,
        "initCaseSearch": "CHECK+STATUS",
    }
    response = requests.post(url, data=data, headers=headers)
    soup = bs(response.text,"html.parser")

    section = soup.find('div', {'class':"rows text-center"})
    status = section.h1.text
    description = section.p.text
    return (status, description)

@click.command()
@click.option('--receipt_number', prompt="Enter your Receipt Number")
def main(receipt_number):
    status, description = check_status(receipt_number)
    print(status)
    print('------------------------------------------')
    print(description)

if __name__=="__main__":
    main()
