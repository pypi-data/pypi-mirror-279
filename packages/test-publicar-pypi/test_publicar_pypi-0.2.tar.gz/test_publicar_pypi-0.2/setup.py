from setuptools import setup, find_packages

setup(
    name='test_publicar_pypi',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        # Añade las dependencias aquí, por ejemplo:
        # 'numpy',
    ],
    author='Lucas',
    author_email='ing.lucasbracamonte@gmail.com',
    description='Es un test para mostrar como publicar',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/lucbra21/publicarPyPI',  # URL de tu proyecto
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)