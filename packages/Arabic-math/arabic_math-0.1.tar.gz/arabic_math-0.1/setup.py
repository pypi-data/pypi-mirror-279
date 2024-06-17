from setuptools import setup, find_packages

# Define the setup parameters for your package
setup(
    name='Arabic_math',  # Package name
    version='0.1',  # Package version
    packages=find_packages(),  # Automatically find all packages and sub-packages
    install_requires=[
        # List any dependencies required by your package here
        'requests',  # Example depend
        'numpy',
        'pandas'
    ],
    python_requires='>=3.6',  # Specify the Python version required by your package
    author='someguy',  # Author's name
    author_email='someguy@gmail.com',  # Author's email address
    description='arabic_basic_math',  # Short description of your package
    license='MIT',  # License type (e.g., MIT, GPL)
)
