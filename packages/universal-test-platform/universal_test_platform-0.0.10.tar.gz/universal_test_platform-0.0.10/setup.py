from setuptools import setup, find_packages

setup(
    name='universal-test-platform',
    version='0.0.10',

    package_dir  = {'': 'src'},
    package_data = {'utp': ['*']},
    packages     = find_packages('src'),
    install_requires=['Click', 'pyyaml' ],
    entry_points={
        'console_scripts': [
            'utp = utp.utp:cli'
        ]
    }
)