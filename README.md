# RRAM Model Generator

![NTHU LARC Logo](images/nthu_larc_logo.png?raw=true)

## Usage

1. Show the help message.
```
$ python rram_model_generator.py --help
```

2. Generate a complete 256 x 512 array.
```
$ python rram_model_generator.py --row 256 --col 512 --mode all
```

3. Generate a 256 x 512 array that has only column 0-5 and 506-511, with other columns replaced by the Pi model.
```
$ python rram_model_generator.py --row 256 --col 512 --mode cols --gen_col 6
```

## Citation

If you use this code in your work, please cite the following paper.
```
K.-W. Hou, H.-H. Cheng,  C. Tung, C.-W. Wu and J.-M. Lu, "Fault Modeling and Testing of Memristor-Based Spiking Neural Networks", in Proc. IEEE Int. Test Conf. (ITC), Anaheim, Sept. 2022.
```
