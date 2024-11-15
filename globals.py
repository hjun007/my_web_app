class GlobalVars:
    def __init__(self):
        self._push_time = {'hour': 22, 'minute': 0}
        self._is_running = False
        
    @property
    def push_time(self):
        return self._push_time
        
    @property
    def is_running(self):
        return self._is_running
        
    def update_push_time(self, hour, minute):
        self._push_time['hour'] = hour
        self._push_time['minute'] = minute
        
    def set_running_status(self, status):
        self._is_running = status

# 创建全局实例
globals = GlobalVars() 