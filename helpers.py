def salting(password):
    iter=0
    passwd=[]
    for c in password:
        iter +=1 
        passwd.append(c)
        if iter %2 ==0:
            passwd.append('$$')
    return ''.join(passwd)