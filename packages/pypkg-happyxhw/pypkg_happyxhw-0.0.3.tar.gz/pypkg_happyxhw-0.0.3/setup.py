from setuptools import find_packages, setup

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='pypkg-happyxhw',
    version='0.0.3',
    author='happyxhw',
    author_email='happyxhw@outlook.com',
    description='python useful package',
    url='https://git.happyxhw.cn:8443/happyxhw/pypkg.git',
    packages=find_packages(),
    install_requires=install_requires,
)
