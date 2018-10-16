#这是用于序列比对的code
#尝试是否可以使用合作模式
def alignment(str1,str2):
    m=len(str1)
    n=len(str2)
    arr=[[None]*(m+1) for i in range(n+1)]
    for i in range(m+1):
        arr[0][i]=0
    for i in range(n+1):
        arr[i][0]=0
    for i in range(1,n+1):
        for j in range(1,m+1):
            maxLength=-1
            if arr[i-1][j]>maxLength:
                maxLength=arr[i-1][j]
            if arr[i][j-1]>maxLength:
                maxLength=arr[i][j-1]
            if str1[i-1]==str2[j-1]:
                maxLength=arr[i-1][j-1]+1
            arr[i][j]=maxLength
    print(arr[n][m])
def printMat(arr):
    m=len(arr)
    for i in range(m):
        print(arr[i])
str1="TAGAATGCGG"
str2="TCGTAGACGA"
alignment(str1,str2)
# printMat(arr)
            
			
			

import numpy as np
def global_score(str1,str2):
    n=len(str1)
    m=len(str2)
    arr=[[None]*(m+1) for i in range(n+1)]
    gaps_i=[[False]*(m+1) for i in range(n+1)]
    gaps_j=[[False]*(m+1) for i in range(n+1)]
    directions=[[[] for j in range(m+1)] for i in range(n+1)]
    arr[0][0]=0
    arr[0][1]=-2
    arr[1][0]=-2
    for i in range(2,m+1):
        arr[0][i]=arr[0][i-1]-1
    for i in range(2,n+1):
        arr[i][0]=arr[i-1][0]-1
    for i in range(1,n+1):
        for j in range(1,m+1):
            score=-float("inf")
            if str1[i-1]==str2[j-1] and arr[i-1][j-1]+1>score:
                score=arr[i-1][j-1]+1
            if str1[i-1]!=str2[j-1] and arr[i-1][j-1]-1>score:
                score=arr[i-1][j-1]-1
            if arr[i-1][j]-2>score:
                score=arr[i-1][j]-2
            if arr[i][j-1]-2>score:
                score=arr[i][j-1]-2
            if gaps_i[i-1][j]==True and arr[i-1][j]-1>score:
                score=arr[i-1][j]-1
            if gaps_j[i][j-1]==True and arr[i][j-1]-1>score:
                score=arr[i][j-1]-1
            if score==arr[i-1][j]-2:
                gaps_i[i][j]=True
            if score==arr[i][j-1]-2:
                gaps_j[i][j]=True
            if gaps_i[i-1][j]==True and arr[i-1][j]-1==score:
                gaps_i[i][j]=True
            if gaps_j[i][j-1]==True and arr[i][j-1]-1==score:
                gaps_j[i][j]=True
            if str1[i-1]==str2[j-1] and arr[i-1][j-1]+1==score:
                directions[i][j].append("\\")
            if str1[i-1]!=str2[j-1] and arr[i-1][j-1]-1==score:
                directions[i][j].append("\\")
            if gaps_i[i][j]==True and gaps_i[i-1][j]==True:
                directions[i][j].append("(|)")
            if gaps_j[i][j]==True and gaps_j[i][j-1]==True:
                directions[i][j].append("(—)")
            if gaps_i[i][j]==True and gaps_i[i-1][j]==False:
                directions[i][j].append("|")
            if gaps_j[i][j]==True and gaps_j[i][j-1]==False:
                directions[i][j].append("—")
            arr[i][j]=score
    return(np.array(arr),directions)
    
def printDirections(directions):
    for item in directions:
        printStr=""
        for subItem in item:
            printSubStr=""
            for subSubItem in subItem:
                printSubStr+=str(subSubItem)
            printStr+="%8s" % (printSubStr)
        print(printStr)
        print()
        print()
def printMat(arr):
    m=len(arr)
    for i in range(m):
        print(arr[i])
        
def printRes(i,j,directions,sequence,idx,orient,res,string="",flag_h=False,flag_v=False):
    lastResLst=directions[i][j]
    if len(lastResLst)==0:
        for index in range(idx,-1,-1):
            string+=sequence[index]
        res.append(string[::-1])
    if flag_h==False and flag_v==False:
        for item in lastResLst:
            if item=="\\":
                string+=sequence[idx]
                printRes(i-1,j-1,directions,sequence,idx-1,orient,res,string)
            elif item=="|":
                if orient=="v":
                    string+=sequence[idx]
                    printRes(i-1,j,directions,sequence,idx-1,orient,res,string)
                elif orient=="h":
                    string+="—"
                    printRes(i-1,j,directions,sequence,idx,orient,res,string)
            elif item=="—":
                if orient=="v":
                    string+="—"
                    printRes(i,j-1,directions,sequence,idx,orient,res,string)
                elif orient=="h":
                    string+=sequence[idx]
                    printRes(i,j-1,directions,sequence,idx-1,orient,res,string)
            elif item=="(—)":
                if orient=="v":
                    string+="—"
                    printRes(i,j-1,directions,sequence,idx,orient,res,string,True,False)
                elif orient=="h":
                    string+=sequence[idx]
                    printRes(i,j-1,directions,sequence,idx-1,orient,res,string,True,False)
            elif item=="(|)":
                if orient=="v":
                    string+=sequence[idx]
                    printRes(i-1,j,directions,sequence,idx-1,orient,res,string,False,True)
                elif orient=="h":
                    string+="—"
                    printRes(i-1,j,directions,sequence,idx,orient,res,string,False,True)     
            string=string[:-1]
    elif flag_h==True and flag_v==False:
        for item in lastResLst:
            if item=="—":
                if orient=="v":
                    string+="—"
                    printRes(i,j-1,directions,sequence,idx,orient,res,string)
                elif orient=="h":
                    string+=sequence[idx]
                    printRes(i,j-1,directions,sequence,idx-1,orient,res,string)
            elif item=="(—)":
                if orient=="v":
                    string+="—"
                    printRes(i,j-1,directions,sequence,idx,orient,res,string,True,False)
                elif orient=="h":
                    string+=sequence[idx]
                    printRes(i,j-1,directions,sequence,idx-1,orient,res,string,True,False)
    elif flag_h==False and flag_v==True:
        for item in lastResLst:
            if item=="|":
                if orient=="v":
                    string+=sequence[idx]
                    printRes(i-1,j,directions,sequence,idx-1,orient,res,string)
                elif orient=="h":
                    string+="—"
                    printRes(i-1,j,directions,sequence,idx,orient,res,string)
            elif item=="(|)":
                if orient=="v":
                    string+=sequence[idx]
                    printRes(i-1,j,directions,sequence,idx-1,orient,res,string,False,True)
                elif orient=="h":
                    string+="—"
                    printRes(i-1,j,directions,sequence,idx,orient,res,string,False,True)
    else:
        print("this is impossible!")
    return(res)
def global_alignment():
    str1=input("plz enter the first sequence").upper()
    str2=input("plz enter the second sequence").upper()
    arr,directions=global_score(str1,str2)
    flag1=input("Do u want to show the score Mat? yes/no")
    if flag1=="yes":
        print(arr)
    flag1=input("Do u want to show the direction Mat? yes/no")
    if flag1=="yes":
        printDirections(directions)
    str1_res=printRes(-1,-1,directions,str1,len(str1)-1,"v",[])
    str2_res=printRes(-1,-1,directions,str2,len(str2)-1,"h",[])
    num=len(str1_res)
    print("we have "+str(num)+" ans")
    idx=int(input("please choose which one?"))
    str1_fix=("%"+str(max(len(str1_res[idx-1]),len(str2_res[idx-1])))+"s") % (str1_res[idx-1])
    str2_fix=("%"+str(max(len(str1_res[idx-1]),len(str2_res[idx-1])))+"s") % (str2_res[idx-1])
    inter_line=""
    for i,j in zip(str1_fix,str2_fix):
        if i!=" " and i!="—" and j!=" " and j!="—":
            inter_line+="|"
        else:
            inter_line+=" "
    flag1=input("Do u want to show the alignment result?")
    if flag1=="yes":
        print(str1_fix)
        print(inter_line)
        print(str2_fix)
		
		

		
import numpy as np
def local_score(str1,str2):
    n=len(str1)
    m=len(str2)
    arr=[[None]*(m+1) for i in range(n+1)]
    gaps_i=[[False]*(m+1) for i in range(n+1)]
    gaps_j=[[False]*(m+1) for i in range(n+1)]
    directions=[[[] for j in range(m+1)] for i in range(n+1)]
    for i in range(m+1):
        arr[0][i]=0
    for i in range(n+1):
        arr[i][0]=0
    for i in range(1,n+1):
        for j in range(1,m+1):
            score=-float("inf")
            if str1[i-1]==str2[j-1] and arr[i-1][j-1]+1>score:
                score=arr[i-1][j-1]+1
            if str1[i-1]!=str2[j-1] and arr[i-1][j-1]-1>score:
                score=arr[i-1][j-1]-1
            if arr[i-1][j]-2>score:
                score=arr[i-1][j]-2
            if arr[i][j-1]-2>score:
                score=arr[i][j-1]-2
            if gaps_i[i-1][j]==True and arr[i-1][j]-1>score:
                score=arr[i-1][j]-1
            if gaps_j[i][j-1]==True and arr[i][j-1]-1>score:
                score=arr[i][j-1]-1
            score=max(score,0)
            if score==arr[i-1][j]-2:
                gaps_i[i][j]=True
            if score==arr[i][j-1]-2:
                gaps_j[i][j]=True
            if gaps_i[i-1][j]==True and arr[i-1][j]-1==score:
                gaps_i[i][j]=True
            if gaps_j[i][j-1]==True and arr[i][j-1]-1==score:
                gaps_j[i][j]=True
            if str1[i-1]==str2[j-1] and arr[i-1][j-1]+1==score:
                directions[i][j].append("\\")
            if str1[i-1]!=str2[j-1] and arr[i-1][j-1]-1==score:
                directions[i][j].append("\\")
            if gaps_i[i][j]==True and gaps_i[i-1][j]==True:
                directions[i][j].append("(|)")
            if gaps_j[i][j]==True and gaps_j[i][j-1]==True:
                directions[i][j].append("(—)")
            if gaps_i[i][j]==True and gaps_i[i-1][j]==False:
                directions[i][j].append("|")
            if gaps_j[i][j]==True and gaps_j[i][j-1]==False:
                directions[i][j].append("—")
            arr[i][j]=score
    return(arr,directions)
def printMat(arr):
    m=len(arr)
    for i in range(m):
        print(arr[i])
def printRes4Local(i,j,arr,directions,sequence,idx,orient,res,string="",flag_h=False,flag_v=False):
    lastResLst=directions[i][j]
    if arr[i][j]==0:
        res.append(string[::-1])
        res.append(idx)
    if flag_h==False and flag_v==False:
        for item in lastResLst:
            if item=="\\":
                string+=sequence[idx]
                printRes4Local(i-1,j-1,arr,directions,sequence,idx-1,orient,res,string)
            elif item=="|":
                if orient=="v":
                    string+=sequence[idx]
                    printRes4Local(i-1,j,arr,directions,sequence,idx-1,orient,res,string)
                elif orient=="h":
                    string+="—"
                    printRes4Local(i-1,j,arr,directions,sequence,idx,orient,res,string)
            elif item=="—":
                if orient=="v":
                    string+="—"
                    printRes4Local(i,j-1,arr,directions,sequence,idx,orient,res,string)
                elif orient=="h":
                    string+=sequence[idx]
                    printRes4Local(i,j-1,arr,directions,sequence,idx-1,orient,res,string)
            elif item=="(—)":
                if orient=="v":
                    string+="—"
                    printRes4Local(i,j-1,arr,directions,sequence,idx,orient,res,string,True,False)
                elif orient=="h":
                    string+=sequence[idx]
                    printRes4Local(i,j-1,arr,directions,sequence,idx-1,orient,res,string,True,False)
            elif item=="(|)":
                if orient=="v":
                    string+=sequence[idx]
                    printRes4Local(i-1,j,arr,directions,sequence,idx-1,orient,res,string,False,True)
                elif orient=="h":
                    string+="—"
                    printRes4Local(i-1,j,arr,directions,sequence,idx,orient,res,string,False,True)
    elif flag_h==True and flag_v==False:
        for item in lastResLst:
            if item=="—":
                if orient=="v":
                    string+="—"
                    printRes4Local(i,j-1,arr,directions,sequence,idx,orient,res,string)
                elif orient=="h":
                    string+=sequence[idx]
                    printRes4Local(i,j-1,arr,directions,sequence,idx-1,orient,res,string)
            elif item=="(—)":
                if orient=="v":
                    string+="—"
                    printRes4Local(i,j-1,arr,directions,sequence,idx,orient,res,string,True,False)
                elif orient=="h":
                    string+=sequence[idx]
                    printRes4Local(i,j-1,arr,directions,sequence,idx-1,orient,res,string,True,False)
    elif flag_h==False and flag_v==True:
        for item in lastResLst:
            if item=="|":
                if orient=="v":
                    string+=sequence[idx]
                    printRes4Local(i-1,j,arr,directions,sequence,idx-1,orient,res,string)
                elif orient=="h":
                    string+="—"
                    printRes4Local(i-1,j,arr,directions,sequence,idx,orient,res,string)
            elif item=="(|)":
                if orient=="v":
                    string+=sequence[idx]
                    printRes4Local(i-1,j,arr,directions,sequence,idx-1,orient,res,string,False,True)
                elif orient=="h":
                    string+="—"
                    printRes4Local(i-1,j,arr,directions,sequence,idx,orient,res,string,False,True)
    else:
        print("this is impossible!")
    return(res)
def local_alignment():
    str1=input("plz enter the first sequence").upper()
    str2=input("plz enter the second sequence").upper()
    arr,directions=local_score(str1,str2)
    flag1=input("Do u want to show the score Mat? yes/no")
    if flag1=="yes":
        print(np.array(arr))
    flag1=input("Do u want to show the direction Mat? yes/no")
    if flag1=="yes":
        printDirections(directions)
    maxNum=0
    i_idx=0
    j_idx=0
    for i in range(len(arr)):
        if max(arr[i])>maxNum:
            maxNum=max(arr[i])
            i_idx=i
            j_idx=arr[i].index(max(arr[i]))
    str1Local=printRes4Local(i_idx,j_idx,arr,directions,str1,i_idx-1,"v",[])
    str2Local=printRes4Local(i_idx,j_idx,arr,directions,str2,j_idx-1,"h",[])
    seq1=str1Local[0]
    seq2=str2Local[0]
    inter_line=""
    for x,y in zip(seq1,seq2):
        if x!="—" and y!="—":
            inter_line+="|"
        else:
            inter_line+=" "
    site1=str1Local[1]
    site2=str2Local[1]
    addLeft1=str1[:site1+1]
    addLeft2=str2[:site2+1]
    if site1>=site2:
        addLeft2=" "*(site1-site2)+addLeft2
        inter_line=" "*(site1+1)+inter_line
    else:
        addLeft1=" "*(site2-site1)+addLeft1
        inter_line=" "*(site2+1)+inter_line
    addRight1=str1[(i_idx):]
    addRight2=str2[(j_idx):]
    addRight1L=len(addRight1)
    addRight2L=len(addRight2)
    if addRight1L>=addRight2L:
        addRight2+=" "*(addRight1L-addRight2L)
    else:
        addRight1+=" "*(addRight2L-addRight1L)
    seq1=addLeft1+seq1+addRight1
    seq2=addLeft2+seq2+addRight2
    flag1=input("Do u want to show the alignment result?")
    if flag1=="yes":
        print(seq1)
        print(inter_line)
        print(seq2)