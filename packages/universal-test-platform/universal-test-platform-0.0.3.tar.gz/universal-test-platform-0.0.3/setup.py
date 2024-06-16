from setuptools import setup

setup(
    name='universal-test-platform',
    version='0.0.3',
    py_modules=['utp'],
    install_requires=['Click', 'pyyaml' ],
    entry_points={
        'console_scripts': [
            'utp = utp:cli'
        ]
    }
)