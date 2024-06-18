from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="exponentation",
    version="1.0.0",
    author="katya_r",
    author_email="katerina.riabova@gmail.com",
    description="This is a computational library based on AI for optimal exponentiation.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Katyana01/Library.git",
    packages=find_packages(),
    install_requires=["pandas", "torch", "numpy"],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="files speedfiles ",
    project_urls={"GitHub": "https://github.com/Katyana01/Library"},
    python_requires=">=3.9",
    include_package_data=True,
    package_data={"exponentation": ["data/Data_learning.csv", "data/my_model.pth"]},
)
