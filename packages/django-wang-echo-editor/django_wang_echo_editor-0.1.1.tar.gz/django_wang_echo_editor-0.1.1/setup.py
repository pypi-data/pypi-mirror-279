from setuptools import setup, find_packages

setup(
    name='django_wang_echo_editor',
    version='0.1.1',
    packages=find_packages(
        include=['wang_editor']
    ),
    include_package_data=True,
    license='MIT License',
    description='Django Admin 中使用 wangEditor 富文本编辑器',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Echo Chu',
    author_email='395150457@qq.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django-js-asset',
    ]
)
