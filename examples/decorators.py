def d1(func):
    print('hi')
    return func

def d2(word):
    print(word
    def decor(func):
        print('hello')
        return func
    return decor

@d1
@d2('test')
def d3():
    print('yo')

d3()
