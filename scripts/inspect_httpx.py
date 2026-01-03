import inspect
import httpx
print('httpx.Client init:', inspect.signature(httpx.Client.__init__))
print('httpx.__version__', httpx.__version__)
