import enum
from bs4 import BeautifulSoup
import csv,re

import bs4
def parse(tag)->list:
    return []
def decodeEEBO(htmlFilePath:str)->list:
    # 返回一个列表，其中每个元素是一个段落
    assert htmlFilePath.endswith("html")
    soup=BeautifulSoup(open(htmlFilePath,"r", encoding="utf-8"),"html.parser")
    print(type(soup))
    container=soup.find_all("div",id="readableContent")[0]
    secs=container.find_all("div1",id=re.compile(r"Sec0[0-9]+"))
    # for sec in secs:
    #     print(sec.attrs)
    #     c=sec.contents
    #     print("C is: ",len(c))
    sec=secs[1]
    print(sec.name)
    article=[]
    lastChild=None
    lastSentence=""
    paragraph=""
    hrbr=0
    quote="data-pqp-search-type"
    for item in sec.children:
        # print("{}:{},{}".format(item.name,type(item),item.attrs if hasattr(item,"attrs") else ""))
        # print("{}:{},{}".format(item.name,type(item),len(item.contents) if hasattr(item, "contents") else ""))
        # if type(item)== bs4.element.NavigableString:
        #     print(item.string)
        if type(item)!=bs4.element.NavigableString and type(item)!=bs4.element.Tag:
            continue
        if item.name=="div" and "dpmi_image" in item["class"]:
            continue
        if item.name in ["small"]:
            continue
        if item.name in ["br","hr"]:
            hrbr+=1
        elif item.name in ["span","em"] or type(item)==bs4.element.NavigableString:
            sent=str(item.string).strip("\"\n")
            
            if hrbr>=2:
                if any([lastSentence.endswith(i) for i in ".?!@#$%^&"]): # 说明到了新段落
                    article.append(paragraph)
                    hrbr=0
                    paragraph=""
                    lastSentence=""
                else:
                    paragraph+=" "
                    hrbr=0
            if item.name in ["span","em"]:
                if lastChild.name in ["span","em"]:
                    sent=str(item.string)
                    paragraph+=" "
            paragraph+=sent
            lastChild=item
            lastSentence=sent
        if item.name =="div" and item.__contains__(quote) and item[quote]=="quotation":
            item=item.find("blockquote")
            paras=parse(item) # 返回的应该是列表
            article.extend(paras)
        else:
            continue
    print("hrbr number: ",hrbr)
    return article
    pass
if __name__=="__main__":
    lister=[]
    with open("./papers.csv","r", encoding="utf-8") as f:
        read=csv.reader(f)
        lister=[i for i in read]
    for i in lister:
        if i[1]=="EEBO":
            pass
    path=lister[1][3]
    print(path)
    title=lister[1][2]
    content=decodeEEBO(path)
    for i,t in enumerate(content):
        content[i]=re.sub("[ ]+"," ",t)
    print("We get: ")
    # print(content)
    a=[print("*"*20,"\n",i) for i in content]
