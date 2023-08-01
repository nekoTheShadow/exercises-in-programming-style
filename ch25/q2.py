
class TFQuarantine:
    def __init__(self, func):
        self._funcs = [func]

    def bind(self, func):
        self._funcs.append(func)
        return self

    def execute(self):
        def guard_callable(v):
            return v() if callable(v) else v
        
        value = lambda : None
        for func in self._funcs:
            value = func(guard_callable(value))
        print(guard_callable(value))

def intercept(arg):
    print("INTERCEPT")
    return arg

TFQuarantine(lambda v : 1).bind(intercept)

# ログを出力するだけの関数interceptを定義し、関数シーケンスに含める。
# bindが関数を実行していると、executeの前にintercept関数がログ出力をするが、
# このプログラムを実行してもログ出力がなされない。