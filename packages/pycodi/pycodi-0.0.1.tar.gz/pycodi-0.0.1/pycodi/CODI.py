import numpy as np

class CODI:
    """
    Class for generating synthetic samples that incorporate independent source variability to input seed samples.
    """
    def __init__(self, variability_sources, random_state=None):
        """
        Initialize the CODI instance.
        
        Parameters:
        - variability_sources (list): List of functions or NumPy arrays that represent variability sources (f_1, f_2, ... in equation 1 in manuscript).
                                      If apriori functions are given, each run of the function should generate different numbers. 
                                      If a calibration dataset is given, a 2-d array is expected. The observations should be given in the rows, and data features in the columns.
                                      For the given variability functions or calibration datasets, the expected value of each feature is 0 (i.e. mean is 0).
        - random_state (int, optional): Seed for the random number generator to ensure reproducibility. Default is None (i.e. each run will generate different random numbers).
        """
        # sanity checks for input
        if not isinstance(variability_sources, list) and not isinstance(variability_sources, np.ndarray):
            raise ValueError('Variability sources must be provided as a 1-d list or NumPy array')
        for source in variability_sources:
            if not callable(source) and not isinstance(source, np.ndarray):
                raise ValueError('Each variability source must be a function or a NumPy array')
                
        self.variability_sources = variability_sources
        self.random_state = random_state
        self.rand = np.random.RandomState(random_state) # set random state for the numpy random number generator
    
    def generate_samples(self, X, seed_strategy, n_per_seed, y=None):
        """
        Generate an aribitrary number of synthetic samples based on the input seed X with a specified seed strategy (described in the parameters below).
        Current implementation assumes a Gaussian distribution for all sources of variability.

        Parameters:
            - X (numpy.ndarray): Input (training) seed data, which serves as a basis data to introduce variability into.
                                 A 2-d array is expected, with observations in rows and feature values in columns.
            - y (numpy.ndarray, optional): Sample labels/classes. 
                                           A 1-d array is expected where the number of entries matches the number of rows in X.
                                           If sample labels are relevant/applicable (e.g., all samples in X are from the sample class), y can be set to None (default behavior).
            - seed_strategy (str): Seed strategy, either 'all' or 'mean'.
                                   Variability will be introduced to samples in X based on the given seed strategy.
                                   If seed_strategy='all', every observation in X will serve as a seed measurement to which variability will be added onto (s_i in equation 1 in manuscript). 
                                   If seed_strategy='mean' and y=None, the mean observation in X will serve as a seed measurement.
                                   If seed_strategy='mean' and y!=None, the mean observation of each sample class will serve as a seed measurement.
            - n_per_seed (int): Number of samples to be generated per seed sample (dependent on the seed_strategy).

        Returns:
            - Tuple of generated synthetic data (X_gen) and their corresponding labels (y_gen).
        """
        # sanity checks for input
        if not isinstance(X, np.ndarray):
            raise ValueError('X must be a NumPy array')
        if y is not None and not isinstance(y, np.ndarray):
            raise ValueError('y must be a NumPy array or None')
        if seed_strategy not in ['all', 'mean']:
            raise ValueError('seed_strategy must be in {"all", "mean"}')
        if not isinstance(n_per_seed, int) or n_per_seed < 1:
            raise ValueError('n_per_seed must be an int (> 0)')
        if y is not None and X.shape[0] != y.shape[0]:
            raise ValueError('X and y must have the same number of observations')
            
        # convert to float arrays, 
        X = X.astype(float)
        if y is not None:
            y = y.astype(float) 
            
        X_seeds, y_seeds = self.__get_seed_samples(X, y, seed_strategy) # get the seed samples on which sample variability will be added (s_i in equation 1 of manuscript).
        
        X_gen = [] # to store the generated synthetic dataset
        y_gen = [] # to store the labels for the generated synthetic dataset
        for x_seed, y_seed in zip(X_seeds, y_seeds):
            X_gen_ = np.tile(x_seed, (n_per_seed, 1))
            for source in self.variability_sources:
                if callable(source):  # If variability source is a function
                    X_gen_ += np.array([source() for i in range(n_per_seed)])
                elif isinstance(source, np.ndarray): # If variability source is a calibration dataset
                    m = source.shape[0] # number of calibration observations
                    std = 1/np.sqrt(m) # standard deviation for the random number generator
                    X_gen_ += (self.rand.normal(0, std, (m, n_per_seed)).T @ source) # matrix multiplication: scale up and down each calibration observation and sum over all to create random matrix. then add it to the seed measurements
            X_gen.append(X_gen_)
            y_gen.append(np.tile(y_seed, n_per_seed))
        
        X_gen = np.vstack(X_gen)
        y_gen = None if y is None else np.hstack(y_gen)
            
        return X_gen, y_gen
    
    def __get_seed_samples(self, X, y, seed_strategy):
        """
        Internal helper function. Returns the 'seed' measurements from the array X based on the given seed_strategy.
        """
        X_seeds = []
        y_seeds = []
        if seed_strategy == 'all': # case when all samples in X are used as a seed
            X_seeds = list(X)
            y_seeds = [None]*len(X) if y is None else list(y)
        elif y is None: # case when the mean measurement is treated as a seed and there are no classes of samples
            X_seeds.append(X.mean(axis=0))
            y_seeds.append(None)
        else: # case when the mean measurement of each class is treated as a seed
            for y_ in set(y):
                X_seeds.append(X[y==y_].mean(axis=0))
                y_seeds.append(y_)
        return X_seeds, y_seeds