from captchapop import CaptchaBox
import requests
import imgkit
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from PIL import Image


class KUDIGITAL:
    url = 'http://ku.digitaluniversity.ac/'
    resurl = 'SearchDuplicateResult.aspx'

    def __init__(self):
        page = requests.get(self.url+self.resurl)
        soup = BeautifulSoup(page.content.decode(), 'html.parser')
        self.sessionid = page.headers['Set-Cookie'].split(';')[0]
        self.viewstate = soup.find(id='__VIEWSTATE')['value']
        self.viewstategen = soup.find(id='__VIEWSTATEGENERATOR')['value']
        self.captchaurl = soup.find(
            id="ctl00_ContentPlaceHolder1_CaptchaControll_captchaImage")['src']
        events = soup.find_all('option')
        self.events = dict()
        for event in events:
            if event['value'] != '0':
                self.events[event.string] = event['value']

    def make(self, eventid, prn):
        eventid, prn = str(eventid), str(prn)
        self.prn = prn
        self.eventid = eventid
        self.header = {
            "Host": "ku.digitaluniversity.ac",
            "Content-Length": "2626",
            "Cache-Control": "no-cache",
            "X-Requested-With": "XMLHttpRequest",
            "X-MicrosoftAjax": "Delta=true",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "Origin": "http://ku.digitaluniversity.ac",
            "Referer": "http://ku.digitaluniversity.ac/SearchDuplicateResult.aspx",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": f"{self.sessionid}; Language=EN",
            "Connection": "close"
        }
        self.body = {
            "ctl00$Scriptmanager1": "ctl00$ContentPlaceHolder1$upSoG|ctl00$ContentPlaceHolder1$btnSearch",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": self.viewstate,
            "__VIEWSTATEGENERATOR": self.viewstategen,
            "__VIEWSTATEENCRYPTED": "",
            "ctl00$ContentPlaceHolder1$ExEv_ID": eventid,
            "ctl00$ContentPlaceHolder1$TxtPrn": prn,
            "ctl00$ContentPlaceHolder1$CaptchaControll$CodeNumberTextBox": self.captcha,
            "ctl00$ContentPlaceHolder1$hidInstID": "0",
            "ctl00$ContentPlaceHolder1$hidUniID": "86",
            "ctl00$ContentPlaceHolder1$hidFacID": "",
            "ctl00$ContentPlaceHolder1$hidCrID": "",
            "ctl00$ContentPlaceHolder1$hidMoLrnID": "",
            "ctl00$ContentPlaceHolder1$hidPtrnID": "",
            "ctl00$ContentPlaceHolder1$hidCourseDetails": "",
            "ctl00$ContentPlaceHolder1$hidBrnID": "",
            "__ASYNCPOST": "true",
            "ctl00$ContentPlaceHolder1$btnSearch": "Search"
        }

    def getcatpcha(self):
        self.captchareq = {
            "Host": "ku.digitaluniversity.ac",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": f"{self.sessionid}; Language=EN",
            "Connection": "close"
        }
        response = requests.get(self.url+self.captchaurl,
                                headers=self.captchareq)
        with open('captcha.jpeg', 'wb') as cpcha:
            for chunk in response:
                cpcha.write(chunk)
        img = Image.open('captcha.jpeg').convert('L')
        print('Waiting for captcha...')
        captchabox = CaptchaBox('captcha.jpeg')
        captchabox.show()
        self.captcha = captchabox.captcha

    def getdata(self, event_id, prn):
        self.make(event_id, prn)
        page = requests.post(self.url+self.resurl,
                             data=self.body, headers=self.header)
        soup = BeautifulSoup(page.content.decode(), 'html.parser')
        strr = page.content.decode()
        strr = strr[strr.find('__VIEWSTATE|')+len('__VIEWSTATE|'):]
        strr = strr[:strr.find('|')]
        self.viewstatenext = strr
        table = soup.find(
            'table', attrs={'id': 'ctl00_ContentPlaceHolder1_oGridViewExmdetails'})
        data = []
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            self.results = data[1:]
        else:
            errormsg = soup.find(
                id='ctl00_ContentPlaceHolder1_lblErrorMessage')
            self.err = 'Invalid Captcha!' if errormsg.string == 'Incorrect authorization code. Try again.' else errormsg.string
            self.results = None

    def getresult(self, res):
        self.body = {
            "ctl00$Scriptmanager1": "ctl00$ContentPlaceHolder1$upSoG|ctl00$ContentPlaceHolder1$oGridViewExmdetails",
            "ctl00$ContentPlaceHolder1$ExEv_ID": self.eventid,
            "ctl00$ContentPlaceHolder1$TxtPrn": self.prn,
            "ctl00$ContentPlaceHolder1$CaptchaControll$CodeNumberTextBox": self.captcha,
            "ctl00$ContentPlaceHolder1$hidInstID": "0",
            "ctl00$ContentPlaceHolder1$hidUniID": "86",
            "ctl00$ContentPlaceHolder1$hidFacID": "",
            "ctl00$ContentPlaceHolder1$hidCrID": "",
            "ctl00$ContentPlaceHolder1$hidMoLrnID": "",
            "ctl00$ContentPlaceHolder1$hidPtrnID": "",
            "ctl00$ContentPlaceHolder1$hidCourseDetails": "",
            "ctl00$ContentPlaceHolder1$hidBrnID": "",
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$oGridViewExmdetails",
            "__EVENTARGUMENT": f"DownloadMarksStatement${res}",
            "__VIEWSTATE": self.viewstatenext,
            "__VIEWSTATEGENERATOR": self.viewstategen,
            "__VIEWSTATEENCRYPTED": "",
            "__ASYNCPOST": "true"
        }
        self.head = {
            "Host": "ku.digitaluniversity.ac",
            "Content-Length": "3887",
            "Cache-Control": "no-cache",
            "X-Requested-With": "XMLHttpRequest",
            "X-MicrosoftAjax": "Delta = true",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset = UTF-8",
            "Accept": "*/*",
            "Origin": "http://ku.digitaluniversity.ac",
            "Referer": "http://ku.digitaluniversity.ac/SearchDuplicateResult.aspx",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US, en; q = 0.9",
            "Cookie": f"{self.sessionid}; Language = EN",
            "Connection": "close"
        }
        page = requests.post(self.url+self.resurl,
                             data=self.body, headers=self.head)
        soup = BeautifulSoup(page.content.decode(), 'html5lib')
        table = soup.find(id="ctl00_ContentPlaceHolder1_lblHTML")
        if input('Save result as JPG? (y/[n]): ') == 'y':
            imgkit.from_string(str(table), 'result.jpg', options={'quiet': ''})
            print("Saved as 'result.jpeg'!")
        # with Image.open('result.jpg') as img:
        #     img.show()
        data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        data = data[1:]
        self.results = data
        self.displayresult()

    def displayresult(self):
        data = self.results[:4]
        totalscore = 0
        reflag = False
        totalScaled = 0
        maxscore = 0
        scores = [row for row in self.results if len(row) == 14]
        print('\n')
        for i in data:
            for x in i:
                print(x)
        table = PrettyTable()
        table.field_names = ['Paper Code', 'Paper Name',
                             'Type', 'External', 'Internal', 'Total', 'Status']
        for r in scores:
            if not reflag and r[12] == 'F':
                reflag = True
            table.add_row([r[0], r[1], r[2], r[5]+'/'+r[3],
                           r[8]+'/'+r[6], r[11]+'/'+r[9], r[12]])
            if r[11].isnumeric():
                totalScaled += int(r[10]) if r[12] == 'F' else int(r[11])
                totalscore += int(r[11])
            else:
                totalScaled += 0
                totalscore += 0
            maxscore += int(r[9]) if r[9].isnumeric() else 0
        print(table)
        print(
            f'\nTotal: {totalscore}/{maxscore}  =  {round(totalscore*100/maxscore,2)}%')
        if reflag:
            print(
                f'Total Scaled to Re: {totalScaled}/{maxscore}  =  {round(totalScaled*100/maxscore,2)}%')
