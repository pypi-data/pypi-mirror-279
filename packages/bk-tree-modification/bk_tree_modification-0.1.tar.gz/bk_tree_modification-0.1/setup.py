from setuptools import setup, find_packages

setup(
    name='bk_tree_modification',
    version='0.1',
    packages=find_packages(),
    description='A simple BK-Tree implementation for finding similar words',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Karen Arcoverde',
    author_email='arcoverdek@gmail.com',
    keywords='bktree edit distance similarity',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
