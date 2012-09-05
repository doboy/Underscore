class a:
    def do(self):
        print 'a'
        return self

class b:
    def run(self):
        print 'b'
        return self

class c(a, b):
    pass

c().do().run()
    
