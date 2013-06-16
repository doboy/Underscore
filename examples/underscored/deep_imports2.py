#  def foo():
#      import logging.handlers
#      print dir(logging.handlers)
#      print 2
#  
#  class bar():
#      import logging.handlers
#      print dir(logging.handlers)
#      print 1
#  
#      @staticmethod
#      def far():
#          import logging.handlers
#          print dir(logging.handlers)
#          print 3
#  
#  foo()
#  bar().far()

(_________, __________, ___________) = (2, 1, 3)
(_______, ________) = (dir, staticmethod)

def _():
    import logging.handlers
    (__,) = (logging,)
    print _______(__.handlers)
    print _________


class ___:
    import logging.handlers
    (____,) = (logging,)
    print _______(____.handlers)
    print __________

    @________
    def _____():
        import logging.handlers
        (______,) = (logging,)
        print _______(______.handlers)
        print ___________
    (far, logging) = (_____, ____)
_()
___().far()
(bar, foo) = (___, _)
