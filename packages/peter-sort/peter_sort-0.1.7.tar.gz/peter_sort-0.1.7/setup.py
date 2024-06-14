from setuptools import setup, find_packages

setup(
    name='peter-sort',
    version='0.1.7',
    description='Sorting methods',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/peterandrian/pypi',  # Update with your repo URL
    author='Peter Andrian Priestley',
    author_email='peter.422023020@civitas.ukrida.ac.id',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)