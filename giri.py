n = int(input())
for i in range(1,n+1):
    space = i*"  "
    star = (n-i)*"* "
    print(space+star)
    