from setuptools import setup

with open("README_PYPI.md", "r") as fh:
    long_description = fh.read()


setup(
    name='anikimiapi',
    packages=['anikimiapi'],
    version='0.1.2',
    license='LGPLv3+',
    description='A Simple, LightWeight, Statically-Typed Python3 API wrapper for GogoAnime',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='BaraniARR',
    author_email='baranikumar2003@outlook.com',
    url='https://github.com/BaraniARR/anikimiapi',
    download_url='https://github.com/BaraniARR/anikimiapi/releases/tag/v0.0.1-beta',
    keywords=['anime', 'gogoanime', 'download', 'sub', 'dub'],
    install_requires=[
        'bs4',
        'requests',
        'requests_html',
        'lxml'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
