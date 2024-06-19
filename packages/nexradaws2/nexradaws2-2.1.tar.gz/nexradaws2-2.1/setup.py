import os
import setuptools

# Read version and author info from ./nexradaws/__init__.py
current_file = __file__
absolute_path = os.path.abspath(current_file)
this_directory = os.path.dirname(absolute_path)
nexradaws_init_path = os.path.join(this_directory, "nexradaws2", "__init__.py")

try:
    with open(nexradaws_init_path) as f:
        for l in f.readlines():
            if l.startswith("__authors__"):
                authors = l.split("= ")[1].lstrip("(").rstrip(",)\n").replace("'", "")
            if l.startswith("__version__"):
                version = float(l.split("= ")[1].strip())
except Exception as e:
    raise
#

with open(os.path.join(this_directory, "README.md")) as f:
    long_description = f.read()

setuptools.setup(
    name='nexradaws2',
    version=version,
    packages=['nexradaws2','nexradaws2.resources'],
    description= 'Query and download NEXRAD data from AWS S3 storage.',
    long_description=long_description,
    url='https://github.com/aarande/nexradaws',
    license='MIT',
    author=authors,
    author_email='aaron.anderson74@yahoo.com',
    keywords='weather,radar,nexrad,aws,amazon',
    download_url='https://github.com/Aareon/nexradaws/archive/2.0.tar.gz',
    install_requires=['boto3','pytz','six'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
