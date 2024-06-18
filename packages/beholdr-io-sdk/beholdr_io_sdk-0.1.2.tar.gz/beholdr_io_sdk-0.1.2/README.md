# Beholdr.io SDK Python
A simple SDK to allow you to integrate your services with Beholdr.io easily.


Here is a basic example of how to use the Beholdr.io SDK

```python
    from beholdr_io_sdk.src.client import BeholdrClient
    class MyService:
        beholdr_client = BeholdrClient(
            service_api_key='xxxxxxxxxxx'
        )

        def something(self):
            pass
        def do_something(self):
            try:
                result = self.something() 
                response = client.emit_metric(200, "Did something")
            except Exception as e:
                response = client.emit_metric(400, "Unable to do something.")
```


# Installation
``` bash
    pip install beholdr-io-sdk
```

# Authentication
To integrate the `BeholdrClient` class into your service, you will need to provide the `ServiceApiKey` generated from your account at [Beholdr.io](https://beholdr.io). This API key allows Beholdr.io to accurately collect and process metrics specific to your service, ensuring that your Monitors can effectively track performance and promptly alert you to any issues.

We recommend that you pass your API keys to the `BeholdrClient` class via environment variables for better security.

``` bash
API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxx

```

``` python
    import os

    api_key = os.getenv('API_KEY', 'default_value_if_not_found')

    beholdr_client = BeholdrClient(
        service_api_key=api_key
    )
```


# Documentation
For a comprehensive documentation, check out the Beholdr.io's information [page](https://beholdr.io/info).


# License
Code is licensed under the Apache License 2.0.