f=open("urls.txt","r")
f2=open("unique-url.txt","w")
lines=list(set(f.readlines()))
for line in lines:
    f2.write(line)