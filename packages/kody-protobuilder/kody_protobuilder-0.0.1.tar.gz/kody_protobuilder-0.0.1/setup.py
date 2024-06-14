from setuptools import setup, find_packages


setup(
    name='kody-protobuilder',
    version='0.0.1',
    description='protofile builder',
    author='kody-protobuilder_author',
    author_email='kodyprotobuilder@gmail.com',
    url='https://github.com/byundojin/auto-protobuf',
    install_requires=['grpcio', 'grpcio-tools',],
    packages=find_packages(),
    python_requires='>=3.8'
)