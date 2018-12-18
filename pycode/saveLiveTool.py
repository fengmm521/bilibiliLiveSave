#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-18 20:53:22
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os,sys
import requests
import chardet  #中文编码判断
import json

def conventStrTOUtf8(oldstr):
    cnstrtype = chardet.detect(oldstr)['encoding']
    try:
        utf8str =  oldstr.decode(cnstrtype).encode('utf-8')
    except Exception as e:
        utf8str =  oldstr.encode('utf-8')
    return utf8str

def getUrl(purl):
    
    urlrequ = purl
    
    try:
        # req = urllib2.Request(urlrequ)
        headers = {'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        # user-agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
        # req.add_header('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36')
        res = requests.get(urlrequ, headers=headers)
        html = res.text.encode('utf8')
        return html
    except Exception, e:
        return None

def findLiveJson(txt):
    startdiv = txt.find('<div class=script-requirement>') + len('<div class=script-requirement>')
    enddiv = startdiv + txt[startdiv:].find('</div>')
    jsontmp = txt[startdiv:enddiv]
    jstart = jsontmp.find('{')
    jend = jsontmp.find('</script>')
    jsonstr = jsontmp[jstart:jend]
    return jsonstr

def getLiveURLFromJson(jstr):
    jtmp = json.loads(jstr)
    if 'playUrlRes' in jtmp:
        urls = jtmp['playUrlRes']['data']['durl']
        return urls

def getAllURL(urls):
    out = []
    for i,item in enumerate(urls):
        # tmp = item['url'][:item['url'].find('trid')-1]
        out.append(item['url'])
    return out

def main(purl="https://live.bilibili.com/9986650",chunnel = 0):
    txt = getUrl(purl)
    jsonstr = findLiveJson(txt)
    if jsonstr:
        # print(jsonstr)
        urls = getLiveURLFromJson(jsonstr)
        allurl = getAllURL(urls)
        print(allurl[chunnel])

def test(purl = 'https://live.bilibili.com/697972'):
    main(purl)
#测试
if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2 :
        fpth = args[1]
        if len(fpth) < 3:
            main(chunnel = int(fpth))
        else:
            main(purl = fpth)
    elif len(args) == 3:
        purl = args[1]
        chunel = args[2]
        main(purl,int(chunel))
    else:
        main()
        # test()
    

    
