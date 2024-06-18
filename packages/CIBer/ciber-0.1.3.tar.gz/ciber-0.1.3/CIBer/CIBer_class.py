import os, sys, scipy
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import warnings
from .CIBer_Engineering import Discretization, Joint_Encoding

sys.path.append(os.path.dirname(scipy.stats.__file__))                          # read _stats.pyd
from _stats import _kendall_dis

class CIBer():
    def __init__(self, cont_col=[], asso_method='modified', min_asso=0.95, alpha=1, 
                 disc_method="norm", **kwargs):
        self.cont_col = cont_col
        if asso_method.lower() == "modified":
            self.asso_method = self._modified_tau
        else:
            self.asso_method = asso_method.lower()
        self.min_asso = min_asso
        self.alpha = alpha
        self.disc_method = disc_method.lower()
        self.discretizer = Discretization(cont_col, self.disc_method, **kwargs)
        self.encoder = Joint_Encoding()
        
        self.distance_matrix_ = dict()
        self.cluster_book = dict()
        assert asso_method.lower() in ["spearman", "pearson", "kendall", "modified"]
        assert min_asso >= 0 and min_asso <= 1
        assert alpha > 0
    
    @staticmethod
    def _modified_tau(x, y):    # modified from scipy.stats._stats_py.kendalltau
        # If most of the numbers are of the same group, they should not be considered as a cm cluster
        if len(np.unique(x)) <= 2 or len(np.unique(y)) <= 2:  # Not accept Binary as cm cluster
            return 0

        # sort on y and convert y to dense ranks
        perm = np.argsort(y)
        x, y = x[perm], y[perm]
        y = np.r_[True, y[1:] != y[:-1]].cumsum(dtype=np.intp)

        # stable sort on x and convert x to dense ranks
        perm = np.argsort(x, kind='mergesort')
        x, y = x[perm], y[perm]
        x = np.r_[True, x[1:] != x[:-1]].cumsum(dtype=np.intp)
        
        dis = _kendall_dis(x, y)                # number of discordant pairs
        tot = (x.size * (x.size - 1)) // 2
        return min(1., max(-1., (tot - 2*dis)/tot))
        
    def _get_association(self, X_train):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            asso_matrix = pd.DataFrame(data=X_train).corr(method=self.asso_method).to_numpy()
        
        distance_matrix = np.nan_to_num(1 - np.absolute(asso_matrix), nan=1)
        AGNES = AgglomerativeClustering(metric='precomputed', linkage='complete', 
                                        distance_threshold=1-self.min_asso, n_clusters=None)
        AGNES.fit(distance_matrix)
        AGNES_clusters = AGNES.labels_
        return distance_matrix, sorted([np.where(AGNES_clusters == cluster)[0].tolist() for cluster in np.unique(AGNES_clusters)])
    
    def _get_prior_prob(self, y_train):
        # prior_prob: dict() key is class, value is the prior probability of this class
        # class_idx:  dict() key is class, value is a list containing the indices of instances for this class
        classes, counts = np.unique(y_train, return_counts=True)
        self.prior_prob = dict(zip(classes, counts/len(y_train)))
        self.class_idx = {k: np.where(y_train == k)[0].tolist() for k in classes}
        self.y_cate = pd.Categorical(y_train, categories=classes)
    
    def fit(self, X_train, y_train):
        ncol = np.shape(X_train)[1]
        self.cate_col = list(set(np.arange(ncol)) - set(self.cont_col))
        self.encoder.cate_col = self.cate_col
        self._get_prior_prob(y_train)
        
        if len(self.cont_col) > 0:
            X_train = self.discretizer.fit_transform(X_train, y_train)
        
        if len(self.cate_col) > 0:
            X_train = self.encoder.fit_transform(X_train)
        
        self.transform_X_train = X_train
        for c, idx in self.class_idx.items():
            self.distance_matrix_[c], self.cluster_book[c] = self._get_association(self.transform_X_train[idx,:])
    
    def _get_cond_prob(self, X_train, X_test):
        ncol = np.shape(X_train)[1]
        self.cond_prob = dict() # key is column, value dict: key is class, value is corresponding probabilities
        self.cond_cum_prob = dict() # key is column, value dict: key is class, value is corresponding cumulative probabilities
        self.prev_idx = dict()  # key is column, value dict: key is value, value is previous value
            
        for col in range(ncol):
            categories = np.unique(np.append(X_train[:,col], X_test[:,col]))
            x_cate = pd.Categorical(X_train[:,col], categories=categories)
            Laplace_tab = pd.crosstab(x_cate, self.y_cate, dropna=False) + self.alpha
            density_tab = Laplace_tab.apply(lambda x: x/x.sum())
            
            if col in self.cont_col and self.disc_method == "ndd":
                density_tab = density_tab.rolling(window=3, min_periods=2, center=True).sum()
                density_tab = density_tab / density_tab.sum(axis=0)
                
            density_tab.loc[-1.0] = 0
            idx_lst = sorted(density_tab.index)
            density_tab = density_tab.reindex(index=idx_lst)
            self.cond_prob[col] = density_tab.to_dict()
            self.cond_cum_prob[col] = density_tab.cumsum().to_dict()
            self.prev_idx[col] = dict(zip(idx_lst[1:], idx_lst[:-1]))
        
    def predict_proba(self, X_test):
        if len(self.cont_col) > 0:
            X_test = self.discretizer.transform(X_test)
        
        if len(self.cate_col) > 0:
            X_test = self.encoder.transform(X_test)
        
        self.transform_X_test = X_test
        self._get_cond_prob(self.transform_X_train, self.transform_X_test)
        
        y_val = []
        for c in self.cluster_book.keys():
            indep_prob = {cluster[0]: self.cond_prob[cluster[0]][c] for cluster in self.cluster_book[c] if len(cluster) == 1}
            clust_prob = [{col: self.cond_cum_prob[col][c] for col in cluster} for cluster in self.cluster_book[c] if len(cluster) > 1]

            df_test = pd.DataFrame(X_test)
            prob = self.prior_prob[c] * df_test[indep_prob.keys()].replace(indep_prob).prod(axis=1)

            for comon_prob in clust_prob:
                prob_inf = df_test[comon_prob.keys()].replace(comon_prob).min(axis=1)
                prob_sup = df_test[comon_prob.keys()].replace(self.prev_idx).replace(comon_prob).max(axis=1)
                prob = prob * np.maximum(prob_inf - prob_sup, 1e-5)
            
            y_val.append(prob)
            
        return np.array(y_val).T / np.sum(y_val, axis=0).reshape(-1, 1)
    
    def predict(self, X_test):
        y_proba = self.predict_proba(X_test)
        class_label = np.array(list(self.class_idx.keys()))
        return class_label[list(np.argmax(y_proba, axis=1))]