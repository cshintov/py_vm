def hcf(a, b):
    if a < b:
        return hcf(a, b - a)
    elif a > b:
        return hcf(a - b, b)
    else:
        return a
def lcm(a, b):
    return a *  b / hcf(a, b)
print 16
print 40
print hcf(16, 40)
print lcm(16, 40)
print 16
print 24
print hcf(16, 24)
print lcm(16, 24)
print 5
print 3
print hcf(5, 3)
print lcm(5, 3)

