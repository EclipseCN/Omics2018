c=[1,3,7]
def RecursiveChange(M,c,d):
    if M==0:
        return(0);
    bestNumCoins=10000
    for i in range(d):
        if M>=c[i]:
            numCoins=RecursiveChange(M-c[i],c,d)
            if numCoins+1<bestNumCoins:
                bestNumCoins=numCoins+1
    return(bestNumCoins)

print(RecursiveChange(40,c,3))



def DynamicChange(M):
    c=[1,3,4]
    d=len(c)
    memo=[None]*(M+1)
    memo[0]=0
    for m in range(1,M+1):
        bestNumCoins=10000
        for i in range(d):
            if m>=c[i]:
                if memo[m-c[i]]+1<bestNumCoins:
                    bestNumCoins=memo[m-c[i]]+1
        memo[m]=bestNumCoins
    return(memo[-1])
print(DynamicChange(98))