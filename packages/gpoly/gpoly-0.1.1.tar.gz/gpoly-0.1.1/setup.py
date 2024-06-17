from setuptools import setup, find_packages

setup(packages=find_packages(),
      python_requires='>=3.12',
      install_requires=['click',
                        'cartopy',
                        'matplotlib',
                        'numpy',
                        'scikit-image',
                        ],
      entry_points={'console_scripts': ['gpoly = gpoly.gpoly:gpoly',]}
      )
