from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='kody-protobuilder',
    version='0.0.4',
    description='protofile builder',
    author='kody-protobuilder_author',
    author_email='kodyprotobuilder@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/byundojin/auto-protobuf',
    install_requires=['grpcio', 'grpcio-tools',],
    packages=find_packages(),
    python_requires='>=3.8'
)