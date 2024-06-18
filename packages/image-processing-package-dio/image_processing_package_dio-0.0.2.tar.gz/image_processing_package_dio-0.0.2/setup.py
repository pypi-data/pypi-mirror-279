from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()
    
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()
    
setup(
    name="image_processing_package_dio",
    version="0.0.2",
    author="Erick Bryan Cubas",
    author_email="datasageanalytics@gmail.com",
    description="A package for image processing.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Erick-Bryan-Cubas/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.12",
)