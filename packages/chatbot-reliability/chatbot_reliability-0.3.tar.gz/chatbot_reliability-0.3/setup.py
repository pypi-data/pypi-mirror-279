from setuptools import setup, find_packages

setup(
    name='chatbot_reliability',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'nltk', 'inflect', 'sentence_transformers', 'scikit-learn'
    ],
)
