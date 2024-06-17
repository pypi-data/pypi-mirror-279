from setuptools import setup, find_packages



VERSION = '0.0.1'
DESCRIPTION = 'This is for Testing '

# Setting up
setup(
    name="test-math_mukul",
    version=VERSION,
    author="Mukul",
    author_email="mukuladhikari14@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['python'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)