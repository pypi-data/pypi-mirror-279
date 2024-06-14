from setuptools import setup, find_packages

setup(
    name='article_assistant',
    version='0.1.2',
    description='Draft and review articles through the use of Large Language Models (LLMs)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='alkhalifas',
    packages=find_packages(),
    install_requires=[
        'langchain',
        'langchain_openai',
        'langchain_experimental',
        'langchain_core',
        'langchain_community',
        'pandas',
        'python-docx',
        'openai',
        'PyPDF2',
    ],
)



