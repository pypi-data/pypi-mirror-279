from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


VERSION = '2.11.1'


setup(
    name='interpretableai',
    version=VERSION,
    description='Interface to Interpretable AI modules in Python',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://docs.interpretable.ai/stable/IAI-Python/',
    author='Interpretable AI',
    author_email='info@interpretable.ai',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
    ],
    packages=['interpretableai'],
    install_requires=[
        'julia>=0.6.2',
        'pandas>=0.24',
        'appdirs>=1.4.3',
        'future',
    ],
    python_requires='>=3.9',
    include_package_data=True,
    zip_safe=False,
)
