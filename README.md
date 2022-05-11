# 3D-Voxel-Gen

This is a project that focusing on automatic generation of 3d voxel-based models.

## Quick Start

### Install

This project working on Python 3.6 and later version.

Then clone the repo and do the following

```shell
cd 3d-voxel-gen
pip install -r requirements.txt
```

### Preprocess

In order to train the model, data pre-process is needed.

Currently, the project only accept the input data in 0.98 version [Magical-Voxel](https://ephtracy.github.io/)’s vox file.

The `preprocess.py` takes input of vox file as input and will create `output.json` file in the home folder. The json file contains transformed 3d-model that can be processed by the neural network.

### Training

Google Colab is highly recommend to use when training the data.

Please creating your colab and using `colab.ipynb` to train your neural network.

The generated `output.json` is the input for the neural network, put is in the home directory of Google Colab to let the program read it. The generated trained model (in h5 file format) will be put in the home folder too.

### Generation

The generation code piece can be found in `colab.ipynb`, put the trained h5 model in `./wei/` to let the program read.

Then, there are provided tools for generation and gif recording. (Both pytorch and tensorflow version are provided). Default seed is the center of the 32x32x32 space, you can modify for add more seed if you like.

## About

This repo is not finished yet, might be some bugs when you run the code.

The code of neural net-work part takes is modified from [Growing Neural Cellular Automata](https://distill.pub/2020/growing-ca/), and the 3d part is build on top of [hybrid-nca-evocraft](https://github.com/hugcis/hybrid-nca-evocraft), checking their web-page for detailed explanation. 

The picture below shows the process of how this repo works.

<img src="https://github.com/midstreeeam/3d-voxel-gen/blob/main/images/process.png?raw=true" alt="window" style="zoom:70%;" />
