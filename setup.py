import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='app',
    version='1.0.0',
    url='',
    license='BSD',
    maintainer='TruthTree',
    maintainer_email='',
    description='REST API server for TruthTree ML',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-restplus==0.9.2',
        'Flask-SQLAlchemy==2.1'
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)

