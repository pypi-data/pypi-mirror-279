from setuptools import setup, find_packages

setup(
    name="PyThermalAnalysis",
    version="0.1.0",
    author="Nirmal Parmar",
    author_email="nirmalparmarphd@gmail.com",
    description="A Python library for a basic exergy analysis in thermodynamic systems",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nirmalparmarphd/PyThermalAnalysis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['pandas', 'numpy'],
)
