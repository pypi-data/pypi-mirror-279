from setuptools import setup, find_packages

setup(
    name='codegyan',
    version='1.0.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'requests',
    ],
    author='Prathmesh Yelne',
    author_email='prathmeshyelne@codegyan.in',
    description='A Python library to interact with the Codegyan API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Codegyan-LLC/codegyan-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords=['codegyan', 'api', 'codex', 'client', 'sdk', 'prathmeshyelne'],
    python_requires='>=3.6',
)
