import inspect
from starlette.testclient import TestClient

print('TestClient init signature:', inspect.signature(TestClient.__init__))
print('Base Client init signature:', inspect.signature(TestClient.__mro__[1].__init__))
print('\nTestClient.__init__ source:\n')
print(inspect.getsource(TestClient.__init__))
