# -*- coding: UTF-8 -*-
import requests
import re
import os

def getContent(url):
    req = requests.get(url=url)
    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding
    content = req.content.decode(encoding, 'replace')
    return content

def getTitleLink(content, pattern):
    text = re.findall(pattern, content)
    title = []
    links = []
    for each in text:
        content = re.search('title="(.*?)"', each)
        if content:
            title.append(content.group(1))
        link = re.search('href="(.*?)"', each)
        if link:
            links.append(link.group(1))
    return title, links

def getContentTime(content, pattern):
    text = re.findall(pattern, content)
    times = []
    for each in text:
        time = re.search('<div class="con1rm2l f xi35">\\r\\n       (.*?)-(.*?)<br>', each)
        if time:
            times.append([time.group(1), time.group(2)])
    return times

def getAbstract(content, pattern):
    text = re.findall(pattern, content)
    abstracts = []
    for each in text :
        abstract = re.search('<div class="con1rm2rf xi14">([^<]*)</div>', each)
        if abstract :
            abstracts.append(abstract.group(1))
    return abstracts

def display(dict_content):
    for i in range(len(dict_content)):
        print('第 ', i + 1, ' 条 :')
        print(dict_content[i]['month'], '月', dict_content[i]['day'], '日', '  ', dict_content[i]['title'])
        print(dict_content[i]['abstract'])
        print('链接地址 :  ', dict_content[i]['link'])
        print('----'*30)
    print('实际有: 20 条', '显示有 ', i + 1, ' 条')

def getDailyInfo(url, pattern):
    content = getContent(url)
    titles, links = getTitleLink(content, pattern)
    pattern = '<div class="con1rm2l f xi35">[^<]*<br>'
    times = getContentTime(content, pattern)
    pattern = '<div class="con1rm2rf xi14">[^<]*</div>'
    abstracts = getAbstract(content, pattern)
    months = [times[i][0] for i in range(len(times))]
    days = [times[i][1] for i in range(len(times))]
    daily = []
    for i in range(len(times)):
        daily.append({'month':months[i], 'day':days[i], 'title':titles[i], 'abstract':abstracts[i], 'link':links[i]})
    return daily

def textWrite(daily, catalog, total=20):
    basePath = os.path.dirname(os.path.abspath('__file__'))
    resultPath = os.path.join(basePath, 'result')
    with open(os.path.join(resultPath, catalog + '.txt'), 'w') as f:
        f.write('----'*30 + '\n')
        f.write('--'*10 + catalog + '--'*10 + '\n')
        f.write('----'*30 + '\n')
        for i in range(len(daily)):
            f.write('第 ' + str(i + 1) + ' 条 :\n' )
            f.write(daily[i]['month'] + '月' + daily[i]['day'] + '日' + daily[i]['title'] + '\n')
            f.write(daily[i]['abstract'] + '\n')
            f.write('链接地址 :  ' + daily[i]['link'] + '\n')
            f.write('----'*30 + '\n')
        f.write('----'*30)
        f.write('实际有: ' + str(total) + ' 条' + ' 显示有 ' + str(i + 1) + ' 条' )

def main_display():
    catalog = {'01学生思政_日常通知':1055856, '02学生思政_评奖评优':1055857, '03学生思政_勤工资助':1055858, '04学生思政_党建相关':1055855}
    resultPath = os.path.join(os.getcwd(), 'result')
    for each_file in os.listdir(resultPath):
        os.remove(os.path.join(resultPath, each_file))
    for key, value in catalog.items():
        # print('----'*30)
        # print('--'*10, key, '--'*10)
        # print('----'*30)
        url = 'http://www.cse.zju.edu.cn/redir.php?catalog_id=' + str(value)
        pattern = '<a href="redir.php\?catalog_id=' + str(value) + '&object_id=.*?</a>'
        daily = getDailyInfo(url, pattern)
        # display(daily)
        textWrite(daily, key)
        print('写入' + key + '.txt' + ' 成功!')


def getMaster(url, pattern):
    text = getContent(url)
    contents = re.findall(pattern, text)
    masters = []
    for each in contents:
        ea = re.search('<p><strong>(.*?)</strong><span>(.*?)</span>', each)
        if ea:
            masters.append({'title':ea.group(1), 'time':ea.group(2)})
        ea = re.search('href="(.*?)"', each)
        if ea:
            masters[-1]['link'] = ea.group(1)
    return masters

def masterWrite(masters, name, total):
    basePath = os.path.dirname(os.path.abspath('__file__'))
    resultPath = os.path.join(basePath, 'result')
    with open(os.path.join(resultPath, name + '.txt'), 'w') as f:
        f.write('----'*30 + '\n')
        f.write('--'*10 + name + '--'*10 + '\n')
        f.write('----'*30 + '\n')
        for i in range(len(masters)):
            f.write('第 ' + str(i + 1) + ' 条 :\n' )
            f.write(masters[i]['time'] + masters[i]['title'] + '\n')
            f.write('链接地址 :  ' + masters[i]['link'] + '\n')
            f.write('----'*30 + '\n')
        f.write('----'*30)
        f.write('实际有: ' + setr(total) + ' 条' + ' 显示有 ' + str(i + 1) + ' 条' )
    print('写入' + name + '.txt' + ' 成功!')

def main_master():
    url = 'http://www.cse.zju.edu.cn/mobile/redir.php?catalog_id=1055842'
    pattern = '<a href="redir.php\?catalog_id=1055842&object_id=[\s\S]*?</a>'
    name = '01研究生教育_最新消息'
    masters = getMaster(url, pattern)
    masterWrite(masters, name, 10)

if __name__ == "__main__" :
    main_display() # 获取学生思政网站
    main_master() # 获取研究生教育网站