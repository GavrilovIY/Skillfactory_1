def iter(a,b):
    for i in range(b):
        yield a+0.1*i

for i in iter(1,5):
    print(i)