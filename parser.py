import enum
from bs4 import BeautifulSoup
import csv,re
import bs4
from translate import trans
import pickle
def parse(sec,isquote=False)->list:
    article=[]
    lastChild=None
    lastSentence,paragraph,hrbr="","",0
    quote="data-pqp-search-type"
    for item in sec.children:
        if item.name in ["br","hr"]:
            hrbr+=1
        elif item.name in ["span","em"] or type(item)==bs4.element.NavigableString:
            if not item.string:
                text=item.text
                sent="".join([i.strip("\"\n") for i in text])
            else:
                sent=str(item.string).strip("\"\n")
            if hrbr>=2 and paragraph:
                paragraph.strip()
                if any([lastSentence.endswith(i) for i in ".?!@#$%^&"]): # 说明到了新段落
                    article.append(paragraph)
                    lastSentence,paragraph,hrbr="","",0
                else:
                    paragraph+=" "
                    hrbr=0
            if item.name in ["span","em"]:
                if lastChild and lastChild.name in ["span","em"]:
                    paragraph+=" "
            paragraph+=sent
            lastChild=item
            lastSentence=sent
        elif item.name =="div" and item.get(quote)=="quotation":
            if hrbr>=2 and paragraph:
                paragraph.strip()
                if any([lastSentence.endswith(i) for i in ".?!@#$%^&"]): # 说明到了新段落
                    article.append(paragraph)
                    lastSentence,paragraph,hrbr="","",0
                else:
                    paragraph+=" "
                    hrbr=0
            print("FOUND QUOTATION")
            item=item.find("blockquote")
            paras=parse(item,True) # 返回的应该是列表
            article.extend(paras)
        else:
            continue
    if paragraph and not article:
        article.append(paragraph)
    if isquote:
        article=["QUOTE: "+i for i in article]
    return article
def decodeEEBO(htmlFilePath:str)->list:
    # 返回一个列表，其中每个元素是一个段落
    assert htmlFilePath.endswith("html")
    soup=BeautifulSoup(open(htmlFilePath,"r", encoding="utf-8"),"html.parser")
    print(type(soup))
    container=soup.find_all("div",id="readableContent")[0]
    secs=container.find_all("div1",id=re.compile(r"Sec0[0-9]+"))
    article=[]
    for sec in secs:
        print(sec.attrs)
        article.extend(parse(sec))
    return article

if __name__=="__main__":
    lister=[]
    with open("./papers.csv","r", encoding="utf-8") as f:
        read=csv.reader(f)
        lister=[i for i in read]
    # for i in lister:
    #     if i[1]=="EEBO":
    #         path=i[3]
    #         title=i[2]
    #         print(title)
    #         content=decodeEEBO(path)
    #         pass
    path=lister[1][3]
    print(path)
    title=lister[1][2]
    print(title)
    content=decodeEEBO(path)
    for i,t in enumerate(content):
        content[i]=re.sub("[ ]+"," ",t)
    print("We get: ",len(content))
    # print(content)
    a=[print("*"*20,"\n",i) for i in content]
    zh_content=[]
    for para in content:
        if len(para)>200:
            sentences=para.split(".")
            zh_para=""
            for sent in sentences:
                if len(sent)>1500:
                    parts=sent.split(";")
                    pret=""
                    for i,p in enumerate(parts):
                        ret=trans(p)
                        if i+1<len(parts):
                            ret+"；"
                        pret+=ret
                    pret+="。"
                    zh_para+=pret
                else:
                    rsent=trans(sent)
                    rsent+="。"
                    zh_para+=rsent
        else:
            zh_para=trans(para)
        zh_content.append(zh_para)
        print(zh_para)
    with open("ckpt/"+title+".pkl","wb") as f:
        pickle.dump(zh_content,f)
