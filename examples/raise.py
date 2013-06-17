try:
    raise AssertionError, 'this is a test', 'xx'
except:
    print('test passed')
