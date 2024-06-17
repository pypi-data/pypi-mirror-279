from setuptools import setup, find_packages
import os

# Cargar el contenido de README.md para la descripción larga
def load_long_description():
    readme_path = 'README.md'
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "Short description of the package"
    
setup(
    name='lili_activation',
    version='0.1.1',
    author='Lili Chen',
    author_email='lilichen577@gmail.com',
    packages=find_packages(),
    description='A custom non-monotonic activation function',
    long_description=load_long_description(),
    long_description_content_type='text/markdown',
    install_requires=[
        'tensorflow>=2.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
)
