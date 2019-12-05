# Math Service

This service is able to calculate `factorial`, `fibonacci` and `ackermann` functions.

After running the service, API documentation will be availalble
at the `localhost:8000/docs` or `localhost:8000/redoc`.

And computation results will be at the main page `localhost:8000`

## Requirments

 - Python >= 3.7

`Makefile` can be used to run few simple commands like `requirements`,
`run`, `lint`.

`pip-tools` is using to manage requirements

```sh
(venv) $ pip install pip-tools
```

## Run

 There are few options to run application.

 - First option is to use virtual enviroment.

 Install requirements.
 ```sh
 (venv) $ make install
 ```
 Run application.
 ```sh
 (venv) $ make run
 ```
 - To run it with `docker`
 ```sh
 $ docker build -t math-service .
 $ docker run -it -p 8000:8000 math-service
 ```
