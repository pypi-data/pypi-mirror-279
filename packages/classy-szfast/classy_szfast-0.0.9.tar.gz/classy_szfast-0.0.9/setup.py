from setuptools import setup, find_packages
import os
import sys
import shutil

# # Determine the library folder and requirements path
# thelibFolder = os.path.dirname(os.path.realpath(__file__))
# requirementPath = os.path.join(thelibFolder, 'requirements.txt')

# # Read the requirements from the requirements.txt file
# install_requires = []
# if os.path.isfile(requirementPath):
#     with open(requirementPath) as f:
#         print('opening requirements ', requirementPath)
#         install_requires = f.read().splitlines()

# # Read the long description from the README.md file
# def read_file(file):
#     with open(file) as f:
#         return f.read()

# long_description = read_file("README.md")

# # Determine whether the system is M1/M2 Mac and adjust TensorFlow dependency
# tensorflow = 'tensorflow'
# if 'arm' in os.uname().machine:
#     tensorflow = 'tensorflow-metal'

# Add TensorFlow to the install_requires list
# install_requires.append(tensorflow)

# Setup configuration
setup(
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research'
    ],
    name="classy_szfast",
    version="0.0.9",
    description="Python package for fast class_sz",
    # long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False,
    packages=find_packages(),
    author="Boris Bolliet, Ola Kusiak",
    author_email="bb667@cam.ac.uk, akk2175@columbia.edu",
    url='https://github.com/CLASS-SZ/classy_szfast',
    download_url='https://github.com/CLASS-SZ/classy_szfast',
    package_data={},
    install_requires=["setuptools", "wheel", "numpy>=1.19.0", "Cython>=0.29.21", "tensorflow==2.13.0", "tensorflow-probability==0.21.0", "cosmopower", "mcfit"],
)

# # Clean up build artifacts
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
# shutil.rmtree("build", True)
# shutil.rmtree("classy_szfast.egg-info", True)
# shutil.rmtree("__pycache__", True)
# shutil.rmtree(".pytest_cache", True)