# python concurrent.futures
# python因为其全局解释器锁GIL而无法通过线程实现真正的平行计算。这个论断我们不展开，但是有个概念我们要说明，IO密集型 vs. 计算密集型。
# IO密集型：读取文件，读取网络套接字频繁。
# 计算密集型：大量消耗CPU的数学与逻辑运算，也就是我们这里说的平行计算。
# 而concurrent.futures模块，可以利用multiprocessing实现真正的平行计算。
# 核心原理是：concurrent.futures会以子进程的形式，平行的运行多个python解释器，从而令python程序可以利用多核CPU来提升执行速度。由于子进程与主解释器相分离，
# 所以他们的全局解释器锁也是相互独立的。每个子进程都能够完整的使用一个CPU内核。

# -*- coding:utf-8 -*-
# 求最大公约数
def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i

numbers = [
    (1963309, 2265973), (1879675, 2493670), (2030677, 3814172),
    (1551645, 2229620), (1988912, 4736670), (2198964, 7876293)
]

# 不使用多线程
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor, as_completed, wait, ALL_COMPLETED, FIRST_COMPLETED, FIRST_EXCEPTION

# start = time.time()
# results = list(map(gcd, numbers))
# end = time.time()
# print(('Took %.3f seconds.' % (end - start)))

# 多线程ThreadPoolExecutor
# import time
# from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor
#
# start = time.time()
# pool = ThreadPoolExecutor(max_workers=2)
# results = list(pool.map(gcd, numbers))
# end = time.time()
# print("'Took %.3f seconds.' % (end - start)")

def run():
    start = time.time()
    pool = ProcessPoolExecutor(max_workers=2)
    results = list(pool.map(gcd, numbers))
    end = time.time()
    print(('Took %.3f seconds.' % (end - start)))

#excutor源码解析
class Executor(object):
    """This is an abstract base class for concrete asynchronous executors."""

    def submit(self, fn, *args, **kwargs):
        """Submits a callable to be executed with the given arguments.

        Schedules the callable to be executed as fn(*args, **kwargs) and returns
        a Future instance representing the execution of the callable.

        Returns:
            A Future representing the given call.
        """
        raise NotImplementedError()

    def map(self, fn, *iterables, **kwargs):
        """Returns a iterator equivalent to map(fn, iter).

        Args:
            fn: A callable that will take as many arguments as there are
                passed iterables.
            timeout: The maximum number of seconds to wait. If None, then there
                is no limit on the wait time.

        Returns:
            An iterator equivalent to: map(func, *iterables) but the calls may
            be evaluated out-of-order.

        Raises:
            TimeoutError: If the entire result iterator could not be generated
                before the given timeout.
            Exception: If fn(*args) raises for any values.
        """
        timeout = kwargs.get('timeout')
        if timeout is not None:
            end_time = timeout + time.time()

        fs = [self.submit(fn, *args) for args in zip(*iterables)]

        # Yield must be hidden in closure so that the futures are submitted
        # before the first iterator value is required.
        def result_iterator():
            try:
                for future in fs:
                    if timeout is None:
                        yield future.result()
                    else:
                        yield future.result(end_time - time.time())
            finally:
                for future in fs:
                    future.cancel()
        return result_iterator()

    def shutdown(self, wait=True):
        """Clean-up the resources associated with the Executor.

        It is safe to call this method several times. Otherwise, no other
        methods can be called after this one.

        Args:
            wait: If True then shutdown will not return until all running
                futures have finished executing and the resources used by the
                executor have been reclaimed.
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False

#map
# map(self, fn, *iterables, **kwargs)
def map():
    start = time.time()
    with ProcessPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(gcd, numbers))
    print('results: %s' % results)
    end = time.time()
    print('Took %.3f seconds.' % (end - start))

def submit():
    import time
    from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor

    start = time.time()
    futures = list()
    with ProcessPoolExecutor(max_workers=2) as pool:
        for pair in numbers:
            future = pool.submit(gcd, pair)
            futures.append(future)
    print()
    'results: %s' % [future.result() for future in futures]
    end = time.time()
    print('Took %.3f seconds.' % (end - start))



def future1():
    start = time.time()
    with ProcessPoolExecutor(max_workers=2) as pool:
        futures = [ pool.submit(gcd, pair) for pair in numbers]
        for future in futures:
            print('执行中:%s, 已完成:%s' % (future.running(), future.done()))
        print('#### 分界线 ####')
        for future in as_completed(futures, timeout=2):
            print('执行中:%s, 已完成:%s' % (future.running(), future.done()))
    end = time.time()
    print('Took %.3f seconds.' % (end - start))


def wait1():
    start = time.time()
    with ProcessPoolExecutor(max_workers=2) as pool:
        futures = [ pool.submit(gcd, pair) for pair in numbers]
        for future in futures:
            print('执行中:%s, 已完成:%s' % (future.running(), future.done()))
        print('#### 分界线 ####')
        done, unfinished = wait(futures, timeout=2, return_when=ALL_COMPLETED)
        for d in done:
            print('执行中:%s, 已完成:%s' % (d.running(), d.done()))
            print(d.result())
    end = time.time()
    print('Took %.3f seconds.' % (end - start))


if __name__ == '__main__':
    run()
    wait1()
    future1()
    map()
    submit()
