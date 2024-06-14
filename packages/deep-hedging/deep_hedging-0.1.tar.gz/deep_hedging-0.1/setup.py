from distutils.core import setup

setup(
    name='deep_hedging',
    packages=['deep_hedging'],
    version='0.1',
    license='MIT',
    description='Hedging Derivatives Under Incomplete Markets with Deep Learning',
    author='Viacheslav Buchkov',
    author_email='viacheslav.buchkov@gmail.com',
    url='https://github.com/v-buchkov/deep-hedging',
    download_url='https://github.com/v-buchkov/deep-hedging/archive/refs/tags/v_01.tar.gz',
    keywords=['deep hedging', 'derivatives', 'hedging', 'deep learning', 'reinforcement learning'],
    install_requires=[
        'numpy',
        'pandas',
        'torch',
        'matplotlib',
        'tqdm',
        'IPython',
        'yfinance',
        'gym'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
