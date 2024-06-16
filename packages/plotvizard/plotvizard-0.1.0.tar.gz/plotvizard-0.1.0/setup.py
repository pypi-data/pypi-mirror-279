# setup.py
from setuptools import setup, find_packages

setup(
    name='plotvizard',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'matplotlib',
        'dash',
        'plotly',
    ],
    entry_points='''
        [console_scripts]
        plotvizard=plotvizard:main
    ''',
    author='Chanaka Prasanna',
    author_email='chanakapinfo@gmail.com',
    description='A data visualization library with interractive functionalities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Chanaka-Prasanna/visualizer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
