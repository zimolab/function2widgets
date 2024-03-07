class NotRegisteredError(Exception):
    pass


class AlreadyRegisteredError(Exception):
    pass


def safe_pop(target: dict, key: str, *more_keys: str):
    if not more_keys:
        if key in target:
            target.pop(key)
        return target

    all_keys = [key, *more_keys]
    for k in all_keys:
        if k in target:
            target.pop(k)
    return target
