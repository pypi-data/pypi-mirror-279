from setuptools import setup, find_packages

setup(
    name='my_chatbot_package',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'mylibrary',  # replace with the actual name of your library if different
    ],
    entry_points={
        'console_scripts': [
            'run-chatbot=my_chatbot.app:main',
        ],
    },
    package_data={
        'my_chatbot': [
            'templates/*.html',
            'static/css/*.css',
            'static/js/*.js',
            'static/images/*.png',
        ],
    },
    author='Your Name',
    author_email='your_email@example.com',
    description='A chatbot package for library inquiries',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_chatbot_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
