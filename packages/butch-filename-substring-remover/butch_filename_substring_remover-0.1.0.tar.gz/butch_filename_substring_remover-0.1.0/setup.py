
from setuptools import setup, find_packages

setup(
    name='butch_filename_substring_remover',
    version='0.1.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'butch-rename=butch_filename_substring_remover.main:main',
        ],
    },
    install_requires=[],
    author='Vladimir Podlevskikh',
    author_email='pypi@podlevskikh.com',
    description='A batch renaming script to remove substrings from filenames and directories.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/namebogsecret/butch_filename_substring_remover',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
