"""Скрипт Setup.py для проекта по упаковке."""

from setuptools import setup, find_packages

from TestGeneratorPluginLib._config import VERSION


def readme():
    with open('readme.md', 'r', encoding='utf-8') as f:
        res = []
        for line in f:
            line = line.replace('](doc', '](https://github.com/SergeiKrivko/TestGeneratorPluginLib/blob/master/doc')
            res.append(line)
        return ''.join(res)


def license():
    with open('LICENSE', 'r', encoding='utf-8') as f:
        return f.read()


def requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return f.read().split()


if __name__ == '__main__':
    setup(
        name='TestGeneratorPluginLib',
        author='SergeiKrivko',
        version=VERSION,
        url='https://github.com/SergeiKrivko',
        long_description=readme(),
        long_description_content_type='text/markdown',
        license=license(),
        package_dir={'TestGeneratorPluginLib': 'TestGeneratorPluginLib'},
        packages=find_packages(include=['TestGeneratorPluginLib*']),
        description='A TestGeneratorPluginLib package.',
        install_requires=requirements(),
        python_requires='>=3.10'
    )
