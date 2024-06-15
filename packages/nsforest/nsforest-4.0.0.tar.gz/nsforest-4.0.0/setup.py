"""A setuptools based setup module.

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))
setup(
    name='nsforest',  # Required
    version='4.0.0',  # Required
    description='NSForest: identifying minimal markers genes for cell types',  # Required
    long_description =  "Discovery of cell type classification marker genes from single cell RNA sequencing data using NS-Forest",
    long_description_content_type='text/plain',  # Optional (see note above)
    url='https://github.com/JCVenterInstitute/NSForest',  # Optional
    author='Renee Zhang, Richard Scheuermann, Brian Aevermann, Angela Liu, Beverly Peng, Ajith V. Pankajam',  # Optional
    author_email='zhangy@jcvi.org, rscheuermann@jcvi.org, baevermann@chanzuckerberg.com, aliu@jcvi.org, bpeng@jcvi.org, ajith.viswanathanasaripankajam@nih.gov',  # Optional
    classifiers=[ 
    
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Bioinformaticians',
        'Topic :: Machine Learning :: scRNA-seq',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3'
    ],
    packages= find_packages(),  # Required
    install_requires = [
        'scanpy>=1.9.6',
    ],
)