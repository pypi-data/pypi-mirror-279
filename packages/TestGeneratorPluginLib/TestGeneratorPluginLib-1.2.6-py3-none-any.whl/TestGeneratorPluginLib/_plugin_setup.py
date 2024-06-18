import argparse
import os
import shutil
import subprocess
import sys
from sys import argv
from typing import Iterable


class PluginSetup:
    def __init__(self,
                 name: str,
                 description: str,
                 version: str,
                 author: str,
                 plugin: str,
                 url='',
                 platform_specific: bool = None,
                 dependencies: Iterable[str] = tuple(),
                 conflicts: Iterable[str] = tuple(),

                 directories: Iterable[str] = tuple(),
                 requirements: Iterable[str] = tuple(),
                 ):
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self._plugin = plugin
        self.url = url
        self.platform_specific = bool(requirements) if platform_specific is None else platform_specific
        self.dependencies = list(dependencies)
        self.conflicts = list(conflicts)

        self._directories = list(directories)
        self._requirements = list(requirements)

        self._parse_args()

    def _parse_args(self):
        _parser = argparse.ArgumentParser()
        _parser.add_argument('-b', '--build', action='store_true')
        _parser.add_argument('-o', '--output')
        _parser.add_argument('-u', '--upload', action='store_true')
        _parser.add_argument('-e', '--email')
        _parser.add_argument('-p', '--password')
        _parser.add_argument('--signup', action='store_true')
        _parser.add_argument('--verify-email', action='store_true')
        args = _parser.parse_args()

        if args.build or args.upload:
            dist_path = self._build(args.output)
            if args.upload:
                self._upload(args, dist_path)
        elif args.signup:
            self._signup(args)
        elif args.verify_email:
            self._signup(args)

    def _build(self, output=None):
        build_path = f'build/{self.name}'
        dist_path = output or f'dist/{self.name}.TGPlugin'
        if os.path.isdir(build_path):
            shutil.rmtree(build_path)
        os.makedirs(build_path)
        if os.path.dirname(dist_path):
            os.makedirs(os.path.dirname(dist_path), exist_ok=True)

        for el in self._directories:
            shutil.copytree(el, os.path.join(build_path, el))
        shutil.copy(argv[0], os.path.join(build_path, os.path.basename(argv[0])))

        if self._requirements:
            subprocess.run(['pip', 'install', *self._requirements, '-t', os.path.join(build_path, '__packages__')])

        with open(os.path.join(build_path, '__plugin__.py'), 'w', encoding='utf-8') as f:
            f.write(f"""from TestGeneratorPluginLib._built_plugin import BuiltPlugin
from {self._plugin[:self._plugin.rindex('.')]} import {self._plugin[self._plugin.rindex('.') + 1:]} as Plugin

__plugin__ = BuiltPlugin(Plugin, {repr(self.name)}, {repr(self.description)}, {repr(self.version)}, {repr(self.author)},
                         {repr(self.url)}, {self.dependencies}, {self.conflicts}, {self.platform_specific}, 
                         '{sys.platform}')
""")

        shutil.make_archive(dist_path, 'zip', build_path)
        return dist_path

    def _upload(self, args, dist_path):
        from TestGeneratorPluginLib._firebase import FirebaseService

        service = FirebaseService(args.email, args.password)
        service.log_in(args.signup)

        platform = sys.platform if self.platform_specific is None and self._requirements or self.platform_specific \
            else 'all'
        service.upload_file(dist_path + '.zip',
                            f"{self.name}/{platform}.TGPlugin.zip")
        service.upload_metadata(self.name, {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'author': self.author,
            'url': self.url,
            'dependencies': self.dependencies,
            'conflicts': self.conflicts,
        })
        service.upload_metadata(self.name + '/versions', {platform: self.version})

    def _signup(self, args):
        from TestGeneratorPluginLib._firebase import FirebaseService

        service = FirebaseService(args.email, args.password)

        service.log_in(args.signup)
        service.verify_email()
        print("Verified email")
        input("Press Enter to continue...")
