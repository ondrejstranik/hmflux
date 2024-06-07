# spectralCamera
Package for holominflux microscopy system
Part of the viscope development tool.


## Package installation
0a. instal [viscope](https://github.com/ondrejstranik/viscope) package
1. clone this repository on your local machine
2. start conda, activate your environment `conda activate xxx` (xxx .. name of your environment)
3. move to the package folder `cd yyy` (yyy ... name of the folder)
4. type `python -m pip install -e.`
5. instal [slmpy](https://github.com/wavefrontshaping/slmPy) package.(It is not in the setup file) In your environment typ `python -m pip install git+https://github.com/wavefrontshaping/slmPy.git`
6. instal drivers / package for allied vision camera
6.a install [Vimba X SDK](https://www.alliedvision.com/de/produktportfolio/software/vimba-x-sdk/#c13326)
6.b instal [VmbPy] package.(It is not in the setup file) In your environment type `python -m pip install git+https://github.com/alliedvision/VmbPy.git`
