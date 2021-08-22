import csv,re
import pickle
from translate import trans_para
from generate import EEBO_Controller,EEBO_Parser
if __name__=="__main__":
    lister=[]
    with open("./papers.csv","r", encoding="utf-8") as f:
        read=csv.reader(f)
        lister=[i for i in read]
    for index,i in enumerate(lister):
        if index<5: continue
        title,path=i[2],i[3]
        print(title)
        if i[1]=="EEBO":
            parser=EEBO_Parser()
            controller=EEBO_Controller(path,parser)
            controller.explore(controller.container)
            content=parser.article
            for i,t in enumerate(content):
                content[i]=re.sub("[ ]+"," ",t)
            print("We get: ",len(content))
            # print(content)
            a=[print("*"*20,"\n",i) for i in content]
            zh_content=[]
            for i,para in enumerate(content):
                zh_para=trans_para(para)
                zh_content.append(zh_para)
                print(i,zh_para)
            name=path.split("/")[-1].split(".")[0]
            filename=name+".pkl"
            with open("./ckpt/"+filename,"wb+") as f:
                pickle.dump(zh_content,f)