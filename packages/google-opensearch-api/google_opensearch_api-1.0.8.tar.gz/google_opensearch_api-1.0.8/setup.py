from setuptools import setup, find_packages

setup(
    name='google-opensearch-api',
    version='1.0.8',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
           'google-search=google_search_api.cli:main'
        ]
    },
    python_requires='>=3.6',
    author='Curious Tinker',
    author_email='hey.en.nanba@gmail.com',
    description='Python library for fetching and parsing Google search results.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CuriousTinker/GoogleOpenSearchAPI',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
