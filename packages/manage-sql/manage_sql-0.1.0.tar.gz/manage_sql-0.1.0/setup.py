from setuptools import setup, find_packages

setup(
    name='manage-sql',
    version='0.1.0',
    author='Web Tech',
    author_email='zoidycine@gmail.com',
    description='Projecto simples para gestão de base de dados SQLite',
    long_description=open('README.md', 'r', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/webtechmoz/manage-sql',
    packages=find_packages(),
    keywords=['manage-sql','sqlite','sqlite manager'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)