from setuptools import setup

setup(
    name='testex',
    packages=['testex'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'pycco',
        'flasgger'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'flask-testing',
        'ddt'
    ],
)
