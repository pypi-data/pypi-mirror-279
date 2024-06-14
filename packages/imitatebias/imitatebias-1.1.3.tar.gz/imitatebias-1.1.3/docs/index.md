# Welcome to imitatebias!

This package offers methods for selection bias identification and mitigation under the assumption that no ground truth is available or known.

Machine Learning typically assumes that training and test set are independently drawn from the same distribution, but this assumption is often violated in practice which creates a bias. Many attempts to identify and mitigate this bias have been proposed, but they usually rely on ground-truth information. But what if the researcher is not even aware of the bias?

In contrast to prior work, we introduce new methods, IMITATE, MIMIC, and CANCELS, to identify and mitigate Selection Bias in the case that we may not know if (and where) a bias is present, and hence no ground-truth information is available.

Those methods investigate the dataset's probability density, then add generated points or points selected from a pool in order to smooth out the density. While IMITATE models the data as a bias-aware multivariate Gaussian, the most common density occurring in real-world applications, MIMIC aims for a bias-aware Gaussian Mixture Model. If the artificial points focus on certain areas and are not widespread, this could indicate a Selection Bias where these areas are underrepresented in the sample.

CANCELS is a unique version of IMITATE specifically designed to work in the Chemical Compound Space. It uses Principal Component Analysis to reduce the dimensionality of typically sparsely distributed or binary feature representations of chemical compounds, and applies IMITATE in PCA-space. Rather than generating points to mitigate the identified selection bias, CANCELS selects from a pool of candidate compounds ensuring that they are feasible compounds.

## Installation
Please note that imitatebias is available as a PyPI package. To install it, use
```
pip install imitatebias
```
and follow the examples in our documentation.

## API Documentation and Examples

* [IMITATE](/imitatebias/imitate/) to fit one multivariate Gaussian to a real-valued tabular dataset.
* [MIMIC](/imitatebias/mimic/) to fit a multivariate Gaussian mixture model to a real-valued tabular dataset where multiple clusters are to be expected.
* [CANCELS](/imitatebias/cancels/) is specifically designed for chemical compound datasets.
* [Data and Bias Generators](/imitatebias/generators/) let you generate biased datasets to try out the methods.

## Citation

If you use this package in your research, please cite the corresponding papers.

[IMITATE](https://ieeexplore.ieee.org/document/9338355):
```
Katharina Dost, Katerina Taskova, Patricia Riddle, and Jörg Wicker.
"Your Best Guess When You Know Nothing: Identification and Mitigation of Selection Bias."
In: 2020 IEEE International Conference on Data Mining (ICDM), pp. 996-1001, IEEE, 2020, ISSN: 2374-8486.
```

[MIMIC](https://link.springer.com/chapter/10.1007/978-3-031-05936-0_12):
```
Katharina Dost, Hamish Duncanson, Ioannis Ziogas, Patricia Riddle, and Jörg Wicker.
"Divide and Imitate: Multi-Cluster Identification and Mitigation of Selection Bias."
In: Advances in Knowledge Discovery and Data Mining - 26th Pacific-Asia Conference, PAKDD 2022. 
Lecture Notes in Computer Science, vol. 13281, pp. 149-160. Springer, Cham (2022).
```

[CANCELS](https://doi.org/10.21203/rs.3.rs-2133331/v1):
```
Katharina Dost, Zac Pullar-Strecker, Liam Brydon, Kunyang Zhang, Jasmin Hafner, Patricia Riddle, and Jörg Wicker.
"Combatting Over-Specialization Bias in Growing Chemical Databases."
05 October 2022, PREPRINT (Version 1) available at Research Square [https://doi.org/10.21203/rs.3.rs-2133331/v1]
```

## More Information
If you would like more information on our projects, please have a look at the individual repositories for [IMITATE](https://github.com/KatDost/Imitate), [MIMIC](https://github.com/KatDost/Mimic) and [CANCELS](https://github.com/KatDost/Cancels) containing all experiments and results presented in the papers. 

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.