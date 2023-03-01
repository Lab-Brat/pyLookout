from setuptools import setup

setup(
    name='pylookout',
    version='0.1.0',
    py_modules=[],
    install_requires=[
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'pylookout = main:main',
        ],
    },
)
