from setuptools import setup

setup(
    name='ytget',
    version='0.2.1',
    author='Cosk',
    description='Easily get data and download youtube videos, focused on speed and simplicity.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Coskon/ytget',
    packages=['ytget'],
    install_requires=[
        'bs4', 'tqdm', 'requests', 'colorama'
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'ytget=ytget.console:cmd_parser',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)