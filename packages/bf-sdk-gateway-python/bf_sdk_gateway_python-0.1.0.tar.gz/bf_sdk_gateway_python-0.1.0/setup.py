from setuptools import setup, find_packages

setup(
    name='bf_sdk_gateway_python',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='SDK para integração com o gateway de pagamentos bemfácil®',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Daniel Lima do Nascimento',
    author_email='daniel.nascimento@bemfacil.com.br',
    url='https://github.com/bemfacil/bf_gateway_sdk_python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)