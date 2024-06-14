# imitatebias
This package offers methods for selection bias identification and mitigation under the assumption that no ground truth is available or known. 

Machine Learning typically assumes that training and test set are independently drawn from the same distribution, but this assumption is often violated in practice which creates a bias. Many attempts to identify and mitigate this bias have been proposed, but they usually rely on ground-truth information. But what if the researcher is not even aware of the bias?

In contrast to prior work, we introduce new methods, IMITATE, MIMIC, and CANCELS, to identify and mitigate Selection Bias in the case that we may not know if (and where) a bias is present, and hence no ground-truth information is available.

Those methods investigate the dataset's probability density, then add generated points or points selected from a pool in order to smooth out the density.
While IMITATE models the data as a bias-aware multivariate Gaussian, the most common density occurring in real-world applications, MIMIC aims for a bias-aware Gaussian Mixture Model. If the artificial points focus on certain areas and are not widespread, this could indicate a Selection Bias where these areas are underrepresented in the sample.

CANCELS is a unique version of IMITATE specifically designed to work in the Chemical Compound Space. It uses Principal Component Analysis to reduce the dimensionality of typically sparsely distributed or binary feature representations of chemical compounds, and applies IMITATE in PCA-space. Rather than generating points to mitigate the identified selection bias, CANCELS selects from a pool of candidate compounds ensuring that they are feasible compounds. 

# How to use imitatebias
Please note that imitatebias is available as a PyPI package. To install it, use
```
pip install imitatebias
```
and follow the examples in our [documentation](https://katdost.github.io/imitatebias/).

# Citation
If you want to use this implementation or cite IMITATE in your publication, please cite the following ICDM paper:
```
Katharina Dost, Katerina Taskova, Patricia Riddle, and Jörg Wicker.
"Your Best Guess When You Know Nothing: Identification and Mitigation of Selection Bias."
In: 2020 IEEE International Conference on Data Mining (ICDM), pp. 996-1001, IEEE, 2020, ISSN: 2374-8486.
```
Bibtex:
```
@INPROCEEDINGS {Dost2020,
author = {K. Dost and K. Taskova and P. Riddle and J. Wicker},
booktitle = {2020 IEEE International Conference on Data Mining (ICDM)},
title = {Your Best Guess When You Know Nothing: Identification and Mitigation of Selection Bias},
year = {2020},
pages = {996-1001},
doi = {10.1109/ICDM50108.2020.00115},
url = {https://doi.ieeecomputersociety.org/10.1109/ICDM50108.2020.00115},
publisher = {IEEE Computer Society},
address = {Los Alamitos, CA, USA},
month = {nov}
}
```

If you want to use this implementation or cite MIMIC in your publication, please cite the following PAKDD paper:
```
Katharina Dost, Hamish Duncanson, Ioannis Ziogas, Patricia Riddle, and Jörg Wicker.
"Divide and Imitate: Multi-Cluster Identification and Mitigation of Selection Bias."
In: Advances in Knowledge Discovery and Data Mining - 26th Pacific-Asia Conference, PAKDD 2022. 
Lecture Notes in Computer Science, vol. 13281, pp. 149-160. Springer, Cham (2022).
```

Bibtex:
```
@inproceedings{Dost2022,
title = {Divide and Imitate: Multi-Cluster Identification and Mitigation of Selection Bias},
author = {Katharina Dost and Hamish Duncanson and Ioannis Ziogas and Pat Riddle and J\"{o}rg Wicker},
year = {2022},
booktitle = {Advances in Knowledge Discovery and Data Mining - 26th Pacific-Asia
               Conference, {PAKDD} 2022},
series    = {Lecture Notes in Computer Science},
volume    = {13281},
pages     = {149--160},
publisher = {Springer},
address   = {Cham},
doi       = {10.1007/978-3-031-05936-0\_12},
}
```

If you would like to use and cite CANCELS in your publication, please stay tuned -- we are working on publishing it! In the meanwhile, we would appreciate a citation for our IMITATE paper or the preprint:
```
Katharina Dost, Zac Pullar-Strecker, Liam Brydon, Kunyang Zhang, Jasmin Hafner, Patricia Riddle, and Jörg Wicker.
"Combatting Over-Specialization Bias in Growing Chemical Databases."
05 October 2022, PREPRINT (Version 1) available at Research Square [https://doi.org/10.21203/rs.3.rs-2133331/v1]
```

# Further Information
If you would like more information on our projects, please have a look at the individual repositories for [IMITATE](https://github.com/KatDost/Imitate), [MIMIC](https://github.com/KatDost/Mimic) and [CANCELS](https://github.com/KatDost/Cancels) containing all experiments and results presented in the papers. 
