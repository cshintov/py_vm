#computes lcm and hcf of x and y

x = 16
y = 40
a = x;
b = y;

while (b != 0):
    t = b;
    b = a % b;
    a = t;

gcd = a;
lcm = (x*y)/gcd;

print gcd
print lcm


