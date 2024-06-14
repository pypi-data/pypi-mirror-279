# OSL-ActionSpotting: A Unified Library for Action Spotting in Sports Videos

[![ArXiv](https://img.shields.io/badge/arXiv-xxx.xxx-b31b1b.svg?style=flat)](https://arxiv.org/abs/xxx.xxx)
[![License](https://img.shields.io/badge/License-GPL_3.0-blue.svg)](https://github.com/SoccerNet/sn-spotting-pip/blob/main/LICENSE)

OSL-ActionSpotting is a plug-and-play library that unifies action
spotting algorithms.

## 🥳 What's New

- A technical report of this library will be provided soon.

## 📖 Major Features

- **Support SoTA TAD methods with modular design.** We decompose the TAD pipeline into different components, and implement them in a modular way. This design makes it easy to implement new methods and reproduce existing methods.
- **Support multiple datasets.** We support new datasets by giving a intermediate JSON format.
- **Support feature-based training and end-to-end training.** The feature-based training can easily be extended to end-to-end training with raw video input, and the video backbone can be easily replaced.

## 🌟 Model Zoo

| Feature based | End to end |
|:-------------:|:----------:|
| [AvgPool](https://arxiv.org/pdf/1804.04527.pdf)   | [E2E-Spot](https://arxiv.org/pdf/2207.10213.pdf) |
| [MaxPool](https://arxiv.org/pdf/1804.04527.pdf)   |                                                  |
| [NetVLAD](https://arxiv.org/pdf/1804.04527.pdf)   |                                                  |
| [NetRVLAD](https://arxiv.org/pdf/1804.04527.pdf)  |                                                  |
| [CALF](https://arxiv.org/pdf/1912.01326.pdf)      |                                                  |
| [AvgPool++](https://arxiv.org/pdf/2104.06779.pdf) |                                                  |
| [MaxPool++](https://arxiv.org/pdf/2104.06779.pdf) |                                                  |
| [NetVLAD++](https://arxiv.org/pdf/2104.06779.pdf) |                                                  |
| [NetRVLAD++](https://arxiv.org/pdf/2104.06779.pdf)|                                                  |

## 🛠️ Installation

Please refer to [install.md](docs/install.md) for installation and data preparation.

## 🚀 Usage

Please refer to [usage.md](docs/usage.md) for details of training and evaluation scripts.

## 🤝 Roadmap

All the things that need to be done in the future is in [roadmap.md](docs/en/roadmap.md).

## 🖊️ Citation

If you think this repo is helpful, please cite us:

```bibtex
@misc{name,
    title={},
    author={},
    howpublished = {\url{https://github.com/OpenSportsLab/OSL-ActionSpotting}},
    year={2024}
}
```

If you have any questions, please contact: `yassine.benzakour@student.uliege.be`.
