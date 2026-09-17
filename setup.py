from setuptools import setup, find_packages

# lower bounds are the versions actually tested against in Plan A's A0
# environment baseline (.venv-rdr, Python 3.11, macOS arm64), not exact
# pins (B3). datasette is dropped -- the `sql` command is disabled, so it
# was an unused dependency. spacy is now declared directly instead of
# arriving transitively via textacy/pytextrank.
setup(
license_files=["LICENSE"],
    name='reader-toolbox',
    packages=find_packages(),
    include_package_data=True,
	install_requires=[
		'catalogue>=2.0.10',
		'click>=8.5.0',
		'gensim>=4.4.0',
		'matplotlib>=3.11.2',
		'networkx>=3.6.1',
		'nltk>=3.10.3',
		'pandas>=3.0.5',
		'pytextrank>=3.3.0',
		'rdflib>=7.6.0',
		'requests>=2.34.2',
		'scikit-learn>=1.9.1',
		'scipy>=1.17.1',
		'spacy>=3.8.16',
		'srsly>=2.5.3',
		'textacy>=0.13.0',
		'tika>=3.3.2',
		'wordcloud>=1.9.6',
	],
	extras_require={
		# _download() (rdr/rdr.py) imports fsspec but is dead code -- its
		# only call site is already commented out -- so fsspec is declared
		# here rather than as a hard dependency (B3)
		'notebooks' : [ 'fsspec' ],
	},
    entry_points={ 'console_scripts': [ 'rdr = rdr.rdr:rdr' ] }
)
