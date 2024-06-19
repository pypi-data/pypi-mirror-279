
from setuptools import setup
import os


# User-friendly description from README.md
current_directory = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(current_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except Exception:
    long_description = ''

setup(
    name = 'cptec-subsaz',
    version = '0.0.16',
    author = 'Framework CPTEC',
    author_email = 'frameworkcptec@gmail.com',
    packages = ['subsaz'],
    install_requires = ['numpy','pandas', 'xarray', 'requests','matplotlib','scipy','netCDF4'],
    description = 'Módulo para distribuição do Modelo SubSazonal do CPTEC.',
    long_description="""Framework CPTEC SubSazonal

É um pacote Python para a distribuição de dados brutos de previsão subsazonal do CPTEC/INPE 
produzidos com o modelo BAM-1.2. Os arquivos de dados contêm a média do conjunto 
(de 11 membros) para todos os produtos e variáveis mostradas no site https://subsazonal.cptec.inpe.br/.

Esses arquivos estão disponíveis como anomalias computadas referentes à climatologia 1999-2018.

Documentacao completa do Projeto - https://sazonal.readthedocs.io/en/latest/index.html

    \n""",
    long_description_content_type='text/markdown',
    url = 'https://sazonal.readthedocs.io/en/latest/index.html',
    project_urls = {
        'Código fonte': 'https://github.com/framework-CPTEC/Sazonal',
        'Download': 'https://github.com/framework-CPTEC/Sazonal'
    },
    license_files = "LICENSE.txt",
    license = 'MIT',
    keywords = 'recuperação de dados climáticos',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    python_requires='>=3.10',
)
