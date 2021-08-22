import enum
from bs4 import BeautifulSoup
import csv,re
import bs4
from translate import trans, trans_para
import pickle
from functools import wraps,partial

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
            # print("FOUND QUOTATION")
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
    # print(type(soup))
    container=soup.find_all("div",id="readableContent")[0]
    secs=container.find_all("div1",id=re.compile(r"Sec0[0-9]+"))
    article=[]
    for sec in secs:
        print(sec.attrs)
        article.extend(parse(sec))
    return article
class Parser(object):
    def __init__(self,configs:dict) -> None:
        super().__init__()
        # Process control
        # self._leafNodeType=configs["leafNodeType"]
        # self._skipList=configs.get("skipList",[])
        # self._continueList=configs.get("continueList",[])
        # Tree properties
        # self.nowNode=None
        self.parentNode=None
        self.lastNode=None
        # Paragraph propertis
        self._quote=configs.get("quote","")
        self.paragraph=""
        self.lastSentence=""
        self.article=[]
    # @property
    # def leafNode(self):
    #     return self._leafNodeType
    # '''Rules: '''
    # @property
    # def skipList(self):
    #     return self._skipList
    # @property
    # def continueList(self):
    #     return self._continueList
    @property
    def quote(self):
        return self._quote
    
    def shouldContinue(self,node):
        raise NotImplementedError
    def dealLeafNode(self,node):
        raise NotImplementedError
    def ifDealLeaf(self,node):
        raise NotImplementedError
    def before_child(self,node):
        raise NotImplementedError
    def after_child(self,node):
        raise NotImplementedError

class EEBO_Parser(Parser):
    def __init__(self) -> None:
        # configs={
        #     "leafNodeType":
        #     "skipList":[],
        #     "continueList":    
        # }
        super().__init__({"quote":"data-pqp-search-type"})
        self._hrbr=0

    def ifDealLeaf(self,node):
        n=node
        if re.match("div[0-9]+",n.parent.name) and re.match("Sec[0-9]+",n.parent.get("id",""))\
            and type(node)==bs4.element.NavigableString:
            return True
        if node.parent.name in ["small"]:
            return False
        # while (node.parent.name in ["span","em"] or node.name in ["br","hr"] )and n.parent:
        while (re.match("(span|em|h[0-9]+|blockquote)",node.parent.name) or node.name in ["br","hr"] )and n.parent:
            n=n.parent
            if re.match("div[0-9]+",n.name) and re.match("Sec[0-9]+",n.get("id","")): # 是 Sec00X 的一部分
                return True
            # if n.name =="div" and n.get(self.quote)=="quotation": # 是引用下面的一部分
            #     return True
        return False
    def endParagraph(self):
        self.article.append(self.paragraph)
        self.lastSentence,self.paragraph="",""
        self._hrbr=0
    def dealLeafNode(self,node):
        if self._hrbr>=2:
            self.paragraph.strip(" ")
            if any([self.lastSentence.endswith(i) for i in ".?!@#$%^&"]): # 说明到了新段落
                self.endParagraph()
            else:
                self.paragraph+=" "
            self._hrbr=0
        if node.name in ["br","hr"]:
            self._hrbr+=1
        elif type(node)==bs4.element.NavigableString:
            sent=str(node.string).strip("\"\n")
            if self.parentNode.name in ["span","em"] and getattr(self.lastNode,"name","") in ["span","em"]:
                self.paragraph+=" "
            self.paragraph+=sent
            self.lastSentence=sent
            self.lastNode=self.parentNode
    def before_child(self,node):
        if node.name=="blockquote":
            self.endParagraph()
            self.paragraph+="QUOTE: "
    def after_child(self,node):
        if node.name=="blockquote":
            self.endParagraph()
class Controller(object):
    def __init__(self, htmlpath,parser:Parser) -> None:
        super().__init__()
        self.htmlpath=htmlpath
        self.parser=parser
        self.container=None
    def explore(self,node)->list:
        if not hasattr(node,"children") or len(list(node.children))==0: # 叶子
            if self.parser.ifDealLeaf(node):
                self.parser.dealLeafNode(node)
            return
        for child in node.children:
            self.parser.parentNode=node
            self.parser.before_child(child)
            self.explore(child)
            self.parser.after_child(child)
        return
            
class EEBO_Controller(Controller):
    def __init__(self, htmlpath,parser) -> None:
        super().__init__(htmlpath,parser)
        soup=BeautifulSoup(open(self.htmlpath,"r", encoding="utf-8"),"html.parser")
        self.container=soup.find_all("div",id="readableContent")[0]
        print(len(self.container))

if __name__=="__main__":
    lister=[]
    with open("./papers.csv","r", encoding="utf-8") as f:
        read=csv.reader(f)
        lister=[i for i in read]
    for index,i in enumerate(lister):
        if index!=4: continue
        if i[1]=="EEBO":
            path=i[3]
            title=i[2]
            print(title)
            parser=EEBO_Parser()
            controller=EEBO_Controller(path,parser)
            controller.explore(controller.container)
            # content=decodeEEBO(path)
            content=parser.article
            for i,t in enumerate(content):
                content[i]=re.sub("[ ]+"," ",t)
            print("We get: ",len(content))
            _=[print("*"*20,"\n",i) for i in content]
            # zh_content=[]
            # for i,para in enumerate(content):
            #     zh_para=trans_para(para)
            #     zh_content.append(zh_para)
            #     print(i,zh_para)
            # name=path.split("/")[-1].split(".")[0]
            # filename=name+".pkl"
            # with open("./ckpt/"+filename,"wb+") as f:
            #     pickle.dump(zh_content,f)
    # path=lister[1][3]
    # print(path)
    # title=lister[1][2]
    # print(title)
    # content=decodeEEBO(path)
    # for i,t in enumerate(content):
    #     content[i]=re.sub("[ ]+"," ",t)
    # print("We get: ",len(content))
    # # print(content)
    # a=[print("*"*20,"\n",i) for i in content]
    # zh_content=[]
    # for para in content:
    #     if len(para)>200:
    #         sentences=para.split(".")
    #         zh_para=""
    #         for sent in sentences:
    #             if len(sent)>1500:
    #                 parts=sent.split(";")
    #                 pret=""
    #                 for i,p in enumerate(parts):
    #                     ret=trans(p)
    #                     if i+1<len(parts):
    #                         ret+"；"
    #                     pret+=ret
    #                 pret+="。"
    #                 zh_para+=pret
    #             else:
    #                 rsent=trans(sent)
    #                 rsent+="。"
    #                 zh_para+=rsent
    #     else:
    #         zh_para=trans(para)
    #     zh_content.append(zh_para)
    #     print(zh_para)
    # with open("ckpt/"+title+".pkl","wb") as f:
    #     pickle.dump(zh_content,f)
