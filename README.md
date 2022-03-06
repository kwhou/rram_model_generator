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
