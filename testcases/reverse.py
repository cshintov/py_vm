# computes the reverse of the number
num = 1234
reverse = 0

if num < 0:
    sign = -1
else:
    sign = 1
num = num * sign
while num > 0:
    rem = num % 10
    reverse = reverse * 10 + rem
    num = num / 10

reverse = reverse * sign
print reverse
