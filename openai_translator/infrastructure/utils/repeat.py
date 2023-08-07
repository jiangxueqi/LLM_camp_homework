from infrastructure.logger.logger import LOG
import traceback
import time

def retries_on_exception(max_tries=3, wait_time=3, hook=None, hook_arg=None, hook_grain_size=1, exceptions=(Exception,)):
    def dec(func):
        def f2(*args, **kwargs):
            hook_grain_size_init = hook_grain_size
            tries = list(range(max_tries))
            tries.reverse()
            for tries_remaining in tries:
                hook_grain_size_init = hook_grain_size_init - 1
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    LOG.error(f"捕获的异常：{e}")
                    LOG.error(f"异常具体信息：{traceback.format_exc()}")
                    if tries_remaining > 0:
                        if hook_grain_size_init == 0:
                            hook_grain_size_init = hook_grain_size
                            if hook is not None:
                                if hook_arg is not None:
                                    hook(hook_arg)
                                else:
                                    hook()
                        LOG.info(f"等待{wait_time}s后重试")
                        time.sleep(wait_time)
                    else:
                        LOG.error(f"重试超过最大次数：{max_tries}")
        return f2
    return dec