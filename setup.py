from distutils.core import setup
import synopsitv

setup(
    name='SynopsiTv',
    author='Jaromir Fojtu',
    author_email='jaromir.fojtu@gmail.com',
    version=synopsitv.__version__,
    url='https://github.com/syntaxsugar/SynopsiTv',
    license='BSD',
    description='A command-line utility to communicate with synopsi.tv API',
    long_description=open('README.md').read(),
    packages=['synopsitv', ],
    scripts=['bin/synopsitv.py',],
    requires=['requests'],

)
