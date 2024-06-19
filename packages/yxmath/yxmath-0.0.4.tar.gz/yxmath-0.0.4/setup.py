# coding utf8
import setuptools
from yxmath.versions import get_versions

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="yxmath",
    version=get_versions(),
    author="Yuxing Xu",
    author_email="xuyuxing@mail.kib.ac.cn",
    description="Xu Yuxing's personal math tools",
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="https://github.com/SouthernCD/yxmath",
    include_package_data = True,

    # entry_points={
    #     "console_scripts": ["HugeP2G = hugep2g.cli:main"]
    # },    

    packages=setuptools.find_packages(),

    install_requires=[
        "interlap>=0.2.6",
        "networkx>=2.4",
        "yxutil>=0.0.1",
        "pingouin>=0.2.7",
        "fitter>=1.2.3",
        "scipy>=1.4.1",
        "numpy>=1.18.1",
        "matplotlib>=3.5.0",
    ],

    python_requires='>=3.5',
)