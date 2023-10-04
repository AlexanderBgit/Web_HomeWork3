import time
import logging

from multiprocessing import cpu_count, Pool

# Ініціалізація системи логування
log_file = 'factorize.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s PID: %(process)d [ %(threadName)s ] %(message)s")
formatter = logging.Formatter("%(asctime)s PID: %(process)d [ %(threadName)s ] %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)

from factorize_multi import (
    factorize_helper,
    factorize_m,
)
from factorize_sync import factorize_s

def factorize(method: int = 0):
    source = (128, 255, 99999, 10651060)

    start_time = time.time()  # Початок вимірювання часу

    if method == 0:
        a, b, c, d = factorize_s(*source)
    elif method == 1:
        a, b, c, d = factorize_m(source)

    end_time = time.time()  # Кінець вимірювання часу
    elapsed_time = end_time - start_time

    logging.info(f"Method {method}: Elapsed time: {elapsed_time} seconds")

    return a, b, c, d

if __name__ == "__main__":
    result_sync = factorize(0)  # Виконання факторизації з методом 0 (синхронний)
    result_multi = factorize(1)  # Виконання факторизації з методом 1 (мультипроцесорний)

    a_sync, b_sync, c_sync, d_sync = result_sync
    a_multi, b_multi, c_multi, d_multi = result_multi

    assert a_sync == a_multi
    assert b_sync == b_multi
    assert c_sync == c_multi
    assert d_sync == d_multi

