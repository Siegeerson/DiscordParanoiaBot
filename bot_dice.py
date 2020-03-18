print()
def adddice(out,r):
    if not out:
        out = [""]*5
    C='o '
    out[0]+="-------  "
    out[1]+="| "+C[r<1]+" "+C[r<3]+" |  "
    out[2]+="| "+C[r<5]+C[r&1]+C[r<5]+" |  "
    out[3]+="| "+C[r<3]+" "+C[r<1]+" |  "
    out[4]+="-------  "
    return out

out = [""]*5

for x in range(10):
    out = adddice(out,x%6)

for x in out:
    print(x)
out = []
for x in range(5,-1,-1):
    out = adddice(out,x)

print("\n".join(out))


def rolln_dice(n=5):
    out=[]
    for x in range(n):
        out=adddice(out)
    
