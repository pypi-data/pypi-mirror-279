from setuptools import setup, find_packages

setup(
    name="yajendra",
    version="1.0.0", 
    packages=find_packages(),
    license="MIT",
    description="This library is to search the best parameters across different steps of the RAG process.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # author="HiDevs",
    # author_email="hidevscommunity@gmail.com",
    # url="https://github.com/hidevscommunity/ragrid",
    install_requires=[
        "langchain>=0.1.13",
        "langchain-openai>=0.1.1",
        "trulens-eval>=0.27.0",
        "chromadb>=0.4.24",
        "sentence-transformers>=2.6.1",
        "unstructured[pdf]>=0.13.0",
    ],
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
)
