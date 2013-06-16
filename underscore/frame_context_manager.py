class FrameContextManager(object):

    def __init__(self, frame, visitor):
        self.frame = frame
        self.visitor = visitor

    def __enter__(self):
        self.visitor.current_frame = self.frame
        return self.frame

    def __exit__(self, *_):
        self.visitor.withdraw_frame()

