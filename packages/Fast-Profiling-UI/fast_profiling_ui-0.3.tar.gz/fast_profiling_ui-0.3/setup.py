from setuptools import setup, find_packages

VERSION = '0.3'

# Read the contents of your README file
with open("README.md", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    name='Fast_Profiling_UI',
    version=VERSION,
    description='An Exploratory Data Analysis Package for Data Engineers With UI',
    long_description=long_description,
    long_description_content_type='text/plain',  # Specify the format of the long description
    author='Mukesh',
    # author_email='your_email@example.com',  # Optional but recommended
    # url='https://github.com/yourusername/Fast_Profiling_UI',  # Optional but recommended
    packages=find_packages(),  # Automatically find packages
    install_requires=[
        'pandas',
        'numpy'
    ],  # Remove tkinter from dependencies
    keywords=['python', 'pandas', 'numpy', 'tkinter', 'eda', 'data analysis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",  # Example license
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',  # Specify your required Python versions
)
