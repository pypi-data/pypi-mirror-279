from pistol_magazine.hooks.hook_manager import hook_manager


def hook(hook_point, order=0):
    def decorator(func):
        hook_manager.register_hook(hook_point, func, order)
        return func
    return decorator
