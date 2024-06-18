from setuptools import setup, find_packages
import os

''' 
# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
 
# Function to read the README file
def read_readme():
    with open('README.txt') as f:
        return f.read()
 
# Package data specification
package_data = {
    '': ['Infrastructure/Environment/*', 'Infrastructure/Search/*', 'Python Scripts/*', 'Maps/*'],
}
 
# Automatically include all packages
packages = find_packages()
 
setup(
    name='RRFI',
    version='0.1.0',
    packages=packages,
    include_package_data=True,
    package_data=package_data,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            # Define console scripts if needed
        ],
    },
    author='Virajith Murali',
    author_email='virajith.murali@defra.gov.uk',
    description='A brief description of your project',
    long_description=read_readme(),
    long_description_content_type='text/plain',
    url='https://github.com/Jithh/RRFI',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11.5',
)
'''
with open('requirements.txt') as f:
    requirements= f.read().splitlines()
 
setup(
    name="rrfi-scripts",
    version="1.0.0",
    packages=find_packages(where="Python Scripts"),
    install_requires=requirements,
    scripts=[
        "Python Scripts/Excel Metadata Extraction.py",
        "Python Scripts/GIS GDB.py",
        "Python Scripts/GIS SHP.py",
        "Python Scripts/Image Metadata Extraction.py",
        "Python Scripts/PDF Extraction.py",
        "Python Scripts/PPT Extraction.py",
        "Python Scripts/videos.py",
        "Python Scripts/Worddoc Extraction.py",
    ],
    author="Virajith Murali",
    description="Scripts for RRFI POC",
    long_description=open('Python Scripts/README.txt').read(),
    long_description_content_type='text/plain',
    url="https://github.com/Jithh/RRFI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)