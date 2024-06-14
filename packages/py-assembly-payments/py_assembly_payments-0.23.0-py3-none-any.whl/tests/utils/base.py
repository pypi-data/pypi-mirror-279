from datetime import datetime, timedelta
from unittest import TestCase

import jwt
from faker import Faker

from assembly_payments.client import TEST_AUTH_URL

fake = Faker()

example_key = """
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCxlVm+DawmijNIDmAt11Sk5lRkd9691RyQevmr8u/eKvTV7eta
ZmGm2GmbuURYzwQfQ1+DFNrzu70wBLTyDrxCoX/vb/5hANwLJr5Eec6gGTF6/y4F
riRM1NEBZG9PnvmEPa1bfa27dnV5hz+GTIsCFCw4rXGI7c6ETg+v9t4HqQIDAQAB
AoGAMoekuYd6bJz2apJsm56h3yoK6WuSXcG+Fv5m/J5r0nO2pwjD5z0qnCcIJd9Z
q0t8iMjK7KmKg7/v3TH5qsa2mmUZ8UYMI5VmkwlKL4BD9mT67+ZAlqdLOHlrdrhG
u2FWR0PF5W2z06NqohWHepL01K7PLtxzaVzbQIwS4X3YsuECQQDrcqdSqj6gSF3Q
ZOZEMoES64iwAe/Fi4VmE6s0PEhoVXbbxFNxuvQPkylmoGs82ByAqltNk7p8G0Wb
hd+j3/KHAkEAwRWmkD189gSR/jLPEy/2fIkXhfe98OruPyG2yDsa3vp5wC2nrniG
udMxC4OJ1yXHGt4KBeOoOL94lX9p9UhQTwJAOx+SZs67ZTJm5HLB4/Qut1qP+2qx
FBEiEWz0++v7Xr+/VhZpwdBpgxO4PL4hz6iRF7ovrT5ggNO0WgZ3D0aoNwJBAKhx
T9ajnaEuCYLeJmJRxFGOc3QO1agX+3Id4kw5q858arxp18/QG5B/Glk2Dokfztu0
er/6hCXFe9fHyNMPm+cCQQCsqdhniYyaHPlyn/6bOwCcZua74JRZ3vNSkjAKzHan
WjSRdVvCHs8bY1Um0QZ+nHpT3QhcBPYyQoJArs8P1XBH
-----END RSA PRIVATE KEY-----"""

class PyAssemblyPaymentsTestCase(TestCase):
    def _setup_auth(self, mocker, expires_in=3600):
        expires_at = (datetime.now() + timedelta(seconds=expires_in)).timestamp()
        token = jwt.encode({"exp": expires_at}, example_key, algorithm="RS256")
        mocker.post(f"{TEST_AUTH_URL}/tokens", json={"access_token": token, "expires_in": expires_in, "token_type": "Bearer"})
        return token