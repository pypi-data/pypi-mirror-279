# Vaul

Vaul is a nano-framework for deploying Python functions as APIs on AWS Lambda using Function URLs. It provides seamless integration with OpenAPI Schema and allows for monitoring and managing microservices with ease.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Defining Actions](#defining-actions)
  - [Deploying to AWS Lambda](#deploying-to-aws-lambda)
  - [Handling Requests](#handling-requests)
  - [Using OpenAPI Schema](#using-openapi-schema)
  - [Accessing Request Data](#accessing-request-data)
- [Contributing](#contributing)
- [License](#license)


## Introduction

Vaul is designed to help developers quickly deploy Python functions as serverless APIs on AWS Lambda. With a focus on simplicity and efficiency, Vaul leverages AWS Lambda's Function URLs to provide scalable and cost-effective API endpoints.

## Features

- **Nano-framework**: Lightweight and easy to use.
- **OpenAPI Integration**: Automatically generate OpenAPI schema for your APIs.
- **AWS Lambda Support**: Seamlessly deploy functions to AWS Lambda using Function URLs.
- **Request Validation**: Built-in request validation using Pydantic.
- **CORS Support**: Pre-configured Cross-Origin Resource Sharing (CORS) support.
- **Custom Actions**: Define and manage custom actions with ease.

## Installation

To install Vaul, you can use `pip`:

```bash
pip install vaul
```

## Usage

### Defining Actions
Vaul allows you to define actions (API endpoints) using simple decorators. Here is an example of how to define a GET and POST endpoint:

```python
from vaul import Vaul

app = Vaul()

@app.action(path='/hello', method="GET")
def hello(name: str) -> str:
    return f"Hello, {name}!"

@app.action(path='/echo', method="POST")
def echo(data: dict) -> dict:
    return data

def handler(event, context):
    return app.handler(event)
```

### Deploying to AWS Lambda
To deploy your Vaul application to AWS Lambda, use the AWS CLI or AWS Management Console. Ensure that your Lambda function's handler is set to the appropriate entry point (e.g., handler).

### Using OpenAPI Schema
Vaul automatically generates an OpenAPI schema for your API based on the defined actions. You can access the schema by visiting the `/openapi` endpoint.

```curl
curl -X GET https://your-function-url/openapi.json
```

### Accessing Request Data
You can access the request data (e.g., query parameters, headers, body) using the `get_request` function:

```python
from vaul import Vaul, get_request

app = Vaul()

@app.action(path='/hello', method="GET")
def hello() -> str:
    request = get_request()
    user_agent = request.headers.get('User-Agent')
    return f"Hello, {user_agent}!"
    
def handler(event, context):
    return app.handler(event)
```

### Handling Requests
Vaul's middleware automatically handles incoming requests, validates them, and routes them to the appropriate action based on the request path and method.

## Contributing
We welcome contributions from the community! If you would like to contribute to Vaul, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them to your branch.
4. Push your changes to your fork.
5. Create a pull request to the main repository.
6. We will review your changes and merge them if they meet our guidelines.
7. Thank you for contributing to Vaul!

## License
Vaul is licensed under the GNU General Public License v3.0. See the LICENSE file for more information.



