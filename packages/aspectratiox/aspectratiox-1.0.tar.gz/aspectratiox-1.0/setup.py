from setuptools import setup

setup(
    name='aspectratiox',
    version='1.0',
    py_modules=['aspectratiox.main'],
    entry_points={
        'console_scripts': [
            'aspectratiox = aspectratiox.main:main',
        ],
    },
    author='Avinion Group',
    author_email='shizofrin@gmail.com',
    description='Aspect ratio conversion tool for images using ffmpeg.',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://x.com/Lanaev0li',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
