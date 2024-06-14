from gunicorn.app.base import BaseApplication
from gunicorn.arbiter import Arbiter
from gunicorn.workers.base import Worker
from fastapi import APIRouter, FastAPI, File, Request, UploadFile
from fastapi.params import Form
from functools import wraps
import inspect
import aiofiles
import logging

from pyfunvice.common_func import delete_file
from pyfunvice.struct import ResponseModel

app = FastAPI()
faas_router = APIRouter()

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] [%(thread)d] [%(levelname)s] %(message)s"
)


def app_service_get(path="/"):
    def decorator(func):
        @wraps(func)
        async def wrapper(data: dict):
            return await func(data)

        @faas_router.get(path)
        async def process_function(request: Request):
            try:
                data = dict(request.query_params)
                result = await wrapper(data)
                return ResponseModel(
                    requestId=data.get("requestId"),
                    code="200",
                    message="success",
                    data=result,
                )
            except Exception as e:
                logging.exception("Server inner error occurred: ")
                return ResponseModel(
                    requestId=data.get("requestId"),
                    code="500",
                    message=str(e),
                    data={},
                )

        return process_function

    return decorator


def app_service(path="/", body_type="raw", inparam_type="dict"):
    """
    path : str = "/",                       # http path
    body_type : str = "raw", "form-data"    # http body type
    inparam_type : str = "dict", "flat"     # faas inparam type
    """

    def decorator(func):
        if body_type == "raw":
            if inparam_type == "dict":

                @wraps(func)
                async def wrapper(data: dict):
                    return await func(data)

                @faas_router.post(path)
                async def process_function(request: Request):
                    try:
                        data = await request.json()
                        result = await wrapper(data)
                        return ResponseModel(
                            requestId=data.get("requestId"),
                            code="200",
                            message="success",
                            data=result,
                        )
                    except Exception as e:
                        logging.exception("Server inner error occurred: ")
                        return ResponseModel(
                            requestId=data.get("requestId"),
                            code="500",
                            message=str(e),
                            data={},
                        )

            elif inparam_type == "flat":

                @wraps(func)
                async def wrapper(*args, **kwargs):
                    return await func(*args, **kwargs)

                signature = inspect.signature(func)
                parameters = list(signature.parameters.values())

                @faas_router.post(path)
                async def process_function(request: Request):
                    try:
                        data = await request.json()
                        args = [data.get(param.name) for param in parameters]
                        result = await wrapper(*args)
                        return ResponseModel(
                            requestId=data.get("requestId"),
                            code="200",
                            message="success",
                            data=result,
                        )
                    except Exception as e:
                        logging.exception("Server inner error occurred: ")
                        return ResponseModel(
                            requestId=data.get("requestId"),
                            code="500",
                            message=str(e),
                            data={},
                        )
            else:
                pass
            return func
        elif body_type == "form-data":

            @wraps(func)
            async def wrapper(file_name: str, file: UploadFile = File(...)):
                async with aiofiles.open(file_name, "wb") as out_file:
                    content = await file.read()
                    await out_file.write(content)
                result = await func(file_name)
                delete_file(file_name)
                return result

            @faas_router.post(path)
            async def process_function(
                file: UploadFile = File(...),
                requestId: str = Form(None),
            ):
                try:
                    if not file:
                        raise Exception("file is empty")
                    file_name: str = requestId
                    result = await wrapper(file_name, file)
                    return ResponseModel(
                        requestId=requestId,
                        code="200",
                        message="success",
                        data=result,
                    )
                except Exception as e:
                    logging.exception("Server inner error occurred: ")
                    return ResponseModel(
                        requestId=requestId,
                        code="500",
                        message=str(e),
                        data={},
                    )
        else:
            pass
        return func

    return decorator


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def start_app(port: int = 8000, workers: int = 1, post_fork_func: callable = None):
    app.include_router(faas_router)

    def post_fork(server: Arbiter, worker: Worker):
        if post_fork_func is not None:
            post_fork_func()
        else:
            pass

    options = {
        "bind": f"0.0.0.0:{port}",
        "timeout": 7200,
        "workers": workers,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "post_fork": post_fork,
    }
    StandaloneApplication(app, options).run()


def get_app_instance(post_fork_func: callable = None):
    if post_fork_func is not None:
        post_fork_func()
    app.include_router(faas_router)
    return app
