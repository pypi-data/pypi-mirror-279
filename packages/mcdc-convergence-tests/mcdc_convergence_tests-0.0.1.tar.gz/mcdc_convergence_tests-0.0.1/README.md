# mcdc_convergence_tests
Runs mcdc on given tests and plots convergence to benchmark data
## Dependencies
requires `numpy`,`hdf5`,and `mcdc`
## Installation guide
Download the `src` folder
## Quick start guide
The most user-friendly way of running the tests is as follows:
```
python -c 'import run; run.test([particlenums],"sourcetype",createdata,loud)' --mode=numba
```
where `particlenums` are the amounts of particles you'd like to use (e.g. `[1e2,1e3,1e4,1e5]`), and `sourcetype` is one of
```
"plane_IC"
"square_IC"
"square_source"
"gaussian_IC"
"gaussian_source"
"all"
```
`createdata` allows you to specify whether you want to run the mcdc simulations again, or use existing data (this is best used when you have run it with `createdata = True` once, then want to reuse that data without taking the time to compute it)
`loud` determines whether convergence is determined and plotted
`--mode=numba` makes computation much quicker, though this can be omitted and mcdc will run in normal python mode

IMPORTANT NOTE:

With the current implementation of MC/DC, the inclusion of `--mode=numba` is the only way to run in numba mode. This poses a problem when trying to run multiple simluations from one script, and so we recommend refraining from using the `all` option to create data, instead specifying each source. The `all` command can still be used to plot all the data with no problems. 
