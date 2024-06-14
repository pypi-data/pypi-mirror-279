from imitatebias.mimic import *
from sklearn.decomposition import PCA

class Cancels:
    """Cancels selects additional points/compounds to mitigate a bias.
    
    Given a pool of potential candidates to be added to a dataset,
    Cancels investigates the dataset's distribution and selects those points
    or compounds that mitigate the dataset's bias without losing its 
    specialization to its domain. See our paper [1]_ for details.
    
    Attributes
    ----------
    n_pc : int (> 0)
        Controls the number of Principal Components used in PCA to decrease
        the dataset dimensionality.
    imi : `Imitate`
        Imitate object containing all information about the fitted multi-
        variate Gaussian indicating a potential bias.
    pca : sklearn.decomposition.PCA
        Stores the trained PCA transformation.
    d_trf : numpy.ndarray (2D)
        The PCA-transformed input dataset.
    
    Methods
    -------
    fit(data, bounding_pool=None, bounding_range=None, strength=1000)
        Fits the Cancels method to a dataset.
    score(pool)
        Scores all points / compounds in a pool.
    augment(pool)
        Selects compounds from the pool that mitigate the bias.

    References
    ----------
    .. [1] Katharina Dost, Zac Pullar-Strecker, Liam Brydon, Kunyang Zhang, Jasmin Hafner, 
       Patricia Riddle, and Jörg Wicker. "Combatting Over-Specialization Bias in Growing 
       Chemical Databases." 05 October 2022, PREPRINT (Version 1) available at Research 
       Square [https://doi.org/10.21203/rs.3.rs-2133331/v1]
        
    Examples
    --------
    >>> from imitatebias.generators import *
    >>> from imitatebias.cancels import *
    >>> import matplotlib.pyplot as plt
    >>> import seaborn as sns

    generate data and pool
    >>> X, y = generateData(500, 1, 10, seed=2210)
    >>> X_b, _, _ = generateBias(X, y, 1, seed=2210)

    fit Cancels
    >>> can = Cancels(n_pc=2)
    >>> can.fit(X_b)

    generate data points to fill in the bias (for the sake of visualization)
    >>> gen_p, _ = can.imi.augment()

    plot Cancels' indicated biases in PCA space
    >>> plt.scatter(can.pca.transform(X_b)[:,0], can.pca.transform(X_b)[:,1])
    >>> sns.kdeplot(x=gen_p[:,0], y=gen_p[:,1], cut=10, thresh=0, cmap='Greens')
    >>> plt.show()

    score the pool
    >>> scores = can.score(pool)

    plot the pool's scores in PCA space
    >>> plt.scatter(can.pca.transform(pool)[:,0], can.pca.transform(pool)[:,1], c=scores)
    >>> plt.colorbar()
    >>> plt.show()

    create a random pool
    >>> pool = np.column_stack([np.random.uniform(min(X[:,0]), max(X[:,0]), size=1000) for i in range(len(X[0]))])

    select additional data points from the pool
    >>> pool_idcs = can.augment(pool)

    plot Cancels' indicated biases in PCA space
    >>> plt.scatter(can.pca.transform(X_b)[:,0], can.pca.transform(X_b)[:,1], label='Dataset')
    >>> plt.scatter(can.pca.transform(pool)[pool_idcs,0], can.pca.transform(pool)[pool_idcs,1], label='Added')
    >>> plt.legend()
    >>> plt.show()
    """
    
    def __init__(self, n_pc=5):
        """Cancels Constructor.
        
        Parameters
        ----------
        n_pc : int
            The number of Principal Components to be used for dimensionality
            reduction.
        """
        self.n_pc = n_pc
        self.imi = Imitate()
    
    def fit(self, data, bounding_pool=None, bounding_range=None, strength=1000):
        """Fits a bias-aware multivariate Gaussian to the dataset.
        
        After reducing the dimensionality of the dataset using PCA, a
        bias-aware multivariate Gaussian is fitted to the data using the
        Imitate algorithm. See [1]_ for details on Imitate and [2]_ for
        details on Cancels.
        
        Parameters
        ----------
        data : numpy.ndarray (2D)
            The input data.
        bounding_pool : numpy.ndarray (2D), optional
            If the fitting of the Gaussian is supposed to be constrained to
            an existing pool, the pool can be provided to ensure that Cancels
            selects the best-possible points / compounds given this pool.
        bounding_range : np.ndarray (2D)
            Alternative to `bounding_pool`. Will be overwritten if a bounding
            pool is provided. Provide the range [R1, ..., Rd] for each of d
            dimensions where Ri = [min_i, max_i] is the range for the i-th
            dimension.
        strength : int or float
            Controls the strength of the boundary enforcement. See [1]_.

	References
	----------
	.. [1] Katharina Dost, Katerina Taskova, Patricia Riddle, and Jörg Wicker. 
           "Your Best Guess When You Know Nothing: Identification and Mitigation 
           of Selection Bias." In: 2020 IEEE International Conference on Data 
           Mining (ICDM), pp. 996-1001, IEEE, 2020, ISSN: 2374-8486.

        .. [2] Katharina Dost, Zac Pullar-Strecker, Liam Brydon, Kunyang Zhang, Jasmin Hafner, 
       	   Patricia Riddle, and Jörg Wicker. "Combatting Over-Specialization Bias in Growing 
           Chemical Databases." 05 October 2022, PREPRINT (Version 1) available at Research 
           Square [https://doi.org/10.21203/rs.3.rs-2133331/v1]
        
        Examples
        --------
        >>> from imitatebias.generators import *
        >>> from imitatebias.cancels import *
        >>> import matplotlib.pyplot as plt
        >>> import seaborn as sns

        generate data and pool
        >>> X, y = generateData(500, 1, 10, seed=2210)
        >>> X_b, _, _ = generateBias(X, y, 1, seed=2210)

        fit Cancels
        >>> can = Cancels(n_pc=2)
        >>> can.fit(X_b)

        generate data points to fill in the bias (for the sake of visualization)
        >>> gen_p, _ = can.imi.augment()

        plot Cancels' indicated biases in PCA space
        >>> plt.scatter(can.pca.transform(X_b)[:,0], can.pca.transform(X_b)[:,1])
        >>> sns.kdeplot(x=gen_p[:,0], y=gen_p[:,1], cut=10, thresh=0, cmap='Greens')
        >>> plt.show()
        """
        self.pca = PCA(n_components = self.n_pc)
        self.pca.fit(data)
        self.d_trf = self.pca.transform(data)
        
        if bounding_pool is not None:
            self.imi.fit(self.d_trf, bounds_set=bounding_pool, strength=strength)
        elif bounding_range is not None:
            self.imi.fit(self.d_trf, bounds={0: bounding_range}, strength=strength)
        else:
            self.imi.fit(self.d_trf, labels=np.zeros(len(data)).astype(int))
    
    def score(self, pool):
        """Scores all elements in a pool on their bias-mitigating ability.
        
        See [1]_ for details on the score.
        
        Parameters
        ----------
        pool : numpy.ndarray (2D)
            The pool that shall be scored.

        Returns:
        
        numpy.array (1D)
            The non-normalized scores for each element of the pool.

	References
	----------
	.. [1] Katharina Dost, Zac Pullar-Strecker, Liam Brydon, Kunyang Zhang, Jasmin Hafner, 
       	   Patricia Riddle, and Jörg Wicker. "Combatting Over-Specialization Bias in Growing 
           Chemical Databases." 05 October 2022, PREPRINT (Version 1) available at Research 
           Square [https://doi.org/10.21203/rs.3.rs-2133331/v1]
            
        Examples
        --------
        >>> from imitatebias.generators import *
        >>> from imitatebias.cancels import *
        >>> import matplotlib.pyplot as plt

        generate data and pool
        >>> X, y = generateData(500, 1, 10, seed=2210)
        >>> X_b, _, _ = generateBias(X, y, 1, seed=2210)
        >>> pool = np.column_stack([np.random.uniform(min(X[:,0]), max(X[:,0]), size=1000) for i in range(len(X[0]))])

        fit Cancels
        >>> can = Cancels(n_pc=2)
        >>> can.fit(X_b)

        score the pool
        >>> scores = can.score(pool)

        plot the pool's scores in PCA space
        >>> plt.scatter(can.pca.transform(pool)[:,0], can.pca.transform(pool)[:,1], c=scores)
        >>> plt.colorbar()
        >>> plt.show()
        """
        pool_trf = self.pca.transform(pool)
        return self.imi.score(pool_trf, score_type='balanced')[:,0]
    
    def augment(self, pool):
        """Augments the input dataset using the pool.
        
        Randomly selects points / compounds from the pool to mitigate the
        identified selection bias of the input dataset.
        
        Parameters
        ----------
        pool : numpy.ndarray (2D)
            The pool that shall be scored.

        Returns
        -------
        numpy.array (1D)
            A set of indices of those element from the pool that have been selected.

	References
	----------
	.. [1] Katharina Dost, Zac Pullar-Strecker, Liam Brydon, Kunyang Zhang, Jasmin Hafner, 
       	   Patricia Riddle, and Jörg Wicker. "Combatting Over-Specialization Bias in Growing 
           Chemical Databases." 05 October 2022, PREPRINT (Version 1) available at Research 
           Square [https://doi.org/10.21203/rs.3.rs-2133331/v1]
            
        Examples
        --------
        >>> from imitatebias.generators import *
        >>> from imitatebias.cancels import *
        >>> import matplotlib.pyplot as plt

        generate data and pool
        >>> X, y = generateData(500, 1, 10, seed=2210)
        >>> X_b, _, _ = generateBias(X, y, 1, seed=2210)
        >>> pool = np.column_stack([np.random.uniform(min(X[:,0]), max(X[:,0]), size=1000) for i in range(len(X[0]))])

        fit Cancels
        >>> can = Cancels(n_pc=2)
        >>> can.fit(X_b)

        select additional data points from the pool
        >>> pool_idcs = can.augment(pool)

        plot Cancels' indicated biases in PCA space
        >>> plt.scatter(can.pca.transform(X_b)[:,0], can.pca.transform(X_b)[:,1], label='Dataset')
        >>> plt.scatter(can.pca.transform(pool)[pool_idcs,0], can.pca.transform(pool)[pool_idcs,1], label='Added')
        >>> plt.legend()
        >>> plt.show()
        """
        score = self.score(pool)
        score = score / np.sum(score) # convert to probability distribution
        pool_trf = self.imi.icas[0].transform(self.pca.transform(pool))
        data = self.imi.icas[0].transform(copy.deepcopy(self.d_trf))
        
        add_idcs = np.array([], dtype=np.int32)
        p_model_given_data = P_data_given_model(data, self.imi.grids[0], self.imi.fitted[0])
        p_model_given_data -= P_data(data, self.imi.grids[0], self.imi.fitted[0], s=3)
        num_fill = int(min(max(self.imi.num_fill_up[0]), len(score>0)))
        batches = np.append([10] * (num_fill // 10), [num_fill % 10])
        tries = 0
        
        for i in range(len(batches)):
            candidates = np.random.choice(range(len(score)), int(batches[i]), p=score).astype(int)
            d_new = np.vstack((data, pool_trf[candidates]))
            #P_new = P_model_given_data(d_new, self.imi.grids[0], self.imi.fitted[0])
            P_new = P_data_given_model(d_new, self.imi.grids[0], self.imi.fitted[0]) 
            P_new -= P_data(d_new, self.imi.grids[0], self.imi.fitted[0], s=3)
            if P_new <= p_model_given_data: # stopping if likelihood gets worse
                if tries < 3:
                    i += -1 # try again!
                    tries += 1
                else:
                    tries = 0
                continue
            p_model_given_data = P_new
            add_idcs = np.append(add_idcs, candidates)
            score[add_idcs] = 0
            data = np.vstack((data, pool_trf[add_idcs]))
            if np.sum(score) == 0: break
            score = score / np.sum(score)
            
        return add_idcs