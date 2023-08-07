

class LLMModel(object):
    def make_request(self, prompt):
        raise NotImplementedError("子类必须实现 make_request 方法")