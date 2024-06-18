from setuptools import setup, Extension

module = Extension('pacflymath', sources=['pacflymath/math.cpp'])

def readme():
    with open('README.rst', 'r') as f:
        return f.read()

setup(
    name='pacflymath',
    version='0.0.1',
    description='A math library written in C(++)',
    long_description=readme(),
    author='pacfly',
    author_email='pacflypy@outlook.com',
    url='https://github.com/pacfly/pacflymath',
    ext_modules=[module]
)