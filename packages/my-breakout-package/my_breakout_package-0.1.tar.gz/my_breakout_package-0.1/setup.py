# setup.py
from setuptools import setup, find_packages

setup(
    name='my_breakout_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    description='A package for calculating breakout trading conditions.',
    author='Kapil Mittal',
    author_email='kapil@breakoutinvesting.in',
    url='https://github.com/yourusername/my_breakout_package',  # Update with your URL
)
