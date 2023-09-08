# PySyun Uniswap Source


**Document Version**: 1.0.

**Author**: Syun Lee.

**Date**: 2023.09.08.

**Copyright**: https://hype.dev, 2023. All rights reserved.

**Download URI**: [pysyun_uniswap_source.pdf](./pysyun_uniswap_source.pdf)

## Functional requirements
The source class should accept the Uniswap pair address and blockchain connection settings in the constructor.

The source class should extract **reserve0** and **reserve1** values from this pair in the **process** method.
Like for any other Pysyun Pipeline sources, the **process** method should return a timeline.
In this particular case, the timeline of a single element - the current date and reserves value as a JSON document.

## Non-functional requirements
The project source code can be forked from this repository.

The library should be installable using PIP. 

The library name: "**pysyun_uniswap_source**".

The main class name: "**UniswapV2Source**".

Example source implementation (for reference):

https://github.com/pysyun/pysyun-timeline/blob/master/pysyun/timeline/filters.py#L20

The library should be tested from a Google Colab, illustrating that the functional requirements are met.
