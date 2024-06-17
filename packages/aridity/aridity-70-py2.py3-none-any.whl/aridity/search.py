from .util import UnparseNoSuchPathException

def scopedepths(scope):
    scopes = [scope]
    while scopes:
        nextscopes = []
        for s in scopes:
            nextscopes.extend(s.parents)
        yield scopes
        scopes = nextscopes

def resolvedscopeornone(s, path):
    for name in path:
        r = s.resolvableornone(name)
        if r is None:
            return
        s = r.resolve(s)
        if not hasattr(s, 'resolvableornone'):
            return
    return s

class Query:

    @classmethod
    def _of(cls, *args):
        return cls(*args)

    def __init__(self, path):
        self.path = path

    def _scoreresolvables(self, scope):
        tail = self.path[1:]
        for k, v in enumerate(scopedepths(scope)):
            for s in v:
                r = s.resolvables.getornone(self.path[0])
                if r is not None:
                    if tail:
                        obj = r.resolve(s) # XXX: Wise?
                        if hasattr(obj, 'parents'):
                            for score, rr in self._of(tail)._scoreresolvables(obj):
                                yield score + [k], rr
                    else:
                        yield [k], r

    def search(self, scope):
        pairs = list(self._scoreresolvables(scope))
        try:
            return min(pairs, key = lambda t: t[0])[1]
        except ValueError:
            raise UnparseNoSuchPathException(self.path)

def slices(path):
    n = len(path)
    for k in range(n)[::-1]:
        for start in range(n - k):
            v = path[start:start + k]
            yield v
            if not v:
                return
