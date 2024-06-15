from setuptools import setup, find_packages

long_description = open("README.md", "r").read()

setup(
    name="order_followup",
    version="1.0.5",
    description="Exports a csv file of email subscribers using the Shopify API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Russ Nastala",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[
    'pytz==2024.1',
    'requests==2.32.3',
    'ShopifyAPI==12.5.0',
],
    python_requires="~=3.8", 

)