class HookManager:
    def __init__(self):
        """
        before_generate: Executes operations before generating all data. Suitable for tasks like logging or starting external services.
        after_generate: Executes operations after generating each data entry but before final processing. Suitable for tasks like data validation or conditional modifications.
        final_generate: Executes operations after generating and processing all data entries. Suitable for final data processing, sending data to message queues, or performing statistical analysis.
        """
        self.hooks = {
            'pre_generate': [],
            'after_generate': [],
            'final_generate': [],
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
