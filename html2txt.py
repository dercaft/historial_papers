import csv,re,os
from generate import EEBO_Controller,EEBO_Parser
from generate import OLL_Parser,OLL_Controller
FILE_PATH="./papers2.csv"
if __name__=="__main__":
    lister=[]
    assert os.path.isfile(FILE_PATH)
    with open(FILE_PATH,"r", encoding="utf-8") as f:
        read=csv.reader(f)
        lister=[i for i in read]
    for index,i in enumerate(lister):
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
            content[i]=re.sub("(〈◊〉|〈◊◊〉)","",content[i])
        name=path.split("/")[-1].split(".")[0]
        with open(os.path.join("./txt",name+".txt") ,"w+",encoding="utf-8") as f:
            for line in content:
                f.write(line)     
                f.write("\n")     
