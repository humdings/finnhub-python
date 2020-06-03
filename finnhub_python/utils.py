import os

import multitasking

multitasking.set_max_threads(multitasking.config["CPU_CORES"] * 5)


def multicall(func, params, *args, **kwargs):
    """
    Calls the same api function several times
    at once and waits until all tasks complete
    before returning.

    :returns dictionary
        {parameter: api result}
    """
    out = {}
    for param in params:
        out[param] = _multitask(
            out, func, param, *args, **kwargs
        )
    multitasking.wait_for_tasks()
    return out


@multitasking.task
def _multitask(out, func, param, *args, **kwargs):
    """
    Utility for making the same api call several times
    at once with different parameters.

    :param out: dict: container for returned data
    :param func: api method to call
    :param param: the parameter in the api call that is changing (usually symbols)
    :param args: positional arguments for api method
    :param kwargs: keyword arguments for api method

    :return: None: Only populates the 'out' dictionary
    """
    result = func(param, *args, **kwargs)
    out[param] = result


def get_finnhub_api_key(env=None):
    if env is None:
        env = os.environ
    return env.get('FINNHUB_API_KEY', None)
