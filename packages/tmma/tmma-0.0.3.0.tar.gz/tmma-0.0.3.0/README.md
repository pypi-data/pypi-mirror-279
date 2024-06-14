# Transfer Matrix Method for Acoustics (TMMA)

Toolbox for design and prediction of multilayered acoustic treatments. Also contains a material model based on the GRAS database.

## Acknowledgement

This repository is a fork from from [rinaldipp/tmm](https://github.com/rinaldipp/tmm).
Its purpose is to rename the `tmm` package to `tmma`,
making it possible to upload it to the [https://pypi.org](https://pypi.org) while
following the original repository as closely as possible.
The name `tmm` cannot be used on [https://pypi.org](https://pypi.org)
because a package with that name [already exists](https://pypi.org/project/tmm/).

## Installation

```
pip install tmma
```

## Example

```python
from tmma.tmm import TMM

# Define the frequency range, resolution and sound incidence
treatment = TMM(fmin=20, fmax=5000, df=1, incidence="diffuse", incidence_angle=[0, 78, 1],
                filename="example_perforated_resonator")

# Define the layers - from top to bottom
treatment.perforated_panel_layer(t=19, d=8, s=24, method="barrier")
treatment.porous_layer(model="mac", t=50, sigma=27)
treatment.air_layer(t=50)

# Compute, plot and export data
treatment.compute(rigid_backing=True, show_layers=True)
treatment.plot(plots=["alpha"], save_fig=True)
treatment.save2sheet(n_oct=3)
treatment.save()
bands, filtered_alpha = treatment.filter_alpha(view=True, n_oct=3)
```

For more examples see the [example files](https://github.com/jvcarli/tmma/tree/main/examples).

## References

<a id="1">[1]</a>
R. Petrolli, A. Zorzo and P. D'Antonio, ["
Comparison of measurement and prediction for acoustical treatments designed with Transfer Matrix Models
"](
https://www.researchgate.net/publication/355668614_Comparison_of_measurement_and_prediction_for_acoustical_treatments_designed_with_Transfer_Matrix_Models/references
), in *Euronoise*, October 2021.
