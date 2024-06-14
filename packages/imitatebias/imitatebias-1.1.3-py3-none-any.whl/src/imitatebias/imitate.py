import numpy as np
from scipy.stats import norm
from sklearn.neighbors import LocalOutlierFactor
from sklearn.decomposition import FastICA
from scipy.optimize import minimize
from statsmodels.nonparametric.kde import KDEUnivariate

# suppress warning: warnings are only thrown by ICA if ICA cannot converge. In this case,
# the data is already Gaussian (i.e., that's a positive outcome!)
np.seterr(divide='ignore', invalid='ignore')

'''Kernel Density Estimation (from Imitate paper)'''
class DE_kde():
    def __init__(self, num_bins):
        self.num_bins = num_bins
        
    def estimate(self, data, d_min, d_max, weights):
        d_range = (d_min - 0.5*(d_max-d_min), d_max + 0.5*(d_max-d_min))
        gridsize = (d_range[1] - d_range[0]) / self.num_bins

        self.grid = [(d_range[0] + i*gridsize) for i in range(self.num_bins+1)]
        self.mids = self.grid[:-1] + np.diff(self.grid)/2
        
        kde = KDEUnivariate(data)
        try:
            kde.fit(bw='silverman', kernel='gau', fft=False, weights=weights)
        except:
            kde.fit(bw=0.01, kernel='gau', fft=False, weights=weights)
        
        self.values = [kde.evaluate(i)[0] if kde.evaluate(i) > 0 else 0 for i in self.mids]
        

'''Bounded scaled normal distribution (from Imitate paper with boundaries introduced in Cancels paper)'''
class scaled_norm_bounded():
    def __init__(self, truncate_std=3, bound_min=None, bound_max=None, ends_zero=True, ends_zero_strength=1, return_loss=False):
        self.ends_zero = ends_zero
        self.ends_zero_strength = ends_zero_strength
        self.return_loss = return_loss
        self.truncate_std = truncate_std
        self.b_min = bound_min
        self.b_max = bound_max
        
    def func_trunc(x, scale, mu, sigma, trunc):
        res = scaled_norm_bounded.func(x, scale, mu, sigma)
        res[abs(x - mu) > trunc*sigma] = 0
        return res
        
    def func(x, scale, mu, sigma):
        return scale * norm(mu, sigma).pdf(x)
    
    def weighted_dist(weights, points_x, points_y, params):
        return (((scaled_norm_bounded.func(points_x, *params) - points_y)**2) * weights).sum()
    
    def constraint(points_x, points_y, params):
        return 2*points_y.sum() - scaled_norm_bounded.func(points_x, *params).sum()

    def fit(self, points_x, points_y, data, returnParams=False):
        d_mean = points_x[np.argmax(points_y)]  # highest bin
        d_std = max(0.0001, np.sqrt( np.sum((np.array(data) - d_mean)**2) / (len(data) - 1) ))
        d_scale = max(points_y) / max(scaled_norm_bounded.func(points_x, 1, d_mean, d_std))
        p0 = np.array([d_scale, d_mean, d_std])  # initial parameters
        weights = np.array(points_y) ** 2
        weights = np.array([max(weights[i], 0.01*max(points_y)) for i in range(len(weights))])
        optimize_me = lambda p: scaled_norm_bounded.weighted_dist(weights, points_x, points_y, p)
        if self.ends_zero:
            weights[0] = weights[-1] = self.ends_zero_strength * max(points_y)
            if self.b_min is not None: weights[points_x <= self.b_min] = self.ends_zero_strength * max(points_y)
            if self.b_max is not None: weights[points_x >= self.b_max] = self.ends_zero_strength * max(points_y)
        try:
            bounds = [[0.01, 2*d_scale], [points_x[0], points_x[-1]], [0.0001,(points_x[-1]-points_x[0])/2]]
            constr = lambda p: scaled_norm_bounded.constraint(np.array(points_x), np.array(points_y), p)
            res = minimize(optimize_me, p0, bounds=bounds)#, method='SLSQP')#, constraints={'type':'ineq', 'fun': constr})
            
            if self.return_loss:
                if constr(res.x) < 0:
                    if returnParams:  return np.array(points_y), p0, optimize_me(res.x)
                    else: return np.array(points_y), optimize_me(res.x)
                if returnParams: return scaled_norm_bounded.func_trunc(points_x, *res.x, self.truncate_std), res.x, optimize_me(res.x)
                else: return scaled_norm_bounded.func_trunc(points_x, *res.x, self.truncate_std), optimize_me(res.x)
            else:
                if constr(res.x) < 0:
                    if returnParams:  return np.array(points_y), p0
                    else: return np.array(points_y)
                if returnParams: return scaled_norm_bounded.func_trunc(points_x, *res.x, self.truncate_std), res.x
                else: return scaled_norm_bounded.func_trunc(points_x, *res.x, self.truncate_std)
        except:
            if self.return_loss:
                if returnParams:  return np.array(points_y), p0, 0
                else: return np.array(points_y), 0
            else:
                if returnParams:  return np.array(points_y), p0
                else: return np.array(points_y)
            
            
'''Outlier Removal using Local Outlier Factor'''
def remove_outliers_lof(data, k=10):
    k = min((len(data), k))
    lof = LocalOutlierFactor(n_neighbors=k)
    stays = lof.fit_predict(data)
    return np.array(data)[stays == 1]

'''finds the number of bins that best describe the data (AICc)'''
def getBestNumBins(bins, d):
    min_aicc = np.Inf
    best_bins = 0
    
    for num_bins in bins:
        # get histogram
        d_range = (min(d) - 0.5*(max(d)-min(d)), max(d) + 0.5*(max(d)-min(d)))
        values, grid = np.histogram(d, bins=num_bins, density=True, range=d_range)
        mids = grid[:-1] + np.diff(grid)/2

        # calc MLE: ln(P[data | model])
        bin_per_p = np.digitize(d, grid)
        ln_L = sum(np.log( values[bin_per_p - 1] ))

        # calc aicc
        aicc = 2*num_bins*len(d) / (len(d)-num_bins-1) - 2*ln_L
        #bic =  log(len(d))*num_bins - 2*ln_L
        #bic =  2*num_bins - 2*ln_L # aic
        
        if aicc < min_aicc:
            min_aicc = aicc
            best_bins = num_bins

    return best_bins

'''main method: For an ICA-transformed dataset, find the bias'''
def run_imitate(data, num_bins=0, bounds=None, strength=1, return_loss=False):
    grids = []
    vals = []
    fitted = []
    fill_up = []
    num_fill_up = []
    params = []
    total_loss = 0

    # consider every dimension
    for line in range(len(data[0])):
        
        d = data[:,line]   # project onto line
        if num_bins==0: num_bins = getBestNumBins(range(min(int(len(d)/2),20), min(60, len(d)-2)), d)
        
        d_range = (min(d) - 0.5*(max(d)-min(d)), max(d) + 0.5*(max(d)-min(d)))
        grid = [(d_range[0] + i*((d_range[1] - d_range[0]) / num_bins)) for i in range(num_bins+1)]
        mids = grid[:-1] + np.diff(grid)/2
        kde = KDEUnivariate(d)
        try:
            kde.fit(bw='silverman', kernel='gau', fft=False)      
        except:
            kde.fit(bw=0.01, kernel='gau', fft=False)  
        values = np.array([kde.evaluate(i)[0] if kde.evaluate(i) > 0 else 0 for i in mids])
        values_scaled = (len(d) / sum(values)) * values    # scale to absolute values
        grids.append(grid)
        vals.append(values_scaled)

        if bounds is not None:
            SN = scaled_norm_bounded(bound_min=bounds[line][0], bound_max=bounds[line][1], ends_zero=True, ends_zero_strength=strength, return_loss=return_loss)
        else:
            SN = scaled_norm_bounded(return_loss=return_loss)
        if return_loss: 
            fitted_, p, loss = SN.fit(mids, values_scaled, d, returnParams=True) # fit Gaussian
            total_loss += loss
        else: fitted_, p = SN.fit(mids, values_scaled, d, returnParams=True) # fit Gaussian

        params.append(p)  
        fitted.append(fitted_)

        diff = fitted_ - values_scaled    # decide where to fill up
        diff[diff < 1] = 0 # don't fill if we are not sure that we need the point
        fill_up.append(np.floor(diff).astype(int))

        num_fill_up.append(sum(np.floor(diff)))    # count how much needs to be filled
        
    mean = np.array(params)[:,1]
    cov = np.zeros((len(data[0]), len(data[0])))
    np.fill_diagonal(cov, np.array(params)[:,2]**2)
    scale = np.array(params)[:,0]

    if return_loss: return grids, vals, fitted, fill_up, num_fill_up, scale, mean, cov, total_loss
    return grids, vals, fitted, fill_up, num_fill_up, scale, mean, cov


################
# USER METHODS #
################
class Imitate:
    """Imitate generates points to mitigate a dataset's bias.
    
    Imitate investigates the dataset's probability density, then adds generated points 
    in order to smooth out the density and have it resemble a Gaussian, the most common 
    density occurring in real-world applications. If the artificial points focus on 
    certain areas and are not widespread, this could indicate a Selection Bias where 
    these areas are underrepresented in the sample.
    
    See our paper [1]_ for details.
    
    Attributes
    ----------
    icas : list(sklearn.decomposition.FastICA) 
        A list of `FastICA` objects trained per label in the training set.
    grids : dict(string or int or float: numpy.ndarray (2D))
        A dictionary mapping a class label to its corresponding grids per dimension 
        over which KDE was evaluated.
    vals : dict(string or int or float: numpy.ndarray (2D))
        A KDE density representation of the dataset evaluated over `grids`.
    fitted : dict(string or int or float: numpy.ndarray (2D))
        Fitted Gaussian PDF evaluated over `grids`.
    fill_up : dict(string or int or float: numpy.ndarray (2D))
        `vals - fitted`, evaluated over `grids`.
    num_fill_up : dict(string or int or float: numpy.array (1D))
        The necessary number of points to add to mitigate the bias; per label and 
        dimension.
    
    Methods
    -------
    fit(data, labels=[], bounds={}, strength=1000)
        Fits the Imitate Gaussians to a dataset.
    score(data)
        Scores new data based on Imitate'd fitted Gaussians.
    augment()
        Augments the fitted dataset to mitigate its bias.

    References
    ----------
    .. [1] Katharina Dost, Katerina Taskova, Patricia Riddle, and Jörg Wicker. 
       "Your Best Guess When You Know Nothing: Identification and Mitigation of 
       Selection Bias." In: 2020 IEEE International Conference on Data Mining (ICDM), 
       pp. 996-1001, IEEE, 2020, ISSN: 2374-8486.
        
    Examples
    --------
    >>> from imitatebias.generators import *
    >>> from imitatebias.imitate import *
    >>> import matplotlib.pyplot as plt

    Generate a dataset.
    >>> X, y = generateData(1000, 2, 2, seed=2210)

    Generate a biased dataset.
    >>> X_b, y_b, idcs_deleted = generateBias(X, y, 1, seed=2210)

    initialize Imitate
    >>> imi = Imitate()

    fit Imitate to the biased dataset
    >>> imi.fit(X_b, labels=y_b)

    visualize data per cluster in ICA space
    >>> for l in np.unique(y_b):
    >>>     data_transformed = imi.icas[l].transform(X_b[y_b == l])
    >>>     plt.scatter(data_transformed[:,0], data_transformed[:,1])
    >>>     plt.title('Class '+str(l))
    >>>     plt.show()

    create some random points to score
    >>> rnd_points = np.column_stack((np.random.uniform(min(X[:,0]), max(X[:,0]), size=1000), \
    >>>                               np.random.uniform(min(X[:,1]), max(X[:,1]), size=1000)))

    score the random points
    >>> scores_fill = imi.score(rnd_points, score_type='fill')
    >>> scores_balanced = imi.score(rnd_points, score_type='balanced')

    visualize data per cluster in ICA space
    >>> for l in np.unique(y_b):
    >>>     plt.scatter(rnd_points[:,0], rnd_points[:,1], c=scores_fill[:,int(l)])
    >>>     plt.title('Class '+str(l)+'; Score type = fill')
    >>>     plt.colorbar()
    >>>     plt.show()

    >>>     plt.scatter(rnd_points[:,0], rnd_points[:,1], c=scores_balanced[:,int(l)])
    >>>     plt.title('Class '+str(l)+'; Score type = balanced')
    >>>     plt.colorbar()
    >>>     plt.show()

    augment the dataset
    >>> X_gen, y_gen = imi.augment()

    visualize data per cluster in ICA space
    >>> plt.scatter(X_b[:,0], X_b[:,1], c=y_b)
    >>> plt.scatter(X_gen[:,0], X_gen[:,1], c=y_gen, edgecolors='red')
    >>> plt.title('Dataset with generated points (red)')
    >>> plt.show()
    """
    
    def __init__(self):
        """Imitate Constructor."""
        self.icas = {}
        self.grids = {}
        self.vals = {}
        self.fitted = {}
        self.fill_up = {}
        self.num_fill_up = {}
        
    def fit(self, data, labels=[], bounds={}, bounds_set=None, strength=1000):
        """Fits a bias-aware multivariate Gaussian per label to the data.
        
        Given a dataset and a potential label array, Imitate splits the data per 
        class and operates on each subset individually. For each of those labels, 
        fit fits a multivariate Gaussian to the subset that accounts for potential 
        biases. See our paper [1]_ for details.
        Custom borders can be defined that constrain the fitting process. The strength
        parameter controls how strongly these borders are enforced (the non-bounded
        version uses `strength=1`).
        
        Parameters
        ----------
        data : numpy.ndarray (2D)
            Potentially biased input dataset.
        labels : numpy.array (1D), optional
            Labels corresponding to the dataset if available.
        bounds : dict(string or int or float: numpy.ndarray (2D)), optional
            Bounds Imitate if provided, for each label, in the shape 
            ``[[min_0, max_0], ..., [min_d, max_d]]``
            for d dimensions. Use a `dictionary` to map each label to its correct
            bounds.
        bounds_set : numpy.ndarray (2D)
            If Imitate should be bounded to the ranges of a certain dataset, this set
            can be passed to it directly. Will be overwritten by `bounds` if specified.
        strength : int, default=1000
            Controls how strongly the bounds are enforced. Will be ignored if no
            bounds are specified.

	References
	----------
	.. [1] Katharina Dost, Katerina Taskova, Patricia Riddle, and Jörg Wicker. 
           "Your Best Guess When You Know Nothing: Identification and Mitigation of 
           Selection Bias." In: 2020 IEEE International Conference on Data Mining (ICDM), 
           pp. 996-1001, IEEE, 2020, ISSN: 2374-8486.
            
        Examples
        --------
        >>> from imitatebias.generators import *
        >>> from imitatebias.imitate import *
        >>> import matplotlib.pyplot as plt

        Generate a dataset.
        >>> X, y = generateData(1000, 2, 2, seed=2210)

        Generate a biased dataset.
        >>> X_b, y_b, idcs_deleted = generateBias(X, y, 1, seed=2210)

        initialize Imitate
        >>> imi = Imitate()

        fit Imitate to the biased dataset
        >>> imi.fit(X_b, labels=y_b)

        visualize data per cluster in ICA space
        >>> for l in np.unique(y_b):
        >>>     data_transformed = imi.icas[l].transform(X_b[y_b == l])
        >>>     plt.scatter(data_transformed[:,0], data_transformed[:,1])
        >>>     plt.title('Class '+str(l))
        >>>     plt.show()
        """
        self.data = data
        self.labels = np.zeros(len(data)).astype(int) if len(labels)==0 else labels
        for l in np.unique(labels):
            d = data[labels == l]
            self.icas[l] = FastICA(n_components=len(d[0]), whiten='arbitrary-variance')
            self.icas[l].fit(d)
            d_trf = self.icas[l].transform(d)
            
            if len(bounds) > 0:
                b = bounds.get(l) if len(bounds)>0 else None            
                p_gen = np.column_stack([np.random.uniform(*b[i], 1000) for i in range(len(d[0]))])            
                p_trf = self.ica.transform(p_gen)
                bounds_trf = np.vstack((p_trf.min(axis=0), p_trf.max(axis=0))).transpose()
                range_trf = bounds_trf[:,1] - bounds_trf[:,0]
                bounds_relaxed = np.vstack((bounds_trf[:,0]-0.1*range_trf, bounds_trf[:,1]+0.1*range_trf)).transpose()
            
                self.grids[l], self.vals[l], self.fitted[l], self.fill_up[l], self.num_fill_up[l], _, _, _ = run_imitate(
                    d_trf, bounds=bounds_relaxed, strength=strength)
            elif bounds_set is not None:
                p_trf = self.ica.transform(bounds_set)
                bounds_trf = np.vstack((p_trf.min(axis=0), p_trf.max(axis=0))).transpose()
                range_trf = bounds_trf[:,1] - bounds_trf[:,0]
                bounds_relaxed = np.vstack((bounds_trf[:,0]-0.1*range_trf, bounds_trf[:,1]+0.1*range_trf)).transpose()
            
                self.grids[l], self.vals[l], self.fitted[l], self.fill_up[l], self.num_fill_up[l], _, _, _ = run_imitate(
                    d_trf, bounds=bounds_relaxed, strength=strength)
            else:
                self.grids[l], self.vals[l], self.fitted[l], self.fill_up[l], self.num_fill_up[l], _, _, _ = run_imitate(
                    d_trf, bounds=None, strength=1)
            
    def score(self, data, score_type='fill'):
        """Scores new data based on Imitate's fitted Gaussian.
        
        Imitate fits one multivariate Gaussian per label in a dataset. Scores are 
        obtained via the difference of those Gaussians' PDFs and the input data
        (represented via a KDE estimate). See our paper [1]_ for details.
        
        Parameters
        ----------
        data : numpy.ndarray (2D)
            Data that shall be scored. This dataset does not need to match the input data,
            but it is required to have the same dimensionality.
        score_type : {'fill', 'balanced'}, default='fill'
            Selects the type of score. `'fill'` measures how well a data points fills in
            the identified bias, i.e., it quantifies the difference between the fitted
            and the observed dataset distribution. The score is set to 0 if the 3-std-
            truncated fitted Gaussian's PDF at this point evaluates to 0. `'balanced'` 
            additionally takes into account how likely a point is to be observed in this 
            dataset. See our paper [2]_ for details.
        
        Returns
        -------
        np.ndarray (2D)
            Score (i,j) corresponds to data point D_i and input data label j. 

	References
	----------
        .. [1] Katharina Dost, Katerina Taskova, Patricia Riddle, and Jörg Wicker. 
           "Your Best Guess When You Know Nothing: Identification and Mitigation of 
           Selection Bias." In: 2020 IEEE International Conference on Data Mining (ICDM), 
           pp. 996-1001, IEEE, 2020, ISSN: 2374-8486.

        .. [2] Katharina Dost, Hamish Duncanson, Ioannis Ziogas, Patricia Riddle, and Jörg 
           Wicker. "Divide and Imitate: Multi-Cluster Identification and Mitigation of 
           Selection Bias." In: Advances in Knowledge Discovery and Data Mining - 26th 
           Pacific-Asia Conference, PAKDD 2022. Lecture Notes in Computer Science, vol. 
           13281, pp. 149-160. Springer, Cham (2022).
            
        Examples
        --------
        >>> from imitatebias.generators import *
        >>> from imitatebias.imitate import *
        >>> import matplotlib.pyplot as plt

        Generate a dataset.
        >>> X, y = generateData(1000, 2, 2, seed=2210)

        Generate a biased dataset.
        >>> X_b, y_b, idcs_deleted = generateBias(X, y, 1, seed=2210)

        initialize Imitate
        >>> imi = Imitate()

        fit Imitate to the biased dataset
        >>> imi.fit(X_b, labels=y_b)

        create some random points to score
        >>> rnd_points = np.column_stack((np.random.uniform(min(X[:,0]), max(X[:,0]), size=1000), \
        >>>                               np.random.uniform(min(X[:,1]), max(X[:,1]), size=1000)))

        score the random points
        >>> scores_fill = imi.score(rnd_points, score_type='fill')
        >>> scores_balanced = imi.score(rnd_points, score_type='balanced')

        visualize data per cluster in ICA space
        >>> for l in np.unique(y_b):
        >>>     plt.scatter(rnd_points[:,0], rnd_points[:,1], c=scores_fill[:,int(l)])
        >>>     plt.title('Class '+str(l)+'; Score type = fill')
        >>>     plt.colorbar()
        >>>     plt.show()

        >>>     plt.scatter(rnd_points[:,0], rnd_points[:,1], c=scores_balanced[:,int(l)])
        >>>     plt.title('Class '+str(l)+'; Score type = balanced')
        >>>     plt.colorbar()
        >>>     plt.show()
        """
        scores = np.zeros((len(data), len(self.icas)))
        for i,l in enumerate(np.unique(self.labels)): # fill scores[:,i]
            data_trf = self.icas[l].transform(data)
            grids, fitted, fill_up = self.grids[l], self.fitted[l], self.fill_up[l]
            
            fitted_grid = np.zeros((len(data_trf), len(data_trf[0]))) # points x dims
            fill_grid = np.zeros((len(data_trf), len(data_trf[0]))) # points x dims
            for d in range(len(data_trf[0])):
                # organize in grid cells: 0 = smaller; len(grids[0]) = larger
                grid_dim = np.digitize(data_trf[:,d], grids[d]) # points x dims
                map_to_fitted = np.vectorize(lambda idx: 0 if idx<=0 or idx>=len(grids[d]) else fitted[d][idx-1])
                map_to_fill = np.vectorize(lambda idx: 0 if idx<=0 or idx>=len(grids[d]) else fill_up[d][idx-1])
                fitted_grid[:, d] = map_to_fitted(grid_dim)
                fill_grid[:, d] = map_to_fill(grid_dim)
            if score_type == 'fill':
                scores[:, i] = np.sum(fill_grid, axis=1)
                scores[np.prod(fitted_grid, axis=1) == 0, i] = 0 # 0 score for unprobable entries
            elif score_type == 'balanced':           
                s1 = np.sum(np.log(fitted_grid + 1), axis=1)  # fitted distribution
                s2 = np.sum(np.log(fill_grid + 1), axis=1)   # fill_up
                scores[:, i] = s1 + len(data_trf[0])*s2   # score as the sum of both (weighted?)
                scores[np.sum(fill_grid, axis=1) == 0, i] = 0   # 0 score where we don't fill anything up
                scores[np.prod(fitted_grid, axis=1) == 0, i] = 0   # 0 score for unprobable entries
        return scores

    def augment(self):
        """Augments the fitted dataset to mitigate its bias.
        
        Generates points to mitigate the bias in the input dataset provided to the `fit` method.
        The number of generated points per label is determined by `Imitate.num_fill_up`.
        
        Returns
        -------
        numpy.ndarray (2D)
            Generated points.
        numpy.array (1D)
            Corresponding labels.
        
        Examples
        --------
        >>> from imitatebias.generators import *
        >>> from imitatebias.imitate import *
        >>> import matplotlib.pyplot as plt

        Generate a dataset.
        >>> X, y = generateData(1000, 2, 2, seed=2210)

        Generate a biased dataset.
        >>> X_b, y_b, idcs_deleted = generateBias(X, y, 1, seed=2210)

        initialize Imitate
        >>> imi = Imitate()

        fit Imitate to the biased dataset
        >>> imi.fit(X_b, labels=y_b)

        augment the dataset
        >>> X_gen, y_gen = imi.augment()

        visualize data per cluster in ICA space
        >>> plt.scatter(X_b[:,0], X_b[:,1], c=y_b)
        >>> plt.scatter(X_gen[:,0], X_gen[:,1], c=y_gen, edgecolors='red')
        >>> plt.title('Dataset with generated points (red)')
        >>> plt.show()
        """
        gen_points = np.empty((0, len(self.data[0])))
        gen_labels = []
        
        for l in np.unique(self.labels):
            num_fill_up = self.num_fill_up[l]
            num_gen = np.max(num_fill_up).astype(int)
            if num_gen == 0: continue
            grids, vals, fitted, fill_up = self.grids[l], self.vals[l], self.fitted[l], self.fill_up[l]
        
            points = np.empty((num_gen, 0))
            for d in range(len(self.data[0])):
                fill = fitted[d] / np.sum(fitted[d]) * (num_gen - num_fill_up[d])  +  fill_up[d] #mixed distr
                fill_cdf = np.cumsum(fill) / num_gen  #normalize

                #generate points according to the cdf
                vals = np.random.rand(num_gen)
                val_bins = np.searchsorted(fill_cdf, vals)
                coords = np.array([np.random.uniform(grids[d][val_bins[i]], grids[d][val_bins[i]+1]) 
                                   for i in range(num_gen)]).reshape(num_gen, 1)
                points = np.concatenate((points, coords), axis=1)

            gen_points = np.concatenate((gen_points, self.icas[l].inverse_transform(points)))
            gen_labels = np.append(gen_labels, [l]*num_gen)
        return gen_points, gen_labels