from distutils.core import setup

setup(
    name='juxte-utils',                                         # Nombre del paquete
    packages=['juxteutils'],                                    # Folder del paquete
    version='0.1',                                              # Version de la libreria
    license='MIT',                                              # Licencia
    description='Juxte functions',                              # Breve descripcion de la libreria
    author='Xavi G. Sunyer',
    author_email='webmaster@basketme.com',
    url='https://github.com/xavigs',                            # Url del sitio web o de Github
    download_url='',                                            # Link del repositorio de la libreria
    keywords=[],                                                # Keywords para definir el paquete/libreria
    install_requires=[                                          # Dependencias que se requieran instalar
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',          # Estados del paquete "3 - Alpha", "4 - Beta", "5 - Production/Stable"
        'Intended Audience :: Developers',                      # Definir cual es el publico al que va dirigido el paquete
        'License :: OSI Approved :: MIT License',               # Licencia
        'Programming Language :: Python :: 3',                  # Especificar las versiones de python que soportan el paquete
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)