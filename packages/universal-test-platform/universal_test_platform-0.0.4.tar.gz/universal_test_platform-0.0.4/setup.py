from setuptools import setup, find_packages

setup(
    name='universal-test-platform',
    version='0.0.4',
    # py_modules=['utp'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['Click', 'pyyaml' ],
    entry_points={
        'console_scripts': [
            'utp = utp:cli'
        ]
    }
)