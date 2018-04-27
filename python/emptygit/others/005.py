

#coding=utf-8
import re
import urllib2
from random import choice
import HTMLParser
parser = HTMLParser.HTMLParser()

f = open('URLtext2','r')
urllist = f.readlines()
iplist=['118.1899.69.34','124.193.144.238','211.144.76.58','58.248.137.228']

def getInfo(url):
    def getHtml(url):
        ip = choice(iplist)
        proxy_support = urllib2.ProxyHandler({'https': 'https://' + ip})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

        page = urllib2.urlopen(url)
        html = page.read()
        return html
    html = getHtml(url)
    def getTel(html):
        req = r'<span itemprop="telephone">(.*?)</span>*'
        telre = re.compile(req)
        tel = re.findall(telre, html)
        return tel

    def getFax(html):
        req = r'<span itemprop="faxNumber">(.*?)</span>*'
        faxre = re.compile(req)
        fax = re.findall(faxre, html)
        return fax

    def getEmail(html):
        req = r'itemprop="email">(.*?)</a>*'
        emailre = re.compile(req)
        email = re.findall(emailre, html)
        return email
    def getCompanyname(html):
        req = r'<h1 itemprop="name" class="beta flush--bottom push--top">(.*?)</h1>*'
        namere = re.compile(req)
        name = re.findall(namere, html)
        return parser.unescape(name)
    def getHomepage(html):
        req = r'<a href="(.*?)\".*?itemprop="url" >'
        homepagere = re.compile(req)
        homepage = re.findall(homepagere, html)
        return homepage
    def getCompanyDetail(html):
        req = r'Company details</h3>(\s*([\s\S]*?)\s*)</div>'
        detailre = re.compile(req)
        detail = re.findall(detailre, html)
        reqq = r'\">(.*?)\''
        try:
            detailin = re.search(re.compile(reqq), str(detail)).group(0)
            strinfo = str(detailin).replace('>','',1)
            return strinfo.replace('<br />', '')
        except:
            return 'none'
    def getCompanyData(html):
        req = r'Company data</h3>((\s*([\s\S]*?)\s*))</div>*'
        datare = re.compile(req)
        try:
            data = re.search(datare, html).group(0)
            str1 = str(data)
            str2 = str1.replace('Company data</h3>', '')
            str2 = str2.replace('<strong>', '')
            str2 = str2.replace('</strong>', '')
            str2 = str2.replace('</div>', '')
            str2 = str2.replace('  ', '')
            str2 = str2.replace('</p>', '.  ')
            str2 = str2.replace('<br />', '-->')
            str2 = str2.replace('<p>','')
            str2 = str2.replace('<li>', '||')
            str2 = str2.replace('</li>','&')
            str2 = str2.replace('</ul>', '')
            str2 = str2.replace('<ul>', '')
            str2 = str2.replace('\n','')
            return str2
        except:
            return 'none'
    tel = getTel(html)
    fax = getFax(html)
    email = getEmail(html)
    company = getCompanyname(html)
    homepage = getHomepage(html)
    companydetail = getCompanyDetail(html)
    companydata = getCompanyData(html)
    print tel , fax , email , company ,homepage , companydetail, companydata
    infostr = url + '  ' + 'Tel > ' + str(tel) + '  ' + 'Fax > ' + str(fax) + '  ' + 'E_mail > ' + str(email) + '  ' + 'CompanyName > ' + str(company) + '  ' + 'HomePage > ' + str(homepage) + '  ' + 'CompanyDetails > [' + companydetail + ']  ' + 'CompanyData > [' + companydata +']\n\n'
    f = open('URLtext', 'a')
    f.writelines(infostr)
    f.close()


for url in urllist[1:3]:
    print url
    getInfo(url)
