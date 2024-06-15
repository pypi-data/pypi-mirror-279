from setuptools import setup, find_packages

setup(
    name='clause_analysis',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'nltk',
    ],
    entry_points={
        'console_scripts': [
            'clause_analyzer = clause_analysis.clause_analyzer:main',
            'passive_tense_classifier = clause_analysis.passive_tense_classifier:main',
            'tense_analyzer = clause_analysis.tense_analyzer:main',
        ],
    },
    author='Kritpofrankss',
    author_email='Krit.poshakrishna@gmail.com',
    description='A library to analyze clauses and classify tenses.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Kritpofrankss/clause_analysis',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
