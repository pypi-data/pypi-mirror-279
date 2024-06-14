
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import pandas as pd
import numpy as np
import copy


class ClusterOptimizer:
    """
    This is a simple object simulating the GridSearchCV object from scikit-learn (sklearn), but only for clustering
    ...

    Attributes
    ----------
    estimator   : sklearn.cluster object
        an instantiated of the sklearn.cluster class as object object
    param_grid  : dictionary 
        the parameter grid to search through
    scoring     : list 
        a list of scoring functions to employ (from sklearn.metrics - unsupervised only)
    results     : pandas.DataFrame
        the results for a cluster object after running the clustering on all paramters and the corresonding scores. 
filter_noise    : Bool
        A boolean indicating if noise (labelled -1 after clustering) should be removed for computing the scoring results

    Methods
    -------
    optimize(X):
        Computes the results for the cluster method and all parameters. The results are sored as a pandas.DataFrame

    
    """
    _results_min_cols  = ['cluster_method','parameters']
    _dataframe_columns = ['cluster_method']
    
    def __init__(
        self, 
        estimator, 
        param_grid, 
        scoring            = [silhouette_score], 
#        n_jobs             = None, 
        refit              = True, 
#        cv                 = None, 
        verbose            = 0, 
#        pre_dispatch ='2*n_jobs', 
#        error_score=nan, 
        return_train_score = False,
        filter_noise       = True, 
    ):
        '''
        Constructs all the necessary attributes for the ClusterOptimizer object.

        Parameters
        ----------
            estimator   : sklearn.cluster object
                an instantiated of the sklearn.cluster class as object object
            param_grid  : dictionary 
                the parameter grid to search through
            scoring     : list  
                a list of scoring functions to employ (from sklearn.metrics - unsupervised only)
                default = [silhouette_score]
                Currently the following have been tested:
                   silhouette_score
                   davies_bouldin_score
                   calinski_harabasz_score
            filter_noise    : Bool
                A boolean indicating if noise (labelled -1 after clustering) should be removed for computing the scoring results, 
                as for exampleHDBSCAN might not cluster all samples
                default = True
        '''

        self.estimator     = estimator
        self.param_grid    = param_grid
        self.scoring       = scoring
        self.results       = pd.DataFrame() # empty dataframe
        self.filter_noise  = filter_noise

    def _compute_dataframe_cols(self):
        cols = self._dataframe_columns
        if self.param_grid_keys:
            cols += [f'cluster_param__{x}' for x in self.param_grid_keys]
        if self.scoring_map:
            cols += [f'{x}' for x in self.scoring_map]
        return cols
    
    @property
    def estimator(self):
        return self.__estimator

    @property
    def estimator_name(self):
        return self.__estimator_name

    @estimator.setter
    def estimator(self, value):
        # need to check for estimator methods fit, predicts etc. 
        self.__estimator      = value
        self.__estimator_name = value.__class__.__name__
    
    @property
    def param_grid(self):
        return self.__param_grid

    @property
    def param_grid_keys(self):
        return self.__param_grid_keys
    
    @param_grid.setter
    def param_grid(self, value):
        param_grid_keys = sorted(list(value.keys()))
        if param_grid_keys != []:
            self.__param_grid      = value
            self.__param_grid_keys = param_grid_keys
    
    @property
    def scoring(self):
        return self.__scoring

    @property
    def scoring_map(self):
        return self.__scoring_map

    @scoring.setter
    def scoring(self, value):
        if value != None and isinstance(value,list):
            self.__scoring      = value
            self.__scoring_map  = dict([(x.__name__,x) for x in value])
        else:
            self.__scoring      = []
            self.__scoring_map  = dict()

    @property
    def scoring_strs(self):
        return [x.__name__ for x in self.__scoring]
        
    def _wrapper(self,X,obj,my_args = {}):
        #print(my_args)
        # create a copy of the original object
        o = copy.deepcopy(obj)
        # set individual (new) parameters
        for param,param_val  in my_args.items():
            setattr(o,param,param_val)

        # cluster the data
        labels = o.fit_predict(X)
        # score according to supplied scores
        scores_to_do = self.scoring
        score_results = {}

        # if required: deal with unassigned samples (like in HDBScan when label is -1)
        if self.filter_noise:
            X = X[labels>=0]
            labels = labels[labels>=0]

        
        for score_to_do in scores_to_do:
            #print(f'{score_to_do}')
            if len(X)>0:
                score = score_to_do(X,labels)
            else:
                score = -np.inf
            score_results[score_to_do.__name__] = score

        # save the results
        # create first column
        dict_row = {
            self._results_min_cols[0]:self.estimator_name,
        }    
        # create parameter columns
        
        dict_row.update(dict([(f'cluster_param__{x}',my_args[x]) for x in self.param_grid_keys]))
        dict_row.update(score_results)
        # convert dict to dataframe
        df_row = pd.DataFrame([dict_row])

        # use new dataframe is current is empty or use existing and merge
        if self.results.empty:
            self.results = df_row
        else:
            self.results = pd.concat([self.results, df_row], ignore_index=True)

    
    def optimize(self,X):
        return self._optimize(X,self.estimator,self.param_grid)
        
    def _optimize(self,X,estimator,params,use_params = {}):

        # if param is not empty
        if params: # checks if not empty
            # need top copy so the original params are not empty later
            params_new = params.copy()
            # get the first key 
            k = list(params_new.keys())[0]
            vals = params_new.pop(k)
            for val in vals:
                #print(k,vals)
                use_params_new = dict({k:val})
                use_params_new.update(use_params)
                self._optimize(X,estimator,params_new,use_params_new)
        else:
            # run program
            self._wrapper(X,estimator,use_params)        
    
    
    def __str__(self):
        return self.__repr__()
    def __repr__(self):
        return f'<<{self.param_grid}>>'


    
