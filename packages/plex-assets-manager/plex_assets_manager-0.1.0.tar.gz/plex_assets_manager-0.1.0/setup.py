from setuptools import setup, find_packages

setup(
    name='plex_assets_manager',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'plexapi',
        'cinemagoer',
        'yt-dlp',
        'phantomjs',
        'argparse',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'plex_assets_manager=plex_assets_manager.main:main',
        ],
    },
    author='Kiritee Konark Mishra',
    author_email='konark@gmail.com',
    description='A Python project for managing and organizing Plex media library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/plex_extension',  # Replace with your repo link
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
