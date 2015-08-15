from setuptools import setup, find_packages

setup(
    name='gitdl',
    version='0.1',
    description='Download git repositories locally',
    long_description="",
    author='Sanket Dasgupta',
    author_email='sanketdasgupta@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'gitdl=gitdl.gitdl:main',
        ],
    },
)
