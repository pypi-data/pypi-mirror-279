class HookManager:
    def __init__(self):
        self.hooks = {
            'before_generate': [],
            'after_generate': []
        }

    def register_hook(self, hook_point, func, order=0):
        if hook_point in self.hooks:
            self.hooks[hook_point].append((func, order))
            self.hooks[hook_point].sort(key=lambda x: x[1])
        else:
            raise ValueError(f"Hook point {hook_point} not recognized.")

    def trigger_hooks(self, hook_point, data):
        for func, _ in self.hooks.get(hook_point, []):
            func(data)
        return data


hook_manager = HookManager()
