from pigmento import pnt
from test_folder.a import A


class B(A):
    def ask(self):
        pnt('hello')
