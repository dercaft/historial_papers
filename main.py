import csv,re
import pickle
from docx import Document
import pickle

from translate import trans_para
from generate import EEBO_Controller,EEBO_Parser
from generate import OLL_Parser,OLL_Controller
if __name__=="__main__":
    lister=[]
    with open("./papers.csv","r", encoding="utf-8") as f:
        read=csv.reader(f)
        lister=[i for i in read]
    for index,i in enumerate(lister):
        if index <10 : continue
        title,path=i[2],i[3]

        if i[1]=="EEBO":
            parser=EEBO_Parser()
            controller=EEBO_Controller(path,parser)
        elif i[1]=="OLL":
            parser=OLL_Parser()
            controller=OLL_Controller(path,parser)
        else: continue
        controller.explore(controller.container)
        content=parser.article
        for i,t in enumerate(content):
            content[i]=re.sub("[ ]+"," ",t)
        # print(content)
        # a=[print("*"*20,"\n",i) for i in content]
        print("*"*20)
        print(title)
        zh_content=[]
        for i,para in enumerate(content):
            zh_para=trans_para(para)
            zh_content.append(zh_para)
            print(i,zh_para)
        name=path.split("/")[-1].split(".")[0]
        filename=name+".pkl"
        print("We get: ",len(content))
        print(len(path),path)
        print(len(name),name)
        print("*"*20)
        with open("./ckpt/"+filename,"wb+") as f:
            pickle.dump(zh_content,f)
            
        en=content
        zh=zh_content
        n=name
        document=Document()
        para=document.add_heading(title)
        for j,(e,z) in enumerate(zip(en,zh)):
            document.add_paragraph(e)
            document.add_paragraph(z)
        document.save("result/{}.docx".format(n))
