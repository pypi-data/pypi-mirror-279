from setuptools import setup, find_packages

setup(
    name='rasifal',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'rasifal = rasifal.main:main',
            # 'rasifal = flutter_smartstart.cli:main', 
        ],
    },
    author='Kapil Bhandari',
    author_email='iam.bkpl031@gmail.com',
    description='A CLI tool to find horoscope in nepali',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/iam-bkpl/rasifal',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)