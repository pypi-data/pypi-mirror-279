# SayoPy: Python Web Framework built for learning purposes

![purpose](https://img.shields.io/badge/purpose-learning-green)
![PyPI - Version](https://img.shields.io/pypi/v/SayoPy)

SayoPy is a Python web framework built for learning purposes.

It's a WSGI framework and can be used with any WSGI application server such as Gunicorn.

## Instalition
```shell
pip install sayopy
```

### Basic usage:
```python
from SayoPy.api import SayoPy

app = SayoPy()

@app.route("/home")
def home(request, response):
    response.text = "Hello from the Home page"


@app.route("/hello/name")
def greating(request, response, name):
    response.text = f"Hello, {name}!"


@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "Books page"
    
    def post(self, request, response):
        response.text = "Endpoint to create a book"


@app.route("/template")
def template_handler(request, response):
    response.html = app.template(
        "index.html", context={"title": "Best Framework", "name": "Askar Saparov"}
    )


@app.route("/json")
def json_handler(request, response):
    response_data = {"name": "Askar Saparov", "age": 25}
    response.json = response_data

```
