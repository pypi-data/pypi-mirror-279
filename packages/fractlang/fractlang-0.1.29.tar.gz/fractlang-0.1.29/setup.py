from setuptools import setup, find_packages

setup(
    name='fractlang',
    version='0.1.29',
    packages=find_packages(),
    install_requires=[
        'watchdog',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'frx = fractlang.frxparser:main',
        ],
    },
   author='ryznxx',
    author_email='7ryznxx@gmail.com',
    description='A custom programming syntax for Fractlang in python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/fractlang',
    license='MIT',
)
