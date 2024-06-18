from typing import Callable, Any

from PyQt6.QtCore import QThread, QObject


class BackendManager:
    def __init__(self):
        self.sm = _SettingsManager()
        self.processes = _ProcessesManager()
        self.projects = _ProjectsManager()


class _SettingsManager:
    def get(self, key, default=None): ...
    def set(self, key, value): ...
    def delete(self, key): ...

    def get_data(self, key, default=None): ...
    def set_data(self, key, value): ...
    def delete_data(self, key): ...

    def get_general(self, key, default=None): ...
    def set_general(self, key, value): ...
    def delete_general(self, key): ...


class _ProcessesManager:
    def run(self, thread: Callable[[], Any] | QThread, group: str, name: str) -> QThread: ...
    async def run_async(self, thread: Callable[[], Any] | QThread, group: str, name: str): ...


class _ProjectsManager:
    @property
    def current(self):
        return None


class Manager(QObject):
    def __init__(self, bm):
        super().__init__()
        self._bm = bm

    async def load(self):
        pass

    async def close(self):
        pass

    async def indexing(self):
        pass

