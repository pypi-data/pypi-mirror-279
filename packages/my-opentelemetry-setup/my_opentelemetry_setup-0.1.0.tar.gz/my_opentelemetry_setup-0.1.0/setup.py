from setuptools import setup, find_packages

setup(
    name="my_opentelemetry_setup",
    version="0.1.0",
    description="A package to setup OpenTelemetry for LangChain projects",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="",
    author_email="",
    url="https://github.com/eliazulai29/my_opentelemetry_setup.git",
    packages=find_packages(),
    install_requires=[
        "opentelemetry-api",
        "opentelemetry-sdk",
        "opentelemetry-exporter-otlp-proto-grpc",
        "phoenix-trace-langchain"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
