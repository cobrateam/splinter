class D(dict):
    def __getattr__(self, k):
        return dict.__getitem__(self, k)

test = D()
