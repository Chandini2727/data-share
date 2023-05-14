from pycocks.cocks import CocksPKG
from pycocks.cocks import Cocks
import base64

cocks_pkg = CocksPKG()
r, a = cocks_pkg.extract("User1")

cocks = Cocks(cocks_pkg.n)  

msg = "welcome to python world".encode()
c = cocks.encrypt(msg, a)
print(c)
'''
cocks_pkg = CocksPKG()
r, a = cocks_pkg.extract("User1")
'''
msg = cocks.decrypt(c, r, a)
print(msg.decode())
