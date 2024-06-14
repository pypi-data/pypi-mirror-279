from imitatebias.imitate import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from collections import Counter
import copy
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.preprocessing import normalize
from scipy.stats import multivariate_normal

# suppress warning: warnings are only thrown by ICA if ICA cannot converge. In this case,
# the data is already Gaussian (i.e., that's a positive outcome!)
np.seterr(divide='ignore', invalid='ignore')



# HELPERS

def findK(data):
    sample, _, _, _ = train_test_split(data, [0]*len(data), train_size=min(500, int(0.7*len(data))))
    max_num_test = int(len(data) / 100)
    scores = np.array([-1.0]*(max_num_test+1))
    for n in range(2, max_num_test+1):
        scores[n] = silhouette_score(sample, KMeans(n_clusters=n, random_state=0).fit_predict(sample))
    return int(max(5, np.argmax(scores)*2))

def init_with_kmeans(data_full, data_clean, k=100):
    kmeans = KMeans(n_clusters=k, n_init=10).fit(np.array(data_clean))
    lab = kmeans.predict(data_full)
        
    for cl in np.unique(lab):
        idcs = np.where(lab == cl)[0]
        if len(idcs) < 10: continue
        if split_test(data_full[idcs]):
            km = KMeans(n_clusters=2, n_init=10).fit(data_full[idcs])
            l = km.predict(data_full[idcs])
            lab[idcs[l==1]] = max(lab)+1
    return lab

def split_test(cluster):
    if np.sum(np.std(cluster, axis=0) == 0) > 0: 
        cluster = cluster[:,np.std(cluster, axis=0)>0]
    ica = FastICA(n_components=len(cluster[0]), max_iter=500, tol=0.01, whiten='arbitrary-variance').fit(cluster)
    data_trf = ica.transform(cluster)
    for d in range(len(cluster[0])):
        DE = DE_kde(30)    # define Density Estimator
        DE.estimate(data_trf[:,d], min(data_trf[:,d]), max(data_trf[:,d]), weights=np.ones(len(data_trf[:,d])))
        hh = DE.values
        for i in range(1, len(hh)-1):
            if max(hh[0:i]) > 0.05*max(hh)+hh[i] and max(hh[i+1:]) > 0.05*max(hh)+hh[i]:
                return True
    return False


# MIMIC

def run_mimic(full_data, init_labels=None, k_init=100):
    
    # remove outliers
    lof = LocalOutlierFactor(n_neighbors=min((len(full_data), 10)))
    valid = lof.fit_predict(full_data)
    lof_nf = lof.negative_outlier_factor_[valid==1]
    
    # initialize using KMeans with a very large number of clusters
    if init_labels is None:
        init_labels = init_with_kmeans(full_data, full_data[valid==1], k_init)
    
    data = full_data[valid==1] # clean data
    labels = init_labels[valid==1]
    
    lof_nf_per_cluster = np.array([np.average(lof_nf[labels==c]) for c in np.unique(labels)])
    lof_nf_min = np.mean(lof_nf_per_cluster) - 3*np.std(lof_nf_per_cluster)
    
    clusters_checked = [] # indicate which cluster have already been processed
    labels_largest_clust = np.copy(labels) # used for the largest cluster count
    cluster_assignments = np.empty((len(full_data),0)) # store the output probabilities per cluster
    
    parameters = [] #store parameters and ICAs
    
    while True:
        # "reset" labels
        labels_tmp = np.copy(labels)
        
        # get largest cluster
        cluster_counts = Counter(labels_largest_clust)
        #cluster_counts = Counter(labels_tmp[valid==1])
        for key in clusters_checked:
            if key in cluster_counts:
                _ = cluster_counts.pop(key) 
        if -1 in cluster_counts: #-1 is reserved for outliers!
            _ = cluster_counts.pop(-1)
        
        # if no cluster left: stop right away
        if len(cluster_counts) == 0:
            break
        largest_cluster = max(cluster_counts, key=cluster_counts.get)
        
        # if small: stop right away
        if cluster_counts[largest_cluster] < 10:
            clusters_checked = np.append(clusters_checked, [largest_cluster])
            break
            
        # if assembly of "left-overs": skip
        #print("Avg LOF score in cluster:", np.average(lof_nf[labels_largest_clust == largest_cluster]),
        #     "min acceptable: ", lof_nf_min)
        if np.average(lof_nf[labels_largest_clust == largest_cluster]) < lof_nf_min:
            clusters_checked = np.append(clusters_checked, [largest_cluster])
            continue
        
        # run iteration, receive labels_tmp and probs_clust for this cluster
        labels_tmp, probs_clust, orig_mean, orig_cov = grow_cluster(data, full_data, labels_tmp, largest_cluster)
        
        # overwrite labels with the newly formed cluster where applicable
        labels_largest_clust[labels_tmp == largest_cluster] = largest_cluster
        clusters_checked = np.append(clusters_checked, [largest_cluster])
        
        # append estimated probs per point for the constructed cluster to cluster_assignments
        cluster_assignments = np.column_stack((cluster_assignments, np.array(probs_clust)))
        parameters.append([orig_mean, orig_cov])
    
    return cluster_assignments, parameters

def P_model_given_data(data_trf, cl_idcs, add_to_cluster_idcs, grids, fitted, p_data_incr=0):
    idcs = np.append(cl_idcs, add_to_cluster_idcs).astype(int)
    
    p_data_given_model = P_data_given_model(data_trf[idcs], grids, fitted)
    if p_data_incr > 0:
        p_data = p_data_incr + P_data(data_trf[add_to_cluster_idcs], grids, fitted, s=3)
    else: 
        p_data = P_data(data_trf[idcs], grids, fitted, s=3)
    p_model = 1 #same model for all datasets, so no need to calculate that!
    p_model_given_data = p_data_given_model - p_data
    #print("p_data_given_model - p_data = %.2f - %.2f = %.2f" % (p_data_given_model, p_data, p_model_given_data))
    return p_model_given_data

def P_data_given_model(data, grids, fitted):
    res = 0
    for d in range(len(data[0])):
        fitted[d][fitted[d]==0] = 0.00001  #use non-truncated results later!!
        hh = np.histogram(data[:,d], bins=grids[d])[0] #histogram heights
        f = fitted[d] / np.sum(fitted[d])
        tmp = hh * np.log(f)
        tmp[hh==0] = 0 # 0 times whatever should be 0
        res += np.sum(tmp)
    return res

def P_data(data, grids, fitted, s=3):
    mean = np.array([(g[0] + g[-1])/2.0 for g in grids])
    std = (mean - np.array([g[0] for g in grids])) / 3.0
    cov = np.zeros((len(grids), len(grids)))
    np.fill_diagonal(cov, std**2)
    
    mn = multivariate_normal(mean, cov)#.pdf(data)
    mids = [(np.array(grids[d][0:-1]) + np.array(grids[d][1:])) / 2 for d in range(len(grids))]
    cubesize = np.prod(np.array([g[1] - g[0] for g in grids]))
    
    data_in_bins = np.column_stack([np.digitize(data[:,i], grids[i])-1 for i in range(len(grids))])
    corresp_mids = np.column_stack([mids[i][data_in_bins[:,i]] for i in range(len(grids))])
    probs = mn.pdf(corresp_mids) * cubesize
    
    return np.sum(np.log(probs))
    #return np.sum(np.log(mn))
    
    
    
    if len(data[0])>5: return -len(data)
    # (1 / #gridcells) ^ #datapoints
    # log  ->  #data * (- log(#cells)) = - #data * log(#cells) -> - #data because #cells is constant here
    #log_cells = sum(np.log([len(grids[i]) for i in range(len(grids))]))
    #return - len(data) * log_cells
    mids = [(np.array(grids[d][0:-1]) + np.array(grids[d][1:])) / 2 for d in range(len(grids))]

    mu0 = np.array([g[0] for g in grids]) # lower mu boundaries for all dimensions
    mu1 = np.array([g[-1] for g in grids]) # upper mu boundaries for all dimensions
    sig0 = np.array([0.01] * len(mu0)) # lower sig boundaries for all dimensions
    sig1 = (mu1 - mu0)*0.5 # upper sig boundaries for all dimensions
    mu_step = (mu1 - mu0) / s # mu step size per dimension
    sig_step = (sig1 - sig0) / s # sig step size per dimension
    
    # split into little boxes: dim x boxes
    mu = [np.linspace(mu0[d] + 0.5*mu_step[d], mu1[d] - 0.5*mu_step[d], s) for d in range(len(mu0))]
    sig = [np.linspace(sig0[d] + 0.5*sig_step[d], sig1[d] - 0.5*sig_step[d], s) for d in range(len(sig0))]
    #ln_hypercube_size = np.sum(np.log(mu_step + 1)) + np.sum(np.log(sig_step + 1))
    ln_hypercube_size = np.sum(np.log(mu_step)) + np.sum(np.log(sig_step))
    # param list: mu for dim0, sig for dim 0, mu for dim 1, sig for dim 1, ...
    params_per_d = list(itertools.chain.from_iterable(zip(mu, sig)))

    coords = np.meshgrid(*params_per_d)
    param_tuples = np.column_stack([coords[i].flatten() for i in range(len(coords))])
    
    # param combos for all dimensions (it's a 2d-tuple with #dims=:d)
    vals = []
    for p_2dtuple in param_tuples: #(mu_dim0, sig_dim0, mu_dim1, sig_dim1, ...)
        val = ln_hypercube_size

        mus = [p_2dtuple[2*i] for i in range(int(len(p_2dtuple)/2))] #(mu_dim0, mu_dim1, ...)
        sigs = [p_2dtuple[2*i+1] for i in range(int(len(p_2dtuple)/2))] #(sig_dim0, sig_dim1, ...)
        # build up "fitted" here and then send together with grids! 
        fitted_p = [norm(mus[d],sigs[d]).pdf(mids[d]) for d in range(len(mids))]
        val += P_data_given_model(data, grids, fitted_p)

        # split into 2-tuples for each dimension
        p_2tuples = p_2dtuple.reshape(int(len(p_2dtuple)/2), 2)
        #iterate over dimensions
        for d in range(len(p_2tuples)):
            p = p_2tuples[d]
            val += log(P_model(p[0], mu0[d], mu1[d])) + log(P_model(p[1], sig0[d], sig1[d]))
        vals.append(val)
        
    return logsumexp(vals)

def P_model(x, left, right):
    mu = (left + right) / 2
    sigma = (mu - left) / 3
    res = norm(mu, sigma).pdf(x)
    #res[abs(x - mu) > 3*sigma] = 0
    return np.prod(res)

def grow_cluster(data, full_data, labels_tmp, grow_this):

    cont_loop = True
    #mle = -np.Inf
    while cont_loop:
        # get the points with this label
        cl_idcs = np.where(labels_tmp==grow_this)[0]
        if len(data) == len(cl_idcs): # break if we already sucked in all data
            break
    
        add_to_cluster_idcs, grids, fitted, ica, mean, cov = eat_points(data, cl_idcs)
        # update labels
        labels_tmp[add_to_cluster_idcs] = grow_this
        cont_loop = len(add_to_cluster_idcs) > 0 # break if we don't add any points
    
    # use the final fit to assign probabilities to all data points
    probs_clust = getProbs(ica.transform(full_data), grids, fitted)
    
    # transform parameters back to original space
    orig_cov = ica.mixing_.dot(cov).dot(ica.mixing_.transpose())
    orig_mean = ica.inverse_transform([mean])[0]
    
    return labels_tmp, probs_clust, orig_mean, orig_cov

class Dummy_ICA():
    def __init__(self, num_dims):
        self.mixing_ = np.identity(num_dims)
    def transform(data):
        return data
    def inverse_transform(data):
        return [data, 0]

def eat_points(data, cl_idcs, batchsize=10):
    
    # train ICA on cluster, transform everything
    cluster_clean = remove_outliers_lof(data[cl_idcs].astype(float))
    try:
        dev = np.std(cluster_clean, axis=0)
        if np.sum(dev == 0) > 0:
            for i in np.where(dev==0)[0]:
                cluster_clean[:,i] += np.random.normal(0,1,len(cluster_clean))
        ica = FastICA(n_components=len(data[0]), max_iter=500, tol=0.01, whiten='arbitrary-variance').fit(cluster_clean.astype(float))
    except:
        ica = Dummy_ICA(len(data[0]))
    data_trf = ica.transform(data)
    
    # use Imitate
    grids, _, fitted, fill_up, num_fill_up, _, mean, cov = run_imitate(data_trf[cl_idcs])
    
    # score all points
    score = score1(data_trf, grids, fitted, fill_up)
    score[cl_idcs] = 0 #don't add the points already in the cluster
    if np.sum(score) == 0: return [], grids, fitted, ica, mean, cov
    score = score / np.sum(score)  #convert to probability distribution
    
    # greedily add points and see if that improves likelihood
    add_to_cluster_idcs = np.array([], dtype=np.int32)
    p_model_given_data = P_model_given_data(data_trf, cl_idcs, add_to_cluster_idcs, grids, fitted)
    num_fill = int(min(max(num_fill_up), len(score>0)))
    batches = np.append([batchsize] * (num_fill // batchsize), [num_fill % batchsize])
    tries = 0
    for i in range(len(batches)):
        candidates = np.random.choice(range(len(score)), int(batches[i]), p=score).astype(int)
        P_new = P_model_given_data(data_trf, cl_idcs, np.append(add_to_cluster_idcs, candidates), grids, 
                                   fitted, p_data_incr=p_model_given_data)
        if P_new <= p_model_given_data: # stopping if likelihood gets worse
            if tries < 3:
                i += -1 # try again!
                tries += 1
            else:
                tries = 0
            continue
        p_model_given_data = P_new
        add_to_cluster_idcs = np.append(add_to_cluster_idcs, candidates)
        score[add_to_cluster_idcs] = 0
        if np.sum(score) == 0: break
        score = score / np.sum(score)  #convert to probability distribution

    return add_to_cluster_idcs, grids, fitted, ica, mean, cov

def score1(data_trf, grids, fitted, fill_up):  
    #  assign grid cell to data point and get corresponding entry in "fitted" or 0
    fitted_grid = np.zeros((len(data_trf), len(data_trf[0]))) # points x dims
    fill_grid = np.zeros((len(data_trf), len(data_trf[0]))) # points x dims
    for d in range(len(data_trf[0])):
        # organize in grid cells: 0 = smaller; len(grids[0]) = larger
        grid_dim = np.digitize(data_trf[:,d], grids[d]) # points x dims
        map_to_fitted = np.vectorize(lambda idx: 0 if idx<=0 or idx>=len(grids[d]) else fitted[d][idx-1])
        map_to_fill = np.vectorize(lambda idx: 0 if idx<=0 or idx>=len(grids[d]) else fill_up[d][idx-1])
        fitted_grid[:, d] = map_to_fitted(grid_dim)
        fill_grid[:, d] = map_to_fill(grid_dim)
        
    s1 = np.sum(np.log(fitted_grid + 1), axis=1)  # fitted distribution
    s2 = np.sum(np.log(fill_grid + 1), axis=1)   # fill_up
    s = s1 + len(data_trf[0])*s2   # score as the sum of both (weighted?)
    s[np.sum(fill_grid, axis=1) == 0] = 0   # 0 score where we don't fill anything up
    s[np.prod(fitted_grid, axis=1) == 0] = 0   # 0 score for unprobable entries
    return s

def getProbs(data_tf, grids, fitted):

    #  assign grid cell to data point and get corresponding entry in "fitted" or 0
    fitted_grid = np.zeros((len(data_tf), len(data_tf[0]))) # points x dims
    for d in range(len(data_tf[0])):
        # organize in grid cells: 0 = smaller; len(grids[0]) = larger
        grid_dim = np.digitize(data_tf[:,d], grids[d]) # points x dims
        map_to_fitted = np.vectorize(lambda idx: 0 if idx<=0 or idx>=len(grids[d]) else fitted[d][idx-1])
        fitted_grid[:, d] = map_to_fitted(grid_dim)
    #  normalize (divide by sum(fitted) per dimension), average over dimensions
    sum_fitted_per_dim = [sum(fitted[i]) for i in range(len(fitted))]
    fitted_grid = fitted_grid / sum_fitted_per_dim
    #probs_clust = np.sum(np.log(fitted_grid), axis=1) 
    probs_clust = fitted_grid.prod(1)
    
    return probs_clust


# FINAL AUGMENTATION

def Mimic_augment(data, labels, restarts=10, num_bins=0):
    gen_points = np.empty((0, len(data[0])))
    gen_labels = []
    for l in np.unique(labels):
        min_loss = np.inf
        best_imi = None
        for outer_restarts in range(10):
            x = data[labels==l].astype(float)
            if len(x) < 5: continue
            cluster_clean = remove_outliers_lof(x)
            if len(cluster_clean) < 5: continue
            dev = np.std(cluster_clean, axis=0)
            if np.sum(dev == 0) > 0:
                for i in np.where(dev==0)[0]:
                    cluster_clean[:,i] += np.random.normal(0,1,len(cluster_clean))

            best_crit = np.Inf
            for r in range(restarts):
                ica_tmp = FastICA(n_components=len(data[0]), max_iter=500, tol=0.01, whiten='arbitrary-variance').fit(cluster_clean.astype(float))
                grids, _, fitted, fill_up, num_fill_up, _, _, _ = run_imitate(
                    ica_tmp.transform(cluster_clean), num_bins=num_bins)
                crit = 0
                for d in range(len(fitted)):
                    if sum(fill_up[d]) > 0:
                        mids = [t + s for s, t in zip(grids[d], grids[d][1:])]
                        mean_fitted = np.average(mids, weights=fitted[d])
                        var_fitted = np.average((mids-mean_fitted)**2, weights=fitted[d])
                        mean_fill = np.average(mids, weights=fill_up[d])
                        var_fill = np.average((mids-mean_fill)**2, weights=fill_up[d])
                        crit += var_fill / var_fitted
                if crit < best_crit: 
                    ica = copy.deepcopy(ica_tmp)
                    best_crit = crit

            data_trf = ica.transform(cluster_clean)
            res = run_imitate(data_trf, num_bins=num_bins, return_loss=True)
            if res[-1] < min_loss: best_imi = copy.deepcopy(res)
        grids, _, fitted, fill_up, num_fill_up, _, _, _, loss = best_imi
        num_gen = int(max(num_fill_up))
        if num_gen == 0: continue
        points = np.empty((num_gen, 0))
        
        for d in range(len(data_trf[0])):
            fill = fitted[d] / np.sum(fitted[d]) * (num_gen - num_fill_up[d])  +  fill_up[d] #mixed distr
            fill_cdf = np.cumsum(fill) / num_gen  #normalize
            
            #generate points according to the cdf
            vals = np.random.rand(num_gen)
            val_bins = np.searchsorted(fill_cdf, vals)
            coords = np.array([np.random.uniform(grids[d][val_bins[i]], grids[d][val_bins[i]+1]) 
                               for i in range(num_gen)]).reshape(num_gen, 1)
            points = np.concatenate((points, coords), axis=1)
            
        gen_points = np.concatenate((gen_points, ica.inverse_transform(points)))
        gen_labels = np.append(gen_labels, [l]*num_gen)
            
    return gen_points, gen_labels



# MERGING

def merge(cluster_probs, cluster_params, data, quant_multiplier=10, olap_threshold=0.8, prints=False):
    if len(cluster_params) <= 1: return cluster_probs, cluster_params
    probs = np.copy(cluster_probs)
    params = copy.deepcopy(cluster_params)
    
    # merge two clusters
    def merge(a, b):
        probs[:, a] = (probs[:, a] + probs[:, b]) / 2
        probs[:, b] = 0
        olaps[b, :] = olaps[:, b] = 0
        member[a] = np.sum(probs[:, a])
        member[b] = 0
        params[a] = [(params[a][0] + params[b][0])/2, (params[a][1] + params[b][1])/2]
        params[b] = None
        for c in range(len(probs[0])):
            if c==a: continue
            olaps[a, c] = (member[a] - sum(probs[probs[:,a] > quant_multiplier*probs[:,c]][:,a])) / member[a]
            olaps[c, a] = (member[c] - sum(probs[probs[:,c] > quant_multiplier*probs[:,a]][:,c])) / member[c]
    
    # remove overgrown clusters
    nearest_clear_neighbor_dist = np.zeros(len(probs[0]))
    for i in range(len(probs[0])):
        clear_data = data[probs[:,i] > quant_multiplier*np.max(probs[:, np.delete(range(len(probs[0])), i)], axis=1)]
        if len(clear_data) == 0: continue
        distances = pairwise_distances(clear_data)
        distances[distances==0] = np.Inf
        nearest_clear_neighbor_dist[i] = np.average(np.min(distances, axis=0))
    #dist = pairwise_distances(data)
    #dist[dist==0] = np.Inf
    #dist_min = np.min(dist, axis=0)
    #avg_1nn_dist = np.average(dist_min) + np.std(dist_min)
    #probs[:, np.where(nearest_clear_neighbor_dist > avg_1nn_dist)[0]] = 0
    dist_threshold = np.average(nearest_clear_neighbor_dist) + 3*np.std(nearest_clear_neighbor_dist)
    remove = np.where(nearest_clear_neighbor_dist > dist_threshold)[0]
    probs[:, remove] = 0
    for r in remove:
        params[r] = None #delete parameters
    
    # quantify overlaps
    olaps = np.empty((len(probs[0]), len(probs[0])))
    member = np.sum(probs, axis=0)
    for A in range(len(probs[0])):
        for B in range(len(probs[0])):
            if A == B:
                olaps[A, B] = 0
            else:
                #olaps[A, B] = np.sum(np.multiply(probs[:,A], probs[:,A]-probs[:,B]))
                clear_A = sum(probs[probs[:,A] > quant_multiplier*probs[:,B]][:,A])
                olaps[A, B] = (member[A] - clear_A) / member[A]
    
    # merge
    outer_flag = True
    while outer_flag:
        outer_flag = False
        cl = prob_cluster_assignment(probs)
        for A in range(len(olaps)):
            if sum(cl==A) == 0: continue
            A_flag = False
            for B in range(A+1, len(olaps)):
                if sum(cl==B) == 0: continue
                if prints: print("Checking", A, "and", B)
                
                # high symmetric overlap
                if olaps[A, B] > olap_threshold and olaps[B, A] > olap_threshold:
                    merge(A, B)
                    A_flag = True
                    break
                
                if olaps[A, B] > 0.2 or olaps[B, A] > 0.2:
                    if merge_test(data, cl, A, B): 
                        merge(A, B)
                        A_flag = True
                        break
                
            if A_flag: 
                outer_flag = True
                break
    
    # remove empty clusters
    cl_sums = np.sum(cl, axis=0)
    remove = np.where(cl_sums == 0)[0]
    probs[:, remove] = 0
    for r in remove:
        params[r] = None
        
    return probs, list(filter(lambda p: p is not None, params))

def merge_test(data_, cl_, A, B):
    dA, dB, dAB = data_[cl_==A], data_[cl_==B], data_[np.logical_or(cl_==A, cl_==B)]
    dA_clean = remove_outliers_lof(dA) if len(dA) > 20 else dA
    dB_clean = remove_outliers_lof(dB) if len(dB) > 20 else dB
    dAB_clean = remove_outliers_lof(dAB) if len(dAB) > 20 else dAB
    repeat = 10
    norm_A = norm_B = norm_AB = 0
    for k in range(repeat):
        norm_A += 0 if len(dA)<5 else imitate_norm_test(dA_clean)
        norm_B += 0 if len(dB)<5 else imitate_norm_test(dB_clean)
        norm_AB += 0 if len(dAB)<5 else imitate_norm_test(dAB_clean)
    norm_avg = (len(dA)*norm_A/repeat + len(dB)*norm_B/repeat) / len(dAB)
    #print("Merge_test new result: ", norm_AB/repeat <= norm_avg)
    return norm_AB/repeat <= norm_avg

def imitate_norm_test(data):
    if np.sum(np.std(data, axis=0) == 0) > 0: 
        data = data[:,np.std(data, axis=0)>0]
    if len(data[0]) == 0: return 0
    # train ICA on cluster, transform everything
    ica = FastICA(n_components=len(data[0]), max_iter=500, tol=0.01, whiten='arbitrary-variance').fit(data)
    data_trf = ica.transform(data)
    
    # use Imitate
    grids, _, fitted, fill_up, num_fill_up, _, _, _ = run_imitate(data_trf)
    
    #err = np.sum([sum(fill_up[i]) / sum(fitted[i]) for i in range(len(fitted))])
    err = np.sum([sum(abs(fitted[i]-np.histogram(data_trf[:,i], bins=grids[i])[0])) / len(data) for i in range(len(fill_up))])
    return err

def prob_cluster_assignment(probs):
    probs_norm = normalize(probs, norm='l1')
    cl_choice = np.empty(len(probs))
    for i in range(len(cl_choice)):
        cl_choice[i] = -1 if sum(probs_norm[i])!=1 else np.random.choice(range(len(probs[0])), p=probs_norm[i])
    return cl_choice



################
# USER METHODS #
################
class Mimic:
    """Mimic generates points to mitigate a multi-cluster dataset's bias.
    
    Machine Learning can help overcome human biases in decision making by focussing 
    on purely logical conclusions based on the training data. If the training data 
    is biased, however, that bias will be transferred to the model and remains 
    undetected as the performance is validated on a test set drawn from the same 
    biased distribution.
    Existing strategies for selection bias identification and mitigation generally 
    rely on some sort of knowledge of the bias or the ground-truth. An exception 
    is the Imitate [1]_ algorithm that assumes no knowledge but comes with a strong 
    limitation: It can only model datasets with one normally distributed cluster 
    per class.
    MIMIC uses Imitate as a building block but relaxes this limitation. By allowing 
    mixtures of multivariate Gaussians, our technique is able to model multi-cluster 
    datasets and provide solutions for a substantially wider set of problems.   
    See our paper [2]_ for details.
    
    Attributes
    ----------
    params : dict(int: numpy.ndarray (2D))
        A label-indexed dictionary containing (mean, cov) tuples for each identified
        cluster belonging to this label.
    data : numpy.ndarray (2D)
        The dataset Mimic is fitted to.
    labels : numpy.array (1D)
        The corresponding labels. Labels need to be integer values.

    Methods
    -------
    fit(data, labels=[], centers=None)
        Fits the Mimic Gaussians to a dataset.
    predict_cluster(which_class)
        Predicts clusters for the input dataset.
    augment()
        Augments the fitted dataset to mitigate its bias.

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
    >>> from imitatebias.mimic import *

    Generate a dataset.
    >>> X, y = generateData(1000, 2, 2, seed=2210)

    Generate a biased dataset.
    >>> X_b, y_b, idcs_deleted = generateBias(X, y, 1, seed=2210)

    initialize Mimic
    >>> mim = Mimic()

    fit to the biased dataset
    >>> mim.fit(X_b, labels=y_b)

    predict cluster assignment for class 0
    >>> predicted_clusters = mim.predict_cluster(0)

    plot the resulting clusters for class 0
    >>> plt.scatter(X_b[y_b == 0, 0], X_b[y_b == 0, 1], c=predicted_clusters)
    >>> plt.show()

    augment the data
    >>> gen_p, gen_l = mim.augment()

    plot the result
    >>> plt.scatter(X_b[:,0], X_b[:,1], label='dataset')
    >>> plt.scatter(gen_p[:,0], gen_p[:,1], label='generated points')
    >>> plt.legend()
    >>> plt.show()

    """
    
    def __init__(self):
        """Mimic Constructor."""
        self.params = {}
        
    def fit(self, data, labels=[], centers=None):
        """Fits a bias-aware multivariate Gaussian Mixture Model per label to the data.
        
        See our paper [1]_ for details. This process is slow and substantially less
        powerful than the Imitate algorithm since it additionally needs to cluster the
        dataset into potentially biased overlapping clusters. We only recommend Mimic
        if the user is certain that the dataset contains multiple clusters. 
        
        Parameters
        ----------
        data : numpy.ndarray (2D)
            The input dataset.
        labels : numpy.array (1D), optional
            The corresponding labels if the dataset contains multiple classes.
        centers : numpy.ndarray (2D), optional
            A list [C1, ..., Cn] of n initial d-dimensional cluster centers 
            Ci = [Ci_0, ..., Ci_d]. If those centers are not provided, the clustering will
            be initialized with KMeans for the K that optimizes the Silhouette score.

	References
	----------
	.. [1] Katharina Dost, Hamish Duncanson, Ioannis Ziogas, Patricia Riddle, and Jörg
           Wicker. "Divide and Imitate: Multi-Cluster Identification and Mitigation of 
           Selection Bias." In: Advances in Knowledge Discovery and Data Mining - 26th 
           Pacific-Asia Conference, PAKDD 2022. Lecture Notes in Computer Science, vol. 
           13281, pp. 149-160. Springer, Cham (2022).
            
        Examples
        --------
        >>> from imitatebias.generators import *
        >>> from imitatebias.mimic import *

        Generate a dataset.
        >>> X, y = generateData(1000, 2, 2, seed=2210)

        Generate a biased dataset.
        >>> X_b, y_b, idcs_deleted = generateBias(X, y, 1, seed=2210)

        initialize Mimic
        >>> mim = Mimic()

        fit to the biased dataset
        >>> mim.fit(X_b, labels=y_b)



        """
        self.data = data
        self.labels = np.zeros(len(data)).astype(int) if len(labels) == 0 else labels
        
        for l in np.unique(self.labels):
            d = data[self.labels == l]
            k_init = findK(d)
            # params = mean/cov for each cluster
            probs_imi, params = run_mimic(d, k_init=k_init)

            # merge the resulting clusters
            probs_merge, params_merge = merge(probs_imi, params, d)

            # store parameters
            self.params[l] = params_merge
            
    def predict_cluster(self, which_class):
        """Predicts clusters for the input data.
        
        Assigns clusters to the input data belonging to a specified class. Those clusters
        are selected based on the maximum probability that a point belongs to each of the 
        clusters.

        Parameters
        ----------
        which_class : int
            Filters the data based on the initial labels.

        Returns
        -------
        numpy.array (1D)
            The array containing the assigned clusters.

        Examples
        --------
        >>> from imitatebias.generators import *
        >>> from imitatebias.mimic import *
        >>> import matplotlib.pyplot as plt

        Generate a dataset.
        >>> X, y = generateData(1000, 2, 2, seed=2210)

        Generate a biased dataset.
        >>> X_b, y_b, idcs_deleted = generateBias(X, y, 1, seed=2210)

        initialize Mimic
        >>> mim = Mimic()

        fit to the biased dataset
        >>> mim.fit(X_b, labels=y_b)
        
        predict cluster assignment for class 0
        >>> predicted_clusters = mim.predict_cluster(0)
        
        plot the resulting clusters for class 0
        >>> plt.scatter(X_b[y_b == 0, 0], X_b[y_b == 0, 1], c=predicted_clusters)
        >>> plt.show()



        """
        l = which_class
        probs = np.column_stack([multivariate_normal(self.params[l][i][0], self.params[l][i][1]).pdf(
            self.data[self.labels==l]) for i in range(len(self.params[l]))])
        return prob_cluster_assignment(probs)

    def augment(self):
        """Augments the fitted dataset to mitigate its bias.
        
        Generates points to fill in the gap between fitted and observed distributions
        in the input dataset.

        Returns
        -------
        numpy.ndarray (2D)
            Generated points.
        numpy.array (1D)
            Corresponding class labels.

        Examples
        --------
        >>> from imitatebias.generators import *
        >>> from imitatebias.mimic import *
        >>> import matplotlib.pyplot as plt

        Generate a dataset.
        >>> X, y = generateData(1000, 2, 2, seed=2210)

        Generate a biased dataset.
        >>> X_b, y_b, idcs_deleted = generateBias(X, y, 1, seed=2210)

        initialize Mimic
        >>> mim = Mimic()

        fit to the biased dataset
        >>> mim.fit(X_b, labels=y_b)

        augment the data
        >>> gen_p, gen_l = mim.augment()

        plot the result
        >>> plt.scatter(X_b[:,0], X_b[:,1], label='dataset')
        >>> plt.scatter(gen_p[:,0], gen_p[:,1], label='generated points')
        >>> plt.legend()
        >>> plt.show()



        """
        gen_points = np.empty((0, len(self.data[0])))
        gen_labels = []
        
        for l in np.unique(self.labels):
            cl_labels = self.predict_cluster(l)
            data_clean = self.data[self.labels==l][cl_labels >= 0]
            cl_labels_clean = cl_labels[cl_labels >= 0]

            points, point_cl_labels = Mimic_augment(data_clean, cl_labels_clean)
            gen_points = np.concatenate((gen_points, points))
            gen_labels = np.append(gen_labels, [l]*len(points))
        return gen_points, gen_labels