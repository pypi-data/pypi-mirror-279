from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='spw_corrosion',
    author='Antonis Mavritsakis',
    author_email='amavrits@gmail.com',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "numpy==1.26.4",
        "scipy==1.13.1",
        "xarray==2024.5.0"
        ],
    extras_require={
        "dev": []
    },
    python_requires=">=3.9.0",
    version='0.1.1',
    license='MIT',
    description='Analysis of sheep pile wall probability of failure considering corrosion.',
)