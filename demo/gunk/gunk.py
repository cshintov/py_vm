def gunk(a=1, b=3, *args):
    print(args)
    c = 5
    return (a + b, c)

print(gunk(2, 4, 10, 11))
