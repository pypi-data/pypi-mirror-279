from setuptools import setup , find_packages 

classifiers = []

setup(
    name='tarda',
    version='0.0.10',
    description='A library for collection of IDS & robust-IDS and tools for evaluating them',
    long_description=open("README.md").read() + '\n\n' + open("CHANGELOG.txt").read(),
    long_description_content_type = "text/markdown",
    url='https://github.com/spg-iitd/tardigrade',
    author='Ravi Ranjan Singh',
    author_email='raviranjans821@gmail.com',
    license='MIT',
    include_package_data=True,
    # classifiers=classifiers,
    keywords='ids adversarial network nids',
    packages= find_packages(),
    install_requires=['scapy', 'numpy', 'pandas', 'matplotlib', 'scikit-learn', 'scipy', 'tqdm', 'torch', 'torchvision', 'torchsummary', 'torchattacks'],
    zip_safe=False
)
