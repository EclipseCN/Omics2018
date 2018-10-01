#前向算法
import numpy as np
A=[[0,1,0,0],[0.4,0,0.6,0],[0,0.4,0,0.6],[0,0,0.5,0.5]]
B=[[0.5,0.5],[0.3,0.7],[0.6,0.4],[0.8,0.2]]
pi=[0.25,0.25,0.25,0.25]
Seq_out=[0,0,1,1,0]
def forward_algo(A,B,pi,Seq_out):
    memo=[[None]*len(Seq_out) for i in range(len(B))]
    for i in range(len(B)):
        memo[i][0]=pi[i]*B[i][Seq_out[0]]
    for i in range(1,len(Seq_out)):
        for j in range(len(B)):
            sumNum=0
            for k in range(len(B)):
                sumNum+=memo[k][i-1]*A[k][j]
            sumNum*=B[j][Seq_out[i]]
            memo[j][i]=sumNum
    sumPrint=0
    for i in range(len(B)):
        sumPrint+=memo[i][-1]
    return(memo,sumPrint)
forward_algo(A,B,pi,Seq_out)



#后向算法
def backward_algo(A,B,pi,Seq_out):
    memo=[[None]*len(Seq_out) for i in range(len(B))]
    for i in range(len(B)):
        memo[i][0]=1
    for i in range(1,len(Seq_out)):
        for j in range(len(B)):
            sumNum=0
            for k in range(len(B)):
                sumNum+=memo[k][i-1]*A[j][k]*B[k][Seq_out[len(Seq_out)-i]]
            memo[j][i]=sumNum

    sumNum=0
    for i in range(len(B)):
        sumNum+=pi[i]*B[i][Seq_out[0]]*memo[i][-1]
    return(memo,sumNum)
backward_algo(A,B,pi,Seq_out)


#计算给定模型和序列时在时刻t状态为i的概率
def calcGamma(t,i,A,B,pi,Seq_out):
    memo_f=forward_algo(A,B,pi,Seq_out)[0]
    memo_b=backward_algo(A,B,pi,Seq_out)[0]
    fenzi=memo_f[i][t-1]*memo_b[i][len(Seq_out)-t]
    fenmu=0
    for j in range(len(B)):
        fenmu+=memo_f[j][t-1]*memo_b[j][len(Seq_out)-t]
    return(fenzi/fenmu)
	
	
#计算给定模型和序列时在t时刻状态为i，t+1时刻状态为j的概率	
def calcDelta(t,i,j,A,B,pi,Seq_out):
    memo_f=forward_algo(A,B,pi,Seq_out)[0]
    memo_b=backward_algo(A,B,pi,Seq_out)[0]
    fenzi=memo_f[i][t-1]*memo_b[j][len(Seq_out)-t-1]*A[i][j]*B[j][Seq_out[t]]
    fenmu=0
    for idx_i in range(len(B)):
        for idx_j in range(len(B)):
            fenmu+=memo_f[idx_i][t-1]*memo_b[idx_j][len(Seq_out)-t-1]*A[idx_i][idx_j]*B[idx_j][Seq_out[t]]
    return(fenzi/fenmu)
	
	
#隐马尔科夫模型的学习问题
def B_W_algo(O,A,B,pi):
    L=len(O)
    for o in O:
        fenmu_arr_A=[None]*len(B)
        fenmu_arr_B=[None]*len(B)
        fenzi_mat_A=[[None]*len(B) for i in range(len(B))]
        fenzi_mat_B=[[None]*len(B[0]) for i in range(len(B))]
        pi_state=[None]*len(B)
        for state in range(len(B)):
            fenmu_A=0
            fenmu_B=0
            pi_state[state]=calcGamma(1,state,A,B,pi,o)
            for t in range(1,len(o)):
                fenmu_A+=calcGamma(t,state,A,B,pi,o)
                fenmu_B+=calcGamma(t,state,A,B,pi,o)
            fenmu_arr_A[state]=fenmu_A
            fenmu_arr_B[state]=fenmu_B+calcGamma(len(o),state,A,B,pi,o)
            for state2 in range(len(B)):
                fenzi_A=0
                for t in range(1,len(o)):
                    fenzi_A+=calcDelta(t,state,state2,A,B,pi,o)
                fenzi_mat_A[state][state2]=fenzi_A
            for k in range(len(B[0])):
                fenzi_B=0
                for t in range(1,len(o)+1):
                    if o[t-1]==k:
                        fenzi_B+=calcGamma(t,state,A,B,pi,o)
                fenzi_mat_B[state][k]=fenzi_B
        for state in range(len(B)):
            for state2 in range(len(B)):
                A[state][state2]=fenzi_mat_A[state][state2]/fenmu_arr_A[state]
        for state in range(len(B)):
            for k in range(len(B[0])):
                B[state][k]=fenzi_mat_B[state][k]/fenmu_arr_B[state]
        for i in range(len(pi_state)):
            pi[i]=pi_state[i]
    return(A,B,pi)
	
	
	
#解码问题，给定观测序列和模型，试给出状态序列
def Viterbi(A,B,pi,Seq_out):
    memo=[[[None,None] for i in range(len(Seq_out))] for i in range(len(B))]
    for i in range(len(B)):
        memo[i][0][0]=pi[i]*B[i][Seq_out[0]]
    for i in range(1,len(Seq_out)):
        for state in range(len(B)):
            current_max=-1
            current_idx=-1
            for j in range(len(B)):
                if memo[j][i-1][0]*A[j][state]>current_max:
                    current_max=memo[j][i-1][0]*A[j][state]
                    current_idx=j
            memo[state][i][0]=current_max*B[state][Seq_out[i]]
            memo[state][i][1]=current_idx
    finalMax=-1
    finalState=-1
    res=[]
    for i in range(len(B)):
        if memo[i][-1][0]>finalMax:
            finalMax=memo[i][-1][0]
            finalState=i
    #假设只给出一条最大可能状态序列
    res.append(finalState)
    for i in range(len(Seq_out)-1,0,-1):
        res.append(memo[finalState][i][1])
        finalState=memo[finalState][i][1]
    return(res[::-1])
	
#test
A=[[0.99,0.01],[0.2,0.8]]
B=[[1/6,1/6,1/6,1/6,1/6,1/6],[1/10,1/10,1/10,1/10,1/10,1/2]]
pi=[0.5,0.5]
Seq_out=[3,1,5,1,1,6,2,4,6,4,4,6,6,4,4,2,4,5,3,2,1,1,3,1,6,3,1,1,6,4,1,5,2,1,3,3,6,2,5,1,4,4,5,4,3,6,3,1,6,5,6,6,2,6,5,6,6,6,6,6]
for i in range(len(Seq_out)):
    Seq_out[i]=Seq_out[i]-1
print(Viterbi(A,B,pi,Seq_out))