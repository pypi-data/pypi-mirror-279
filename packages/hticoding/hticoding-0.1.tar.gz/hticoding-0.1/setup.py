from setuptools import setup, find_packages

setup(
    name='hticoding',
    version='0.1',
    description='Python functions for controlling Arduino devices',
    author='taein',
    author_email='hti7220@gmail.com',
    packages=find_packages(),
    install_requires=['pyserial'],
)
