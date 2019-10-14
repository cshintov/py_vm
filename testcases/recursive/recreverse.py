def reverse(num, acm):
    if num / 10 == 0:
        return acm * 10 + num
    rem = num % 10
    return reverse(num / 10, acm * 10 + rem)

print 543
print reverse(543, 0)
