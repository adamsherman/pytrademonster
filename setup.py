from setuptools import setup, find_packages

setup(
    name='pytrademonster',
    version='0.11',
    url='https://github.com/adamsherman/pytrademonster',
    license='MIT',
    author='Adam Sherman',
    author_email='adam.r.sherman@gmail.com',
    description='Simple wrapper around TradeMonster/Optionhouses\' XML based API',
    packages = find_packages(),
    install_requires = [ 'ggplot >= 0.6.5','pandas >= 0.13.1', 'xmltodict >= 0.9.2', 'simple-crypt >= 4.1.0']
)
