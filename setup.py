from setuptools import setup, find_packages
from gitdl import __version__

setup(
    name='gitdl',
    version=__version__,
    description='Download git repositories locally',
    long_description="",
    author='Sanket Dasgupta',
    author_email='sanketdasgupta@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests', 'docopt', 'tabulate', 'tqdm'],
    entry_points={
        'console_scripts': [
            'gitdl=gitdl.gitdl:main',
        ],
    },
)
