from setuptools import setup, find_packages

long_description = open("README.md", "r").read()

setup(
    name="order_followup",
    version="1.0.4",
    description="Exports a cvs file of email subscribers using the Shopify API",
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
    # entry_points={
    #     'console_scripts': [
    #         'order-followup=order_followup.main:main',
    #     ],
    # },    

)