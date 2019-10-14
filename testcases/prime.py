# checks whether num is prime; 1 for prime and 0 for not prime

num = 5

res = 1

div = num - 1

while div > 1:
    if num % div == 0:
        res = 0
    div = div - 1

print res
