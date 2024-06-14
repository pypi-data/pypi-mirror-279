from setuptools import setup, find_packages

setup(
    name='televisor',
    version='0.0.1',
    license='Apache 2.0',
    author='Zeio Nara',
    author_email='zeionara@gmail.com',
    packages=find_packages(),
    description='A tool for sending videos to telegram chats',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/zeionara/televisor',
    project_urls={
        'Documentation': 'https://github.com/zeionara/televisor#readme',
        'Bug Reports': 'https://github.com/zeionara/televisor/issues',
        'Source Code': 'https://github.com/zeionara/televisor'
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.12"
    ],
    install_requires = ['click', 'python-telegram-bot']
)
