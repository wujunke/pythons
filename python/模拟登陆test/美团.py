#coding=utf-8
import HTMLParser

s = '&#33529;&#26524;'
parser = HTMLParser.HTMLParser()
print parser.unescape(s)


