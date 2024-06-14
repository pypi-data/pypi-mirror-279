from setuptools import setup, find_packages

setup(
    name='relcli',
    version='0.2.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto3',
        'click',
        'pyperclip',
        'rich',
        'setuptools>=40.8.0',
    ],
    entry_points='''
        [console_scripts]
        dash=dashcli.dashcli:dashcli
    ''',
    author='Siddharth Rao',
    author_email='isiddharthrao@gmail.com',
    description='A custom CLI tool for managing AWS services and connecting to PostgreSQL databases',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/dashcli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
