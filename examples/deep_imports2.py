def foo():
    import logging.handlers
    print(dir(logging.handlers))
    print(2)

class bar():
    import logging.handlers
    print(dir(logging.handlers))
    print(1)

    @staticmethod
    def far():
        import logging.handlers
        print(dir(logging.handlers))
        print(3)

foo()
bar().far()
