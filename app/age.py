def test():
    m = int(input("First year? "))
    j = int(input("Second year? "))

    while m != j:
        m = m + 2
        j = j + 1

        print(m, j)

test()