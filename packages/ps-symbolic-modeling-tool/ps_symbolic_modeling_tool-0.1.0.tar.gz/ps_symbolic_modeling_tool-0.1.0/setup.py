from setuptools import setup, find_packages

setup(
    name='ps_symbolic_modeling_tool',
    version='0.1.0',
    author='Tianqi Hong, Jing Xiong',
    author_email='tianqi.hong@uga.edu, jxiong20@outlook.com',
    description='This package converts symbolic functions written in sympy to their numerical versions and also generates the Jacobian matrix.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/th1275/ps_symbolic_modeling_tool',  # Update this with your repository URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'sympy',
    ],
    entry_points={
        'console_scripts': [
            'ps_symbolic_modeling_tool=ps_symbolic_modeling_tool.cli:main',
        ],
    },
    license='LGPL-3.0-or-later',
)
