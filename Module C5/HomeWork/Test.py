def recurs(num):
    if len(num)==0:
        return ''
    else:
        return num[-1]+recurs(num[:-1])


c = 0.9877654



b = str(c)

print(float(b[0]+'.'+recurs(b.split('.')[1])))

#b = 0.4567789




