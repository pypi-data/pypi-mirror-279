from setuptools import setup, find_packages

setup(
    name='fractlang',
    version='0.1.20',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'fractx=fractlang.__main__:main',
        ],
    },
    install_requires=[
        # Dependensi lain jika ada
    ],
    author='ryznxx',
    author_email='7ryznxx@gmail.com',
    description='A custom programming language interpreter for Fractlang',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ryznxx/fractlang',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
