from pprint import pformat

def teq(a, b):
    assert a == b, "\n%s\n!=\n%s" % (pformat(a),
                                     pformat(b))
