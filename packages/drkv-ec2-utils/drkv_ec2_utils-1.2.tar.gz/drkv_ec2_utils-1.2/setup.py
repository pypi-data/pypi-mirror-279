from setuptools import setup, find_packages

setup(
    name='drkv_ec2_utils',
    version='1.2',
    author="drkv - Duesseldorf - Germany",
    author_email="m.kirchhof@drkv.com",
    description="Python module to onboard the EC2 Utils Library",
    url='https://github.com/drkv-com/ec2-utils',
    download_url='https://github.com/drkv-com/ec2-utils/archive/refs/tags/v0.1.0.tar.gz',
    packages=find_packages(),
    install_requires=[
        "boto3 >= 1.28.10",
        "pycryptodome >= 3.20.0",
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)