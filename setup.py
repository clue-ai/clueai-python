import setuptools
from setuptools.command.install import install
from setuptools.dist import Distribution

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


class InstallPlatlib(install):
    def finalize_options(self):
        install.finalize_options(self)
        if self.distribution.has_ext_modules():
            self.install_lib = self.install_platlib


class BinaryDistribution(Distribution):
    def is_pure(self) -> bool:
        return False

    def has_ext_modules(foo) -> bool:
        return True

setuptools.setup(
    name='clueai',
    version='0.0.1.6',
    author='matrix',
    author_email='brightmart@hotmail.com',
    description='A Python library for the ClueAI API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/clue-ai/clueai-python',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'Pillow'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    distclass=BinaryDistribution,
    cmdclass={'install': InstallPlatlib}
)
