from setuptools import setup, find_packages

setup(
    name="embedding_server_client",
    version="1.0.0",
    packages=find_packages(),
    package_data={'embedding_server_client': ['schema/*']},
    author="Anil Aydiner",
    author_email="a.aydiner@qimia.de",
    description="A ZMQ client interface for embedding server",
    long_description="A ZMQ client interface for embedding server",
    url="https://gitlab.com/qimiaio/qimia-ai-dev/embedding-server-client",
    python_requires=">=3.11",
    install_requires=[
        "pyzmq>=25.1.1",
        "msgpack>=1.0.7",
        "dacite>=1.8.1"
    ],
    extras_require={
        "tests": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.23.2",
            "polyfactory>=2.5.0",
        ]
    }
)
