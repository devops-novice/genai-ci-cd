from contextlib import contextmanager

@contextmanager
def tag(name):
    print(f"<{name}>")
    yield
    print(f"</{name}>")

with tag("devsecops"):
    print("Hello from GenAI Engineering")
