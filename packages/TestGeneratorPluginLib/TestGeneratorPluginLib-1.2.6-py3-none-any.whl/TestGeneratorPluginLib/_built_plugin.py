from typing import Callable, Iterable, Type

from TestGeneratorPluginLib._language import _FastRunOption
from TestGeneratorPluginLib._plugin import Plugin
from TestGeneratorPluginLib._managers import BackendManager, Manager
from TestGeneratorPluginLib._widgets import MainTab, SideTab


class BuiltPlugin:
    def __init__(self,
                 plugin: Type,
                 name: str,
                 description: str,
                 version: str,
                 author: str,
                 url='',
                 dependencies: Iterable[str] = tuple(),
                 conflicts: Iterable[str] = tuple(),
                 platform_specific=False,

                 platform: str = ''):
        self._name = name
        self._description = description
        self._version = version
        self._author = author
        self._url = url
        self._dependencies = dependencies
        self._conflicts = conflicts

        self._plugin_class = plugin
        self._plugin: Plugin | None = None
        self._platform = platform if platform_specific else ''

    def init(self, bm):
        self._plugin = self._plugin_class(bm)

    def terminate(self):
        if self._plugin:
            self._plugin.terminate()

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def version(self) -> str:
        return self._version

    @property
    def author(self) -> str:
        return self._author

    @property
    def url(self) -> str:
        return self._url

    @property
    def platform(self) -> str:
        return self._platform

    @property
    def dependencies(self) -> Iterable[str]:
        return self._dependencies

    @property
    def conflicts(self) -> Iterable[str]:
        return self._conflicts

    @property
    def main_tabs(self) -> dict[str: Callable[[BackendManager], MainTab]]:
        return self._plugin.main_tabs

    @property
    def side_tabs(self) -> dict[str: Callable[[BackendManager], SideTab]]:
        return self._plugin.side_tabs

    @property
    def managers(self) -> dict[str: Callable[[BackendManager], Manager]]:
        return self._plugin.managers

    @property
    def fast_run_options(self) -> dict[str, list[_FastRunOption]]:
        return self._plugin.fast_run_options

