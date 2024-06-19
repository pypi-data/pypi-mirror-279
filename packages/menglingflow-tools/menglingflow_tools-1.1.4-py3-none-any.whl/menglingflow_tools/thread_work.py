from threading import Thread, get_ident
from menglingtool.queue import Mqueue
import traceback
import os
import logging
import time
import asyncio

# 便捷获取log对象
def getLogger(name, level=logging.INFO, log_path=None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.FileHandler(log_path) if log_path else logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def run_thread_tasks(task_queue: Mqueue, getGood, gooder_getResult, good_num: int,
                     logger: logging.Logger = None,
                     is_put_args=True,
                     is_put_kwargs=True,
                     is_put_time=True) -> list[Thread]:
    logger = logger if logger else getLogger(f'pid-{get_ident()}')
    logger.info(f'PID-{os.getpid()} worker num: {good_num}')

    def _worker():
        gooder = getGood()
        while True:
            que, args, kwargs = task_queue.get()
            sd = time.time()
            try:
                result = gooder_getResult(gooder, *args, **kwargs)
                err = None
            except:
                err = traceback.format_exc()
                result = None

            logger.info(f'args:{args}, kwargs:{kwargs}, is_err:{bool(err)}')
            rdt = {}
            if is_put_args:
                rdt['args'] = args
            if is_put_kwargs:
                rdt['kwargs'] = kwargs
            rdt['result'] = result
            rdt['err'] = err
            if is_put_time:
                rdt['time'] = time.time() - sd
            que.put(rdt)

    ts = [Thread(target=_worker, daemon=True) for _ in range(good_num)]
    [t.start() for t in ts]
    return ts


def arg_in_task_puts(task_queue: Mqueue, vs: list) -> (Mqueue, int):
    return all_in_task_puts(task_queue, [[(v,), {}] for v in vs])


def args_in_task_puts(task_queue: Mqueue, argss: list[list]) -> (Mqueue, int):
    return all_in_task_puts(task_queue, [[args, {}] for args in argss])


def kwargs_in_task_puts(task_queue: Mqueue, kwargss: list[dict]) -> (Mqueue, int):
    return all_in_task_puts(task_queue, [[(), kwargs] for kwargs in kwargss])


def all_in_task_puts(task_queue: Mqueue, args_and_kwargs: list) -> (Mqueue, int):
    result_queue = Mqueue()
    task_queue.puts(*[(result_queue, args, kwargs)
                    for args, kwargs in args_and_kwargs])
    return result_queue, len(args_and_kwargs)


def getResults(result_queue: Mqueue, maxlen: int) -> list[dict]:
    while result_queue.qsize() < maxlen:
        time.sleep(1)
    return result_queue.to_list()


async def async_getResults(result_queue: Mqueue, maxlen: int) -> list[dict]:
    while result_queue.qsize() < maxlen:
        await asyncio.sleep(1)
    return result_queue.to_list()
