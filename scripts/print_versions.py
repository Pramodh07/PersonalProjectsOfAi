import importlib

for pkg in ('fastapi', 'starlette', 'httpx'):
    try:
        m = importlib.import_module(pkg)
        print(pkg, getattr(m, '__version__', 'n/a'))
    except Exception as e:
        print(pkg, 'not installed', e)
