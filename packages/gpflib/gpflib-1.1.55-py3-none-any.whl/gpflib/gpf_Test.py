import threading
import json
import re
import os,glob
from gpflib import GPF
import requests
import jieba
import gpflib

def PrintRelation(gpf):
    Relations=gpf.GetRelations()
    for R in Relations:
        Relation=gpf.GetWord(R["U1"])+" "+gpf.GetWord(R["U2"])+"("+R["R"]+")"
        KVs=gpf.GetRelationKVs(R["U1"],R["U2"],R["R"])
        Info=""
        for k in KVs:
            Val=" ".join(KVs[k])
            if len(KVs[k]) > 1:
                Info=Info+k+"=["+Val+"] "
            else:
                Info=Info+k+"="+Val+" "
            print("=>"+Relation)
        if Info != "":
	        print("KV:"+Info)


def PrintUnit(gpf,Type=""):
    if Type =="":
        Type="Type=Chunk|Type=Word|Type=Phrase|Type=Char"	
    GridInfo=gpf.GetGrid()
    for Col in GridInfo:
        for Unit in Col:
            if gpf.IsUnit(Unit,Type):
                Info=""
                KVs=gpf.GetUnitKVs(Unit)
                print("=>",gpf.GetWord(Unit))
                for K in KVs:
                    Val=" ".join(KVs[K])
                    print(K,"=",Val)



def Test_Grid():
    gpf = GPF("config.txt")
    Line='{"Type": "Chunk", "Units": ["瑞士球员塞费罗维奇", "率先", "破门", "，", "沙其理", "梅开二度", "。"], "POS": ["NP", "XP", "VP", "w", "NP", "VP", "w"], "Groups": [{"HeadID": 1, "Group": [{"Role": "sbj", "SubID": 0}]}, {"HeadID": 2, "Group": [{"Role": "sbj", "SubID": 0}]}, {"HeadID": 5, "Group": [{"Role": "sbj", "SubID": 4}]}],"ST":"dep"}'
    gpf.AddGridJS(Line)
    Grid = gpf.GetGrid()
    for C in Grid:
        for U in C:
            print(U,gpf.GetWord(U))
            
    KV = gpf.GetGridKVs("")
    for K in KV:
        for V in KV[K]:
            print(K,V)

def Test_JSON():
    Line= """
    {"Words": ["瑞士", "率先", "破门", "，", "沙其理", "梅开二度", "。"], 
    "Tags": ["ns", "d", "v", "w", "nr", "i", "w"], 
    "Relations": [{"U1": 2, "U2":0,"R":"A0","KV":"KV1"},
    {"U1": 2, "U2":1,"R":"Mod","KV":"KV2"},
    {"U1": 5, "U2":4,"R":"A0","KV":"KV3"}]} """
    gpf = GPF()
    
    json_data = json.loads(Line)
    Sentence="".join(json_data["Words"])
    gpf.SetGridText(Sentence)
    Units=[]
    Col=0
    for i in range(len(json_data["Words"])):
        Col=Col+len(json_data["Words"][i])
        print(json_data["Words"][i],Col-1)
        Unit=gpf.AddUnit(Col-1,json_data["Words"][i])
        gpf.AddUnitKV(Unit,"POS",json_data["Tags"][i])
        Units.append(Unit)
        
    for i in  range(len(json_data["Relations"])):
        U1=Units[json_data["Relations"][i]["U1"]]
        U2=Units[json_data["Relations"][i]["U2"]]
        R=json_data["Relations"][i]["R"]
        KV=json_data["Relations"][i]["KV"]
        gpf.AddRelation(U1,U2,R)
        gpf.AddRelationKV(U1,U2,R,"KV",KV)

    GridInfo=gpf.GetGrid()
    for C in GridInfo:
        for U in  C:
            print("=>",gpf.GetWord(U))
	
    Rs = gpf.GetRelations("")
    for R in Rs:
        print(gpf.GetWord(R["U1"]),gpf.GetWord(R["U2"]),R["R"])
    print(gpf.GetText(0,-1))


def Test_TermInfo():
    gpf = GPF()
    Line="称一种无线通讯技术为蓝牙"
    gpf.SetGridText(Line)
    gpf.CallTable("Segment_Term")
    gpf.CallFSA("Term")
    Units=gpf.GetUnit("Tag=Term")
    for i in range(len(Units)):
        print(gpf.GetWord(Units[i]))     

def Idx_GPF(Name,Path="./data"):
    for file in glob.glob(Path):
        if os.path.isfile(file):
            os.remove(file)

    gpf = GPF(Path)
    FSA="./Examples/"+Name+"/GPF.fsa"
    if os.path.exists(FSA):
        gpf.IndexFSA(FSA)
    Table="./Examples/"+Name+"/GPF.tab"
    if os.path.exists(Table):
        gpf.IndexTable(Table)
   
def Test_Time():
    Line="星期日下午我去图书馆"
    gpf = GPF()
    gpf.SetGridText(Line)
    gpf.CallTable("Time_Entry")
    gpf.CallFSA("Time")
    Us=gpf.GetUnit("Tag=Time")
    for U in Us:
        print(gpf.GetWord(U))


def Test_DupWord():
    Sent="李明回头看了一看。"
    gpf = GPF()
    Segment=gpf.Parse(Sent,Structure="Segment")
    gpf.AddGridJS(Segment)
    gpf.CallFSA("DupWord")
    Units=gpf.GetUnit("Tag=DupWord")
    for i in range(len(Units)):
        print(gpf.GetWord(Units[i]))

def Test_Merge():
    Line = "下半场的38分钟，李明攻入第1个球，成功将比分扳平至2-1。"
    gpf = GPF()
    gpf.SetGridText(Line)
    depseg_struct = gpf.Parse(Line, "depseg")
    gpf.AddGridJS(depseg_struct)
    gpf.CallTable("Merge_Dict")
    gpf.CallFSA("Merge")
    phrase_units = gpf.GetUnit("Tag=MatchTime|Tag=Order|Tag=MatchScore")
    for i in range(len(phrase_units)):
        print(gpf.GetWord(phrase_units[i]))

def Test_Mood():
    Sent="李明非常不喜欢他"
    gpf = GPF()
    gpf.SetGridText(Sent)
    DepStruct=gpf.Parse(gpf.GetText(),Structure="Dependency")
    gpf.AddGridJS(DepStruct)
    Seg=gpf.Parse(gpf.GetText(),Structure="Segment")
    gpf.AddGridJS(Seg)
    gpf.CallTable("Tab_Mod")
    gpf.CallFSA("Mod2Head")
    gpf.CallFSA("Mod2Prd")
    Logs=gpf.GetLog()
    for log in Logs:
        print(log)
    Units=gpf.GetUnit("Tag=Mood")
    for i in range(len(Units)):
        print(gpf.GetWord(Units[i]))


def Test_WSD():
    gpf=GPF()
    Sentence="这个苹果很甜呀"
    gpf.SetTable("Dict_Info")
    gpf.SetGridText(Sentence)
    Segment=gpf.Parse(gpf.GetText(),Structure="Segment")
    gpf.AddGridJS(Segment)
    Units=gpf.GetUnit("Sem=*")
    for i in range(len(Units)):
        Sems=gpf.GetUnitKVs(Units[i],"Sem")
        MaxScore=-10
        WS=""
        for j in range(len(Sems)):
            gpf.CallFSA("WSD","Sem="+Sems[j])
            Score=gpf.GetUnitKVs(Units[i],"Sem_"+Sems[j])
            if len(Score) != 0:
                Score=int(Score[0])
            else:
                Score=0
            if MaxScore < Score:
                MaxScore = Score
                WS=Sems[j]
        if WS != "":
            gpf.AddUnitKV(Units[i],"Sense",WS)
    Units=gpf.GetUnit("Sense=*")
    for i in range(len(Units)):
        WS,=gpf.GetUnitKVs(Units[i],"Sense")
        print(gpf.GetWord(Units[i]),WS)

def Test_SepWord(Type):
    Sent="李明把守的大门被他破了"
    gpf=GPF()
    gpf.SetGridText(Sent)
    DepStruct=gpf.Parse(gpf.GetText(),Structure="Dependency")
    gpf.AddGridJS(DepStruct)
    Seg=gpf.Parse(gpf.GetText(),Structure="Segment")
    gpf.AddGridJS(Seg)
    gpf.CallTable("Sep_V")
    if Type == 1:
        gpf.CallFSA("SepV1")
    else:
        gpf.CallFSA("SepV2")
    Units=gpf.GetUnit("Tag=SepWord")
    for  Unit in Units:
        print(gpf.GetWord(Unit))

def Test_CoEvent():
    Sentence="淘气的孩子打碎了一个花瓶。"
    gpf=GPF()
    gpf.SetGridText(Sentence)
    DepStruct=gpf.Parse(gpf.GetText(),Structure="Dependency")
    gpf.AddGridJS(DepStruct)
    Seg=gpf.Parse(gpf.GetText(),Structure="Segment")
    gpf.AddGridJS(Seg)
    gpf.CallTable("Co_Event")
    gpf.CallFSA("CoEvent")
    PrintUnit(gpf)

def Test_Main():
    Idx_GPF("CoEvent")
    Test_CoEvent()

def BCC_Corpus1():
    gpf=GPF()
    IN=open("./Examples/BuildBCC/Corpus.txt","r")    
    Out=open("./Examples/BuildBCC/treebank.txt","w")
    Num=0
    for Line in IN:
        Num+=1;
        Tree=gpf.Parse(Line.strip(),Structure="Tree")
        try:
            Ret=json.loads(Tree.replace('\\','\\\\'),strict=True)
        except:
            continue
        if Ret.get("Units") and len(Ret["Units"]) >0:
            print(json.loads(Tree)["Units"][0],file=Out)
        if Num%50 == 0:
            print("processing:",Num,end="\r")
            
    IN.close()
    Out.close()

def BCC_Corpus2():
    CorpusIn="./Examples/BuildBCC/treebank.txt"
    CorpusOut="./Examples/BuildBCC/treebankEx.txt"
    IN=open(CorpusIn,"r")    
    Out=open(CorpusOut,"w")
    Num=0
    No=0
    for Line in IN:
        Line=Line.strip()
        if Num%100 == 0:
            print("Table %dParts"%No,file=Out)
            print("#Global ID=%d"%No,file=Out)
            No+=1
        Num+=1;
        print("Item:%s"%Line,file=Out)
    IN.close()
    Out.close()

    

def BCC_Lua2():
    gpf = GPF()
    Query='''
Handle0=GetAS("$NP-SBJ","","","","","~","","","","0,1")
Handle1=GetAS("击>","打击")
Handle3=JoinAS(Handle0,Handle1,"*")
Handle4=Freq(Handle3,"$1")
Ret=Output(Handle4,1000)
return Ret'''
    Ret=gpf.BCC(Query,Service="BCC")
    print(Ret)
    

def Test():
    gpf = GPF()
    Files=["D:/Xunendong/GPF/Src/pysetup/gpflib/Examples/BuildBCC/Tree.txt"]
    Ret=gpf.IndexBCC(Files)
    

def Test2():
    gpf = GPF()
    Ret=gpf.GetTable()
    for I in Ret:
        print(I)
        Items=gpf.GetTableItem(I)
        for It in Items:
            KV=gpf.GetTableItemKV(I,It)
            print(KV)
            for K,V in KV.items():
                print(K,"".join(V))    
        
def Test3():
    gpf = GPF()
    In=open("./Examples/BuildBCC/Corpus.txt","r")
    Out=open("./Examples/BuildBCC/CorpusEx.txt","w")
    Num=0
    for S in In:
        Ret=gpf.Parse(S.strip())
        Ret=json.loads(Ret)
        Ret=" ".join(Ret["Units"])
        if Num%1000 == 0:
            print(Num)
            print(Ret)
        print(Ret,file=Out)    
        Num+=1 
    In.close()
    Out.close()
           
def Test5():
    In=open("./Examples/BuildBCC/Corpus.txt","r")
    Num=0
    for S in In:
        Ret=jieba.lcut(S)
        if Num%2000 == 0:
            print(Num,Ret)
        Num+=1 
    In.close()

def Test6():
    gpf = GPF()   
    In=open("word.txt","r",encoding="utf-8")
    for L in In:
        L=L.strip()
        Array=L.split("\t")
        if len(Array) > 1 :
            Ret=gpf.BCC(Array[0],Command="Freq",Service="BCC")
            print(Ret)
            
    In.close()

def Test7():
    gpf = GPF()   
    Ret=gpf.BCC("(a)的",Command="Freq",Target="$1",WinSize=30)
    print(Ret)

def Parse1():
    Line="我们大家今天下午在邵逸夫操场集合"
    gpf=GPF()
    Ret=gpf.Parse(Line,Structure="Tree")
    gpf.AddGridJS(Ret)
    gpf.Show()

def ShowPng():
	Line="我们大家今天下午在邵逸夫操场集合"
	gpf=GPF()
	Ret=gpf.Parse(Line,Structure="ChunkDep")
	gpf.Show(Json=Ret,IsShowGrid=False)

def DrawGrid(): 
    Line="我们大家今天下午在邵逸夫操场集合"
    gpf=GPF()
    Ret=gpf.Parse(Line,Structure="Tree")
    gpf.AddGridJS(Ret)
    gpf.Show()

def Test11():
    gpf = GPF()
    Ret=gpf.BCC("a的人",Service="hskjc")
    print(Ret)    

def TestGrid():
    gpf = GPF()
    Text = '我在北京语言大学读书。'
    TreeRet = gpf.Parse(Text,Structure='Tree') 
    gpf.Show(Json=TreeRet,IsShowGrid=False)
    Ret=gpf.GetGridKV()
    for K,Vs in Ret.items():
        print(K,"="," ".join(Vs))

    Ret=gpf.GetGrid()
    for Col in Ret:
        for U in Col:
            Ret=gpf.GetUnitKV(U)
            print("==>",gpf.GetUnitKV(U,"Word"))
            for K,Vs in Ret.items():
                print(K,"="," ".join(Vs))


    Ret=gpf.GetRelation()
    for R in Ret:
            Ret=gpf.GetRelationKV(R["U1"],R["U2"],R["R"])
            for K,Vs in Ret:
                print(K,"="," ".join(Vs))

def TestShow():
    gpf = GPF()
    Text = '我在北京语言大学读书。'
    gpf.SetGridText(Text)
    gpf.Show()

def IdxTable():
    gpf = GPF()
    Ret=gpf.IndexTable("./Examples/Dict/org/gpf.tab")

def testTable():
    gpf = GPF()
    Ret=gpf.GetTableItemKV("Dict","6")
    for K,Vs in Ret.items():
        print(K,end=" ")
        for V in Vs:
            print(V,end=" ")
        print("")

def Thread():
    gpf=GPF()
    Ret=gpf.Parse("大家好")
    print(Ret)
	
def TestThread():
	threads = []
	for i in  range(10):
		t = threading.Thread(target=Thread,args=())
		threads.append(t)
		t.start()
		
	for t in threads:
		t.join()

	print("Over!")		

def Bcc():
    gpf = GPF()
    gpf.AddBCCKV("AA","灵怪;疏松;愚笨")
    gpf.AddBCCKV("AA1","灵怪;疏松;愚笨")
    print("1")
    Ret=gpf.BCC("(a)的{$1=[AA]}",Command="Freq",Number=200000)
    print(Ret)
    print("2")
    Ret=gpf.BCC("(a)的{$1=[AA]}",Command="Freq",Number=200000)
    print(Ret)

def Parsing(Sent,Cat,ShowGrid):
    gpf=GPF()
    Ret=gpf.Parse(Sent,Structure=Cat)
    print(Ret)
    
'''
Json='{"S":[{"NP":[{"r":"我们"},{"n":"大家"}]},{"VP":{"v":"喜欢"}}]}'
Json='[[["我们1","大家1"],"喜欢1"],["我们","大家","喜欢"]]'
Json='{"S":[{"NP":[{"r":"我们"},{"n":"大家"}]},{"VP":{"v":"喜欢"}}]}'
Json='[{"NP":[{"r":"我们"},{"n":"大家"}]},{"VP":{"v":"喜欢"}}]'
Json='[["Root","带来了","Pred"],["Root","成为","Pred"],["带来了", "前说未有的机遇和挑战","obj"],["带来了", "人工智能","sbj"],["带来了", "为我们","mod"],["成为", "人工智能","sbj"],["成为", "重要发展方向","obj"],["成为", "已经","mod"]]'
Json='["我们","大家","喜欢"]'
Json='{"Root":{"Pred":["带来了","成为"]},"带来了":{"sbj":"人工智能","obj":"机遇","mod":["已经","可见的"]},"成为":{"sbj":"人工智能","obj":"方向"}}'
gpf.SetText("人工智能为我们带来了前说未有的机遇和挑战，已经成为重要发展方向")
Json='{"Root":[["带来了","Pred"],["成为","Pred"]],"带来了":[["人工智能","sbj"],["机遇","obj"],["已经","mod"],["相当多","mod"]],"成为":{"sbj":"人工智能","obj":"方向"},"机遇":[[{"K":1},{"K1":2}]]}'
gpf.Show(Json)
'''

Sent='["我们/r","大家/n","喜欢/v"]'
Sent='[{"我们":{"A":1}},"大家","喜欢/v"]'
Sent='{"我们":["A","A"],"大家":["A","A"],"喜欢":["A","A"]}'
Sent='["我在","北语/Loc","读计算机专业"]'
Sent='{"发展":140,"经济":70,"推进":66,"建设":63,"加强":53,"支持":52,"保障":50,"稳定":49,"完善":48,"就业":40,"增长":39,"国家":38,"人民":30}'
Sent='{"S":[{"NP":[{"r":"我们"},{"r":"大家"}]},{"NP":{"v":"喜欢"}}]}'
Sent='{"张三":{"年龄":"22","性别":"男","教育信息":{"学历":"本科","专业":"计算机"}},"李四":{"年龄":"26","性别":"男","教育信息":{"学历":"硕士","专业":"汉语国际教育","教育信息":{"学历":"硕士","专业":"汉语国际教育"}}}}'
Sent='{"学习":[["我","主语"],["在","mod"]]}'
Sent='{"张三":{"年龄":22,"性别":"男","教育信息":{"学历":"本科","专业":"计算机"}},"李四":{"年龄":26,"性别":"男","教育信息":{"学历":"硕士","专业":"汉语国际教育"}}}'


gpf=GPF()

Text="饭孩子们都吃完了"
Text="饭孩子们都吃光了"

Text="孩子们都吃撑了"
gpf.SetText(Text)
Child=gpf.AddUnit(2,"孩子们")
All=gpf.AddUnit(3,"都")
Eat=gpf.AddUnit(4,"吃")
Full=gpf.AddUnit(6,"撑了")

gpf.AddUnitKV(Eat,"POS","V")
gpf.AddUnitKV(Full,"POS","V")

gpf.AddRelation(Eat,All,"mod")
gpf.AddRelation(Eat,Full,"mod")
gpf.AddRelation(Eat,Child,"sbj")
gpf.AddRelation(Full,Child,"sbj")
gpf.AddRelationKV(Full,Child,"sbj","K1","V1")
gpf.AddRelationKV(Full,Child,"sbj","K2","V2")
R=gpf.GetRelation()

for r in R:
    print(gpf.GetUnitKV(r["Head"],"Word"),gpf.GetUnitKV(r["Sub"],"Word"),r["Relation"])
    KVs=gpf.GetRelationKV(r["Head"],r["Sub"],r["Relation"])
    for K,Vs in KVs.items():
        Val=" ".join(Vs)    
        print(K+"="+Val)
