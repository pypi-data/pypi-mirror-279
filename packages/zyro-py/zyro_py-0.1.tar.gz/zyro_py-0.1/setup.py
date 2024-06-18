from setuptools import setup, find_packages

setup(
    name='zyro_py',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'zyro_py=zyro_py.__main__:main',
        ],
    },
)