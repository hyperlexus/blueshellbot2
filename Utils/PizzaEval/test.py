# all hail test.py
def der_neger(a):
    while a.startswith(" "):
        a = a[1:]
    while a.endswith(" "):
        a = a[:-1]
    return a


n = "   mein cock ist 40cm lang        "

print(der_neger(n) == n.strip())  # True
