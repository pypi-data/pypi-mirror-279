from setuptools import setup, find_packages

setup(
    name='flask111',
    version='1.0.1',
    packages=find_packages(),  # 自动查找包含 __init__.py 的包
    install_requires=[],  # 依赖的第三方库
    author='Your Name',
    author_email='your@email.com',
    description='Description of your module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_module',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
