from setuptools import setup, find_packages

setup(
    name='model_uploader',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'psycopg2-binary',
    ],
    author='Sunil',
    author_email='sunilrudrakumar@gmail.com',
    description='A package to upload models and store in PostgreSQL',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SunilRudraKumar/model_uploader.git',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
