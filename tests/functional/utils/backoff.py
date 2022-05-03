from functools import wraps
from time import sleep

from utils.app_logger import get_logger

logger = get_logger("wait_func")


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка. Использует наивный
    экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            time = start_sleep_time
            count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    count += 1
                    if count == 10:
                        break
                    sleep(time)
                    if time < border_sleep_time:
                        time *= factor
                    else:
                        time = border_sleep_time

        return inner

    return func_wrapper
