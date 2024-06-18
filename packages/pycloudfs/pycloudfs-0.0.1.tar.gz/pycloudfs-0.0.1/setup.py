from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pycloudfs",
    version="0.0.1",
    description="Python wrapper for cloud storage APIs",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WadhwaniAI/PyCloudFS",
    author="Wadhwani Institute for Artificial Intelligence",
    author_email="samarth@wadhwaniai.org",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
    install_requires=[  "boto3>=1.34.54",
                        "botocore>=1.34.54,",
                        "google-api-core>=2.18.0",
                        "google-auth>=2.29.0",
                        "google-cloud-core>=2.4.1",
                        "google-cloud-storage>=2.16.0",],    
    extras_require={
        "dev": ["ipykernel>=6.29.3", "jupyter_client>=8.6.1", "twine>=5.1.0"],
    },
    python_requires=">=3.10",
)