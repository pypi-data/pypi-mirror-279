from setuptools import setup, find_packages


setup(
    name='veolint',
    version='0.1',
    description='A custom flake8 plugin to check for no empty line after class definition without docstring',
    packages=find_packages(),
    entry_points={
        'flake8.extension': [
            'C999 = veolint.plugin:Veolint',
        ],
    },
    install_requires=[
        'flake8-plugin-utils',
    ],
)
