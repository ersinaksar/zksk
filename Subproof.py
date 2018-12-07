from petlib.ec import EcPt

class RightSide:
    def __init__(self, secret, ecPt):
        if not isinstance(secret, Secret) or not isinstance(ecPt, EcPt):
            raise Exception("in {0} * {1}, the first parameter should be a string (the secret name), and the second parameter should be an elliptic curve point".format(secret, ecPt))
        self.secrets = [secret]
        self.pts = [ecPt]
    def __add__(self, other):
        if not isinstance(other, RightSide):
            raise Exception("${0} doesn't correspond to something like \"x1\" * g1 + \"x2\" * g2 + ... + \"xn\" * gn")
        self.secrets.extend(other.secrets)
        self.pts.extend(other.pts)
        return self
    def eval(self):
        for secret in self.secrets:
            if secret.value == None:
                raise Exception("trying to evaluate secret {0} which was set with no value".format(secret.name))

        def ith_mul(i):
            return self.secrets[i].value * self.pts[i]

        summation = ith_mul(0) 
        for i in range(1, len(self.secrets)):
            summation += ith_mul(i)
        return summation

class Secret:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __mul__(self, ecPt):
        if not isinstance(ecPt, EcPt):
            raise Exception("parameter should be an elliptic curve point", ecPt)
        return RightSide(self, ecPt)
