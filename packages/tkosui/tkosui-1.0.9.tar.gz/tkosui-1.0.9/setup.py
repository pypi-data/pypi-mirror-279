from setuptools import setup

# Read the current version from the file
with open('version.txt', 'r') as file:
    current_version = file.read().strip()

# Split the version into major, minor, and patch parts
major, minor, patch = map(int, current_version.split('.'))

# Increment the patch version
patch += 1

# Check for reset conditions
if patch == 10:
    patch = 0
    minor += 1

if minor == 10:
    minor = 0
    major += 1

# Create the new version string
new_version = f"{major}.{minor}.{patch}"

# Write the updated version back to the file
with open('version.txt', 'w') as file:
    file.write(new_version)

# Use the setup function for your package configuration
setup(
    name='tkosui',
    version=new_version,
    author='ElliNet13',
    author_email='ellinet13@googlegroups.com',
    description='This library lets for ask for user input with GUI.',
    long_description='This library lets for ask for user input with GUI easily.',
    long_description_content_type='text/markdown',
    url='https://github.com/ElliNet13/tk-osui',
    packages=['tkosui'],
    classifiers=[
        
    ],
    install_requires=[
        
    ],
)
