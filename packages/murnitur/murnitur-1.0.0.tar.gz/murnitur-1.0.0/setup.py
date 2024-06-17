from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as readme_file:
    long_description = readme_file.read()


setup(
    name="murnitur",
    version="1.0.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Caleb Okpara",
    author_email="support@murnitur.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "openlit",
        "deepeval",
        "transformers>=4.39.3",
        "pandas",
        "vaderSentiment",
        "openai",
    ],
    python_requires=">=3.7.1",
)
