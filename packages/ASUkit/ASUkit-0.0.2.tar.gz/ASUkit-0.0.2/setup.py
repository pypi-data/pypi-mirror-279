from setuptools import setup, find_packages

setup(
    name='ASUkit',
    version='0.0.2',
    description="toolkit for AUSnet",
    long_description=open('README.md', encoding='utf-8').read(),
    include_package_data=True,
    author='CaoBin',
    author_email='bcao686@connect.hkust-gz.edu.cn',
    maintainer='CaoBin',
    maintainer_email='bcao686@connect.hkust-gz.edu.cn',
    license='MIT License',
    packages=find_packages(),  # Automatically include all Python modules
    package_data={'ASUkit': ['CGCNN_atom_emb.json']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.5',
    install_requires=['scipy', 'ase', 'spglib','pandas', 'numpy', ],
    entry_points={
        'console_scripts': [
            '',
        ],
    },
)
