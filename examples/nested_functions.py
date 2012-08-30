def bar(a):
    def car(b):
        def sitar(a, c):
            print a, b, c
        print b
        sitar(a+b, a)
    car(a*2)

bar(9)
