
import functools

# https://stackoverflow.com/questions/3012421/python-memoising-deferred-lookup-property-decorator
def lazyprop(fn):
    attr_name = '_lazy_' + fn.__name__

    @functools.wraps(fn)
    def get(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    @functools.wraps(fn)
    def set(self, value):
        setattr(self, attr_name, value)

    @functools.wraps(fn)
    def delete(self):
        delattr(self, attr_name)

    return property(get, set, delete)
