from setuptools import setup

setup(
    name='universal-test-platform',
    version='0.0.1',
    py_modules=['universal-test-platform'],
    install_requires=['Click', 'pyyaml' ],
    entry_points={
        'console_scripts': [
            'utp = utp:cli'
        ]
    }
)