from setuptools import setup, find_packages

setup(
    name='KISSAI',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'scikit-learn','pandas','numpy','requests','psycopg2-binary','pymysql','pymongo'
    ],
    description='Kiss the AI',
    author='Kartik Murali',
    author_email='kartik.m@avasoft.com',
    url='https://github.com/yourusername/my_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
