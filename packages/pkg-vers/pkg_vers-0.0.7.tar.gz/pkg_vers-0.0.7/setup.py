from setuptools import setup, find_packages

setup(
    name="pkg-vers",
    version="0.0.7",
    packages=find_packages(),
    author='Charles Feinn',
    author_email='chuckfinca@gmail.com',
    description="pkg_vers is a utility that helps you determine the versions of packages imported in your Python scripts or Jupyter notebooks.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chuckfinca/pkg_vers',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'nbformat',
    ],
    entry_points={
        'console_scripts': [
            'get_versions=pkg_vers.cli:get_versions',
        ],
    },
    python_requires='>=3.8',
    license_files = ('LICENSE.txt',),
)
