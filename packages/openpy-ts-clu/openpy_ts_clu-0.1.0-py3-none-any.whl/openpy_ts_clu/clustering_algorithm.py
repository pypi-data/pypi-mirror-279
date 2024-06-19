# -*- coding: utf-8 -*-
# @Time    : 05/06/2023
# @Author  : Ing. Jorge Lara
# @Email   : jlara@iee.unsj.edu.ar
# @File    : clustering_algorithm.py
# @Software: PyCharm

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'
import tqdm
from scipy import stats
from tqdm.autonotebook import tqdm
from sklearn.cluster import KMeans
from tslearn.clustering import TimeSeriesKMeans
from tslearn.barycenters import euclidean_barycenter
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.manifold import TSNE, MDS
from typing import List, Union
import seaborn as sns

clu_no_centroid = ['DBSCAN', 'Birch', 'GaussianMixture', 'OPTICS', 'Agglomerative', 'Spectral', 'SOM']
model_with_eps = ['DBSCAN', 'OPTICS']


def change_dict_key(dictionary, old_key, new_key, default_value=None):
    dictionary[new_key] = dictionary.pop(old_key, default_value)


def set_tittle_cluster(key):
    """
    Set the title of the cluster
    :param key: key of the cluster
    :return:
    """
    if key == 'centroid':
        return 'Centroid'
    if key == 'mean':
        return 'Mean'
    if key == 'euclidean':
        return "Euclidean"



def set_tittle_cluster(case: bool = None, gamma=None):
    if case == 'centroid':
        return 'Centroid'
    if case == 'mean':
        return 'Mean'
    if case == 'euclidean':
        return "Euclidean"


def dict_clu_models():
    dict_models = {
        'KMeans': KMeans,
        'TSKMeans': TimeSeriesKMeans
    }
    return dict_models



class clustering_kmeans:

    def __init__(
            self,
            users=None,
            model: str = 'KMeans',
            metric: str = 'dtw',
            type_dr: str = None,
            n_components: int = 2,
            seed: int = 123,
            df_sce: pd.DataFrame = None,
    ):
        """
        class to content the clustering algorithm
        :param users: name of the users
        :param model: model to use
        :param metric: metric to use
        :param type_dr: type of dimensional reduction
        :param n_components: number of components
        :param seed: seed of the model
        :param df_sce: dataframe with the data to use
        """

        if users is None:
            users = df_sce.columns[:-11]
        self.model = model
        self.users = users
        self.metric = metric
        self.type_dr = type_dr
        self.n_components = n_components
        self.seed = seed
        self.df_sce = df_sce
        self.n_jobs = -1
        self.max_iter = 10
        self.acum_bar = None

    def _prepare_data_to_clu(
            self,
            op: int = 1
    ):

        dict_sce = dict()
        df_users_mean = pd.DataFrame()
        df_user = pd.DataFrame()
        for k in self.users:
            df_aux = self.get_df_aux(k)
            dict_sce[k] = df_aux
            user_mean = self._outlier_removal(df_aux, df_aux.columns, op, k)
            df_aux.loc[:, 'user'] = k
            df_user = pd.concat([df_user, df_aux], axis=0)
            df_users_mean = pd.concat([df_users_mean, user_mean], axis=0)
        df_users_mean.interpolate(inplace=True, axis=1)
        dict_sce['means'] = df_users_mean

        # Scaler data
        dict_scaler = self._scaler_data(dict_sce)
        ts_scaler = dict_scaler['dataset'].values
        # Dimensional reduction
        if self.type_dr is not None:
            data = self.dimensionality_reduction().fit_transform(ts_scaler)
        else:
            data = ts_scaler
        return {'data': data, 'ts_scaler': ts_scaler, 'dict_scaler': dict_scaler, 'data_user': df_user.sort_index()}


    def get_df_aux(self, user):
        data = self.df_sce.loc[:, [user, 'count_day', 'date']].copy()
        aux = []
        for i in data['count_day'].unique():
            aux.append(data[data['count_day'] == i].shape[0])
        n_meas = max(aux)
        data = data.reset_index()
        data[data.columns[0]] = data[data.columns[0]].apply(lambda x: x.strftime('%H:%M'))
        data.set_index(data.columns[0], inplace=True)
        day_aux = list(data.count_day.value_counts()[data.count_day.value_counts() == n_meas].index)
        data = data[data.count_day.isin(day_aux)]
        data.reset_index(inplace=True)
        data.drop(columns=['count_day'], inplace=True)
        df_aux = pd.pivot(
            data,
            index=['date'],
            columns=['index']
        )
        df_aux.columns = ['_'.join(col) for col in df_aux.columns.values]
        df_aux.columns = [item.replace(f'{user}_', "") for item in df_aux.columns]
        return df_aux

    def _outlier_removal(self, df_aux, cols, op=1, user=None):
        data_graf = []
        vector_Prom = []
        aux = 0
        for i in cols:
            data = df_aux[i]
            size = len(data)  # determinar la longitud de los datos
            if size != 0:
                if op == 1:
                    # print(k, i)
                    Q1 = data.quantile(0.25)
                    Q3 = data.quantile(0.75)
                    IQR = Q3 - Q1
                    lower_lim = Q1 - 1.5 * IQR
                    upper_lim = Q3 + 1.5 * IQR
                    outliers_low = (data < lower_lim)
                    outliers_up = (data > upper_lim)
                    data[outliers_low] = lower_lim
                    data[outliers_up] = upper_lim
                if op == 2:
                    z_critical = stats.norm.ppf(q=0.999)
                    mean = data.mean()  # determina la media.
                    std = data.std()  # Get the population standard deviation
                    margin_of_error = z_critical * (std / math.sqrt(size))  # margen de error
                    confidence_interval = (mean - margin_of_error, mean + margin_of_error)
                    int_min = mean - margin_of_error
                    int_max = mean + margin_of_error
                    data = data[(data >= int_min)]  # filtrar obteniendo los valores de mayores al min
                    data = data[(data <= int_max)]  # filtrar obteniendo los valores de menores al min
            data_graf.append(data)
            df_mean = data_graf[aux].mean()
            vector_Prom.append(df_mean)
            aux += 1

        user_mean = pd.DataFrame(vector_Prom, index=cols, columns=[user]).T
        user_mean.interpolate(inplace=True, axis=1)
        return user_mean

    def prepare_data_to_clu(
            self,
            atypical: bool = True
    ):
        data = self.df_sce.copy()
        aux = []
        for i in data['count_day'].unique():
            aux.append(data[data['count_day'] == i].shape[0])
        n_meas = max(aux)
        data = data.reset_index()
        data[data.columns[0]] = data[data.columns[0]].apply(lambda x: x.strftime('%H:%M'))
        data.set_index(data.columns[0], inplace=True)
        day_aux = list(data.count_day.value_counts()[data.count_day.value_counts() == n_meas].index)
        data = data[data.count_day.isin(day_aux)]
        if atypical:
            if type(self.users) == str:
                self.users = self.users.split()
            # remove atypical datasets
            for col in self.users:
                Q1 = data.loc[:, col].quantile(0.25)
                Q3 = data.loc[:, col].quantile(0.75)
                IQR = Q3 - Q1
                lower_lim = Q1 - 1.5 * IQR
                upper_lim = Q3 + 1.5 * IQR
                outliers_low = (data.loc[:, col] < lower_lim)
                outliers_up = (data.loc[:, col] > upper_lim)
                data.loc[:, col][(outliers_low | outliers_up)] = np.nan
                '''
                data.loc[:, col] = data.loc[:, col].apply(
                    lambda x: seasonal.nullify_outliers(x, period=n_meas),
                    axis='index'
                )
                '''
                if data[col].isna().sum().sum() > 0:
                    data[col].ffill(inplace=True)
        data.reset_index(inplace=True)
        # data['user'] = data.columns[1]
        sce_days = dict()
        for user in self.users:
            sce_days[user] = pd.pivot(
                data,
                values=user,
                index=['date'],
                columns=data.columns[0]
            )
        return sce_days

    def _scaler_data(self, dict_data, label=None):
        dict_scaler = {}
        df_scaler = dict_data['means']
        user_aux = list(dict_data['means'].index)
        cols = df_scaler.columns
        scalars = {}
        for i in cols:
            scaler = MinMaxScaler(feature_range=(0, 1))
            s_s = scaler.fit_transform(df_scaler[i].values.reshape(-1, 1))
            s_s = np.reshape(s_s, len(s_s))
            scalars['scaler_' + i] = scaler
            df_scaler[i] = s_s
        dict_scaler['dataset'] = df_scaler
        dict_scaler['scaler'] = scalars
        dict_scaler['user'] = user_aux
        return dict_scaler

    def _inverse_transform(
            self,
            yhat,
            dict_scaler,
    ):
        for index, i in enumerate(dict_scaler['dataset'].columns[:-2]):
            scaler = dict_scaler['scaler']['scaler_' + i]
            yhat[index, :] = scaler.inverse_transform(yhat[index, :].reshape(-1, 1)).reshape(yhat.shape[1], )
        return yhat

    def scaler_data(self, data):
        from sklearn.preprocessing import StandardScaler, MinMaxScaler
        scaler = MinMaxScaler()
        dict_scaler = {
            'dataset': scaler.fit_transform(data.T).T,
            'scaler': scaler
        }
        return dict_scaler

    def train_clu_model(
            self,
            n_clusters: int = 3,
            num_iteration: int = 500,
            points_2d: bool = False,
            view_clu: bool = False,
            acum_bar: bool = True,
            inv_scaler: bool = True,
            parameters_clu: dict = None
    ):
        """
        Train the clustering model with the parameters given
        :param n_clusters: number of clusters to use
        :param num_iteration: number of iterations
        :param points_2d: plot the points in 2d
        :param view_clu: plot the clusters view
        :param acum_bar: plot acumulated bar
        :param inv_scaler: inverse the scaler
        :param parameters_clu: parameters of the clustering model in development
        :return:
        """
        if parameters_clu is not None:
            parameters = parameters_clu
        else:
            parameters = {
                'type_dr': self.type_dr,
                'model': self.model,
                'metric': self.metric,
                'n_jobs': self.n_jobs,
                'max_iter': self.max_iter,
                'seed': self.seed,
                'n_clusters': n_clusters,
                'num_iteration': num_iteration,
                'points_2d': points_2d,
                'view_clu': view_clu
            }

        self.acum_bar = acum_bar
        mdl_clu = _choice_clu_model(parameters)
        dict_data = self._prepare_data_to_clu()
        train_mdl = mdl_clu.check_model(
            dict_data['data'],
            dict_data['ts_scaler'],
            dict_data['dict_scaler'],
            n_clusters=parameters['n_clusters'],
            inv_scaler=inv_scaler
        )
        df_aux = pd.DataFrame()
        for k in train_mdl['dataset'].user.unique():
            cluster = train_mdl['dataset'][train_mdl['dataset'].user == k].cluster.values[0]
            df_user = dict_data['data_user'][dict_data['data_user'].user == k]
            df_user.loc[:, ['cluster']] = cluster
            df_aux = pd.concat([df_aux, df_user], axis=0)
        df_aux = df_aux.sort_index()
        train_mdl['data_user'] = df_aux
        if points_2d:
            self.clu_model_2d(train_mdl)
        return train_mdl

    def _get_dict_parameters(self):
        parameters_clu = {
            'type_dr': self.type_dr,
            'model': self.model,
            'metric': self.metric,
            'n_jobs': self.n_jobs,
            'max_iter': self.max_iter,
            'seed': self.seed,
            'n_clusters': None,
            'num_iteration': None,
            'points_2d': None,
            'view_clu': None
        }
        return parameters_clu

    def _test_hyperparameters(
            self,
            parameters,
            all_barycenters: bool = False,
            centroid: bool = None,
            mean: bool = None,
            euclidean: bool = None,
            plt_all_graphs: bool = False
    ):
        parameters_clu = self._get_dict_parameters()
        dict_clu = {}
        for i in parameters.index:
            if i != 0:
                parameters_clu['n_clusters'] = parameters.loc[i, 'Clusters range (K)']
                dict_clu[parameters.loc[i, 'Clusters range (K)']] = self.performance_to_clu(
                    self.cluster_ts_extraction(
                        all_barycenters=all_barycenters,
                        plt_all_graphs=plt_all_graphs,
                        parameters_clu=parameters_clu
                    )
                )
        return dict_clu

    def _performance_model(self):
        pass

    def cluster_ts_extraction(
            self,
            n_clusters: int = 3,
            max_iter: int = 10,
            tol: float = 1e-3,
            gamma: float = 1.0,
            verbose: bool = False,
            all_barycenters: bool = False,
            centroid: bool = None,
            mean: bool = None,
            euclidean: bool = None,
            plt_n_cluster: int = 1,
            plt_barycenters: bool = None,
            plt_summary: bool = None,
            plt_clusters: bool = None,
            plt_pct_clu: bool = None,
            plt_count_clu: bool = None,
            plt_all_graphs: bool = False,
            parameters_clu: dict = None
    ):
        """
        Extract the clusters baricentres and plot the results
        :param n_clusters: number of clusters to use
        :param max_iter: maximum number of iterations
        :param tol: tolerance of the model (development)
        :param gamma: gamma of the model (development)
        :param verbose: view the results (development)
        :param all_barycenters: get all the barycenters
        :param centroid: boolean to use the centroid
        :param mean: boolean to use the mean
        :param euclidean: boolean to use the euclidean
        :param plt_n_cluster: plot the number of clusters
        :param plt_barycenters: plot the barycenters
        :param plt_summary: plot the summary
        :param plt_clusters: plot the clusters
        :param plt_pct_clu: plot the percentage of clusters
        :param plt_count_clu: plot the count of clusters
        :param plt_all_graphs: plot all the graphs together
        :param parameters_clu: parameters of the clustering model in development
        :return:
        """
        ## Parameters - barycenters
        bool_bar = {
            'centroid': centroid,
            'mean': mean,
            'euclidean': euclidean,
        }
        bool_plots = {
            'plt_n_cluster': plt_n_cluster,
            'plt_barycenters': plt_barycenters,
            'plt_summary': plt_summary,
            'plt_clusters': plt_clusters,
            'plt_pct_clu': plt_pct_clu,
            'plt_count_clu': plt_count_clu
        }
        if all_barycenters:
            bool_bar['centroid'] = True
            bool_bar['mean'] = False
            bool_bar['euclidean'] = True

        if plt_all_graphs:
            bool_plots['plt_barycenters'] = True
            bool_plots['plt_summary'] = True
            bool_plots['plt_clusters'] = True
            bool_plots['plt_pct_clu'] = True
            bool_plots['plt_count_clu'] = True

        train_model = self.train_clu_model(n_clusters=n_clusters, inv_scaler=False, parameters_clu=parameters_clu)
        dict_barycenters = self._dict_barycenter(train_model, bool_bar, bool_plots, max_iter, tol, verbose, gamma)
        dict_barycenters['dataset'] = train_model['data_user']
        return dict_barycenters

    def _find_barycenter(self, train_model, bool_bar, max_iter, tol, verbose, gamma, dict_bar):
        # Find barycentre's
        bar = barycenter(train_model['ts_clustered'], max_iter, tol, verbose, gamma)
        if bool_bar['centroid']:
            dict_bar['centroid'] = bar.centroid(
                train_model['clu_model'],
                train_model['ts_scaler'],
                train_model['data']
            )
        if bool_bar['mean']:
            dict_bar['mean'] = bar.mean()
        if bool_bar['euclidean']:
            dict_bar['euclidean'] = bar.euclidean()
        return dict_bar

    def _dict_barycenter(self, train_model, bool_bar, bool_plots, max_iter, tol, verbose, gamma, label: str = None):

        dict_bar = {
            'dataset': train_model['dict_scaler']['dataset'],
            'clusters': [x.T for x in train_model['ts_clustered']]
        }
        # Find baricentres
        dict_bar = self._find_barycenter(train_model, bool_bar, max_iter, tol, verbose, gamma, dict_bar)
        ## Scaler data
        for key, values_scales in dict_bar.items():
            if key == 'dataset':
                dict_bar['dataset'] = pd.DataFrame(
                    self._inverse_transform(values_scales.values.T, train_model['dict_scaler']).T,
                    columns=train_model['dict_scaler']['dataset'].columns,
                    index=train_model['dict_scaler']['dataset'].index
                )
            else:
                for x in values_scales:
                    self._inverse_transform(x, train_model['dict_scaler'])
        dict_bar['dataset']['cluster'] = train_model['cluster_labels']
        dict_bar['dataset']['user'] = train_model['dict_scaler']['user']
        # Plots - Barycenters
        self._plot_barycenters(bool_plots, gamma, dict_bar, train_model, label)
        return dict_bar

    def _plot_barycenters(self, bool_plots, gamma, dict_bar, train_model, label):
        if bool_plots['plt_summary']:
            fx_clu_plots.all_barycenter(True, False, bool_plots['plt_n_cluster'], gamma, dict_bar, label)
        if bool_plots['plt_barycenters']:
            fx_clu_plots.all_barycenter(False, True, bool_plots['plt_n_cluster'], gamma, dict_bar, label)
        ## !! Need review
        if bool_plots['plt_clusters']:
            self._view_cluster(len(dict_bar['clusters']), dict_bar, gamma, label)
        if bool_plots['plt_pct_clu']:
            fx_clu_plots.plt_pct_clu(train_model['cluster_labels'], label)
        if bool_plots['plt_count_clu']:
            fx_clu_plots._clu_barplot(dict_bar, label)

    def get_dendograma(self, n_cluster: int = None):
        import scipy.cluster.hierarchy as shc
        dict_data = self._prepare_data_to_clu()
        plt.figure(figsize=(10, 7))
        plt.title("Dendrograms")
        dend = shc.dendrogram(shc.linkage(dict_data['data'], method='ward'))
        if n_cluster is not None:
            plt.axhline(y=n_cluster, color='r', linestyle='--')
        plt.show()

    def optimal_number_of_clusters(
            self,
            max_clusters: int = 10,
            plot: bool = True,
            n_clusters: int = 3,
            points_2d: bool = False,
            view_clu: bool = False,
            plt_metrics: bool = False

    ):
        """
        Runs KMeans n times (according to max_cluster range)

        datasets: pd.DataFrame or np.array
            Time Series Data
        max_clusters: int
            Number of different clusters for KMeans algorithm
        metric: str
            Distance metric between the observations
        Returns:
        -------
        None
        """
        parameters = {
            'type_dr': self.type_dr,
            'model': self.model,
            'metric': self.metric,
            'n_jobs': self.n_jobs,
            'max_iter': self.max_iter,
            'seed': self.seed,
            'n_clusters': n_clusters,
            'max_clusters': max_clusters,
            'points_2d': points_2d,
            'view_clu': view_clu

        }
        dict_data = self._prepare_data_to_clu()
        # Number the test
        metrics = self._run_optimal_number_of_clusters(
            parameters,
            dict_data['data'],
            dict_data['ts_scaler'],
            dict_data['dict_scaler']
        )
        if plot:
            metrics_aux = metrics.copy()

            if plt_metrics:
                fx_clu_plots.plot_multi(data=metrics_aux, x='Clusters range (K)', model=self.model)
                plt.show()
        # print(metrics)
        return metrics

    @staticmethod
    def _calculate_indices(data, clu_labels, dict_index):
        if len(np.unique(clu_labels)) > 1:
            dict_index['Silhouette'].append(silhouette_score(data, clu_labels))
            dict_index['Davies Bouldin'].append(davies_bouldin_score(data, clu_labels))
            dict_index['Calinski Harabasz'].append(calinski_harabasz_score(data, clu_labels))
        else:
            dict_index['Silhouette'].append(np.NaN)
            dict_index['Davies Bouldin'].append(np.NaN)
            dict_index['Calinski Harabasz'].append(np.NaN)
        return dict_index

    def _run_optimal_number_of_clusters(
            self,
            parameters,
            data,
            ts_scaler,
            dict_scaler
    ):
        # list empty for metrics
        dict_metrics = {
            'Silhouette': [],
            'Davies Bouldin': [],
            'Calinski Harabasz': [],
            'Clusters range (K)': [],
            'Distortions': []
        }

        clusters_range = range(1, parameters['max_clusters'] + 1)
        for k in tqdm(clusters_range):
            parameters['n_clusters'] = k
            clu = _choice_clu_model(parameters)
            clu_model = clu.check_model(data, ts_scaler, dict_scaler)
            clu_labels = clu_model['clu_model'].fit_predict(data)
            dict_metrics = self._calculate_indices(data, clu_labels, dict_metrics)
            dict_metrics['Clusters range (K)'].append(k)
            dict_metrics['Distortions'].append(clu_model['clu_model'].inertia_)

        df_metrics = pd.DataFrame.from_dict(
            dict_metrics
        ).drop_duplicates(
            subset='Clusters range (K)', keep="last"
        ).sort_values(
            'Clusters range (K)'
        ).reset_index(drop=True)
        return df_metrics

    def dimensionality_reduction(self):
        if self.type_dr == 'tsne':
            return TSNE(
                n_components=self.n_components,
                init='pca',
                random_state=self.seed
            )
        if self.type_dr == 'mds':
            return MDS(
                n_components=self.n_components,
                n_init=3,
                max_iter=100,
                random_state=self.seed
            )

    # Visualization for obtained clusters
    def clu_model_2d(self, train_model):
        # Visualization for obtained clusters
        u_labels = np.unique(train_model['cluster_labels'])
        # Centroids Visualization
        plt.figure(figsize=(16, 10))
        centroids = train_model['clu_model'].cluster_centers_
        plt.scatter(centroids[:, 0], centroids[:, 1], s=150, color='r', marker="x")
        # Downsize the datasets into 2D
        if train_model['data'].shape[1] > 2:
            self.type_dr = 'tsne'
            data = self.dimensionality_reduction().fit_transform(train_model['data'])
            for u_label in u_labels:
                cluster_points = data[(train_model['cluster_labels'] == u_label)]
                plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=u_label)
        else:
            for u_label in u_labels:
                cluster_points = train_model['data'][(train_model['cluster_labels'] == u_label)]
                plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=u_label)
        plt.title('Clustered Data')
        plt.xlabel("Feature space for the 1st feature")
        plt.ylabel("Feature space for the 2nd feature")
        plt.grid(True)
        plt.legend(title='Cluster Labels')
        plt.show()

    def _view_cluster(
            self,
            n_clusters: int = None,
            dict_bar: dict = None,
            gamma: float = None,
            label: str = None
    ):
        n_cols = len(dict_bar.keys()) - 2
        if n_cols == 1:
            fig_3, ax = plt.subplots(nrows=n_clusters, ncols=1, sharex=True)
            for key, value in dict_bar.items():
                if key == 'dataset' or key == 'clusters':
                    pass
                else:
                    for index, series in enumerate(dict_bar[key]):
                        ax[index].plot(dict_bar['clusters'][index], "k-", alpha=0.15)
                        ax[index].plot(series, c='r')
                        ax[index].set_ylabel(f'Cluster {index}')
                        if index == n_clusters - 1:
                            ax[index].set_xlabel('Number of measurements')
                        if index == 0:
                            myTitle = f"Cluster with {set_tittle_cluster(key)}"
                            ax[index].set_title(myTitle, loc='center', wrap=True)
            plt.legend()
            if label is None:
                fig_3.suptitle(f"Nro. {n_clusters} Clusters with {self.type_dr} dimentional reduction ")
            else:
                fig_3.suptitle(f"Nro. {n_clusters} Clusters with {self.type_dr} dimentional reduction - Label: {label}")
        else:
            fig_3, ax = plt.subplots(nrows=n_clusters, ncols=len(dict_bar.keys()) - 2, sharex=True)
            n = 0
            for key, value in dict_bar.items():
                if key == 'dataset' or key == 'clusters':
                    pass
                else:
                    for index, series in enumerate(dict_bar[key]):
                        ax[index, n].plot(dict_bar['clusters'][index], "k-", alpha=0.15)
                        ax[index, n].plot(series, c='r')
                        if n == 0:
                            ax[index, n].set_ylabel(f'Cluster {index}')
                        if index == n_clusters - 1:
                            ax[index, n].set_xlabel('Number of measurements')
                        if index == 0:
                            myTitle = f"Cluster with {set_tittle_cluster(key)}"
                            ax[index, n].set_title(myTitle, loc='center', wrap=True)
                    n += 1
            plt.legend()
            if label is None:
                fig_3.suptitle(f"Nro. {n_clusters} Clusters with {self.type_dr} dimentional reduction ")
            else:
                fig_3.suptitle(f"Nro. {n_clusters} Clusters with {self.type_dr} dimentional reduction - Label: {label}")
        plt.show()


class _choice_clu_model:
    def __init__(
            self,
            parameters
    ):
        self.type_dr = parameters['type_dr']
        self.model = parameters['model']
        self.metric = parameters['metric']
        self.n_jobs = parameters['n_jobs']
        self.max_iter = parameters['max_iter']
        self.seed = parameters['seed']
        self.n_clusters = parameters['n_clusters']
        self.points_2d = parameters['points_2d']
        self.view_clu = parameters['view_clu']

    def check_model(self, data, ts_scaler, dict_scaler, n_clusters: int = None, inv_scaler: bool = None):
        if n_clusters is not None:
            self.n_clusters = n_clusters
        train_model = self._train_model(data, ts_scaler, dict_scaler)
        dict_df_clu = {}
        for i in train_model['dataset']['cluster'].unique():
            df_aux = train_model['dataset'][train_model['dataset']['cluster'] == i]
            df_aux.drop(columns=['cluster'], inplace=True)
            dict_df_clu[i] = df_aux
        train_model['clusters'] = dict_df_clu
        if inv_scaler:
            train_model['dataset'] = pd.DataFrame(
                self._inverse_transform(train_model['dataset'].values.T, train_model['dict_scaler']).T,
                columns=train_model['dict_scaler']['dataset'].columns,
                index=train_model['dict_scaler']['dataset'].index
            )
        if self.view_clu:
            fx_clu_plots.view_all_clusters(train_model)
        return train_model

    def _train_model(self, data, ts_scaler, dict_scaler):
        clu_model = self._select_model(data)
        cluster_labels = clu_model.fit_predict(data)
        ts_clustered = [ts_scaler[(cluster_labels == label), :] for label in np.unique(cluster_labels)]
        train_model = {
            'clu_model': clu_model,
            'ts_clustered': ts_clustered,
            'cluster_labels': cluster_labels,
            'data': data,
            'ts_scaler': ts_scaler,
            'dict_scaler': dict_scaler
        }
        train_model['dataset'] = train_model['dict_scaler']['dataset']
        train_model['dataset']['cluster'] = train_model['cluster_labels']
        train_model['dataset']['user'] = train_model['dict_scaler']['user']
        return train_model

    def _inverse_transform(
            self,
            yhat,
            dict_scaler,
    ):
        for index, i in enumerate(dict_scaler['dataset'].columns[:-2]):
            scaler = dict_scaler['scaler']['scaler_' + i]
            yhat[index, :] = scaler.inverse_transform(yhat[index, :].reshape(-1, 1)).reshape(yhat.shape[1], )
        return yhat

    def _select_model(self, data):
        return TimeSeriesKMeans(
            n_clusters=self.n_clusters,
            metric=self.metric,
            n_jobs=self.n_jobs,
            max_iter=self.max_iter,
            random_state=self.seed
        )


class barycenter:

    def __init__(self, ts_clustered, max_iter, tol, verbose, gamma):
        self.ts_clustered = ts_clustered
        self.max_iter = max_iter
        self.tol = tol
        self.verbose = verbose
        self.gamma = gamma

    def centroid(self, clu_model, ts_scaler, data):
        # Cluster Centroid
        closest_clusters_index = [
            np.argmin(
                [np.linalg.norm(cluster_center - point, ord=2) for point in data]
            ) for cluster_center in clu_model.cluster_centers_
        ]
        closest_ts = ts_scaler[closest_clusters_index, :]
        # Centroids
        all_centroids = [np.array(x).reshape(np.array(x).shape[0], 1) for x in closest_ts.tolist()]
        return all_centroids

    def mean(self):
        # Means to cluster's
        all_meas = [
            np.mean(np.array(x), axis=0).reshape(np.mean(np.array(x), axis=0).shape[0], 1) for x in self.ts_clustered
        ]
        return all_meas

    def euclidean(self):
        euclidean = [euclidean_barycenter(cluster_series) for cluster_series in self.ts_clustered]
        return euclidean


class fx_clu_plots:

    def __init__(self):
        return

    @staticmethod
    def _clu_barplot(dict_bar, label):
        df_count_clu = dict_bar['dataset'].groupby(['cluster', 'user', ]).size().unstack()
        df_count_clu = df_count_clu / df_count_clu.sum(axis=0)
        # plot df_count_clu T in barprlot stacked = True
        # df_count_clu.T.plot.bar(stacked=True, figsize=(10, 5))
        ax = df_count_clu.T.plot.bar(stacked=True, figsize=(10, 5))
        if label is None:
            ax.set_title('Cluster distribution')
        else:
            ax.set_title(f'Cluster distribution - Label: {label}')
        ax.legend(bbox_to_anchor=(1.0, 1.0))
        ax.plot()
        plt.show()

    @staticmethod
    def plt_pct_clu(
            labels_clu,
            label
    ):
        labels = np.unique(labels_clu, return_counts=True)
        fig, ax = plt.subplots()
        ax.pie(labels[1], labels=labels[0], autopct='%1.1f%%', shadow=True, startangle=90)
        if label is not None:
            ax.set_title(f'Cluster distribution - Label: {label}')
        else:
            ax.set_title(f'Cluster distribution - Label: {label}')
        plt.show()

    @staticmethod
    def plot_multi(
            data: pd.DataFrame,
            x: Union[str, None] = None,
            y: Union[List[str], None] = None,
            spacing: float = 0.1,
            model: str = None,
            label_clu: str = None,
            **kwargs
    ) -> matplotlib.axes.Axes:
        """Plot multiple Y axes on the same chart with same x axis.

        Args:
            data: dataframe which contains x and y columns
            x: column to use as x axis. If None, use index.
            y: list of columns to use as Y axes. If None, all columns are used
                except x column.
            spacing: spacing between the plots
            **kwargs: keyword arguments to pass to data.plot()

        Returns:
            a matplotlib.axes.Axes object returned from data.plot()

        See Also:
            This code is mentioned in https://stackoverflow.com/q/11640243/2593810
            :param data:
            :param x:
            :param y:
            :param label_clu:
            :param model:
        """
        from pandas.plotting._matplotlib.style import get_standard_colors
        from matplotlib.lines import Line2D

        list_markers = list(Line2D.markers.keys())

        # Get default color style from pandas - can be changed to any other color list
        if y is None:
            y = data.columns
        # remove x_col from y_cols
        if x:
            y = [col for col in y if col != x]
        if len(y) == 0:
            return
        colors = get_standard_colors(num_colors=len(y))
        if "legend" not in kwargs:
            kwargs["legend"] = False  # prevent multiple legends
        # First axis
        aux = 0
        ax = data.plot(x=x, y=y[0], color=colors[0], marker=list_markers[aux], **kwargs)
        ax.set_ylabel(ylabel=y[0])
        lines, labels = ax.get_legend_handles_labels()
        aux += 0
        for i in range(1, len(y)):
            # Multiple y-axes
            ax_new = ax.twinx()
            ax_new.spines["right"].set_position(("axes", 1 + spacing * (i - 1)))
            data.plot(
                ax=ax_new, x=x, y=y[i], color=colors[i % len(colors)], marker=list_markers[aux], **kwargs
            )
            ax_new.set_ylabel(ylabel=y[i])
            # Proper legend position
            line, label = ax_new.get_legend_handles_labels()
            lines += line
            labels += label
            aux += 1
        ax.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True,
                  ncol=aux + 1)
        plt.tight_layout()
        if label_clu is not None:
            plt.title(f'Optimal number of clusters with {model}- Label: {label_clu}')
        else:
            plt.title(f'Optimal number of clusters with {model}')

        return ax

    @staticmethod
    def view_all_clusters(results_mdl, n_rows: int = None, n_cols: int = 2, legend: bool = False):
        if n_rows is None:
            n_rows = int(round(len(results_mdl['clusters'].keys()) / n_cols, 0))
        fig_1, axs = plt.subplots(nrows=n_rows, ncols=n_cols, sharex=True)
        row, col, clu = 0, 0, 0
        for key, value in results_mdl['clusters'].items():
            ax = value.loc[:, value.columns[:-1]].T.plot(ax=axs[row, col], sharex=True)
            if legend:
                ax.legend(loc=8, ncols=3, fontsize='xx-small', alignment='right')
            else:
                ax.legend().set_visible(False)
            ax.set_title(f'cluster {key}')
            col += 1
            clu += 1
            if n_cols == col:
                row += 1
                col = 0
        plt.show()

    @staticmethod
    def clu_model_view(
            model
    ):
        def _plot_cluster_ts(current_cluster):
            """
            Plots time series in a cluster

            current_cluster: np.array
                Cluster with time series
            Returns:
            -------
            None
            """
            fig, ax = plt.subplots(
                int(np.ceil(current_cluster.shape[0] / 5)),
                5,
                figsize=(45, 3 * int(np.ceil(current_cluster.shape[0] / 5))),
                sharex=True,
                sharey=True
            )
            fig.autofmt_xdate(rotation=45)
            ax = ax.reshape(-1)
            for index, series in enumerate(current_cluster):
                ax[index].plot(series)
                plt.xticks(rotation=45)

            plt.tight_layout()
            plt.show()

        # Objects distribution in the obtained clusters
        labels = [f'Cluster_{i}' for i in range(len(model['ts_clustered']))]
        samples_in_cluster = [val.shape[0] for val in model['ts_clustered']]
        plt.figure(figsize=(16, 5))
        plt.bar(labels, samples_in_cluster)
        # plt.pie(samples_in_cluster, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        for cluster in range(len(model['ts_clustered'])):
            print(f"==========Cluster number: {cluster}==========")
            _plot_cluster_ts(model['ts_clustered'][cluster])
        # plt.show()

    @staticmethod
    def all_barycenter(
            summary: bool = True,
            all_bar: bool = False,
            plt_n_cluster: int = 1,
            gamma: int = 1.0,
            dict_bar: dict = None,
            label: str = None
    ):
        if all_bar:
            # Plot barycenter of the cluster input for user and selected
            n_rows = len(dict_bar.keys()) - 2
            if n_rows == 1:
                for key, value in dict_bar.items():
                    if key == 'dataset' or key == 'clusters':
                        pass
                    else:
                        plt.plot(dict_bar['clusters'][plt_n_cluster], "k-", alpha=0.2)
                        plt.plot(dict_bar[key][plt_n_cluster], c='r')
                        plt.title(set_tittle_cluster(key), loc='left', y=0.85, x=0.02, fontsize='medium')
                        if label is None:
                            plt.suptitle(f'Cluster Series - Cluster No. {plt_n_cluster}')
                        else:
                            plt.suptitle(f'Cluster Series - Cluster No. {plt_n_cluster} - Label: {label}')
            else:
                fig_1, ax = plt.subplots(nrows=n_rows, ncols=1, sharex=True)
                n = 0
                for key, value in dict_bar.items():
                    if key == 'dataset' or key == 'clusters':
                        pass
                    else:
                        ax[n].plot(dict_bar['clusters'][plt_n_cluster], "k-", alpha=0.2)
                        ax[n].plot(dict_bar[key][plt_n_cluster], c='r')
                        ax[n].set_title(set_tittle_cluster(key), loc='left', y=0.85, x=0.02, fontsize='medium')
                        n += 1
                if label is None:
                    fig_1.suptitle(f'Cluster Series - Cluster No. {plt_n_cluster}')
                else:
                    fig_1.suptitle(f'Cluster Series - Cluster No. {plt_n_cluster} - Label: {label}')
                plt.show()

        if summary:
            fig, ax = plt.subplots(nrows=len(dict_bar['clusters']), ncols=1, sharex=True, layout='constrained')
            for i in range(len(dict_bar['clusters'])):
                ax[i].plot(dict_bar['clusters'][i], "k-", alpha=0.2)
                for key, value in dict_bar.items():
                    if (key == 'dataset') or (key == 'clusters'):
                        pass
                    else:
                        ax[i].plot(dict_bar[key][i], label=set_tittle_cluster(key))
                if label is None:
                    ax[i].set_title(f"Summary to Cluster Nro. {i}")
                else:
                    ax[i].set_title(f"Summary to Cluster Nro. {i} - Label: {label}")
            labels_handles = {
                label: handle for ax in fig.axes for handle, label in zip(*ax.get_legend_handles_labels())
            }
            lines = []
            labels = []
            for ax in fig.axes:
                Line, Label = ax.get_legend_handles_labels()
                # print(Label)
                lines.extend(Line)
                labels.extend(Label)

            lines = [i for n, i in enumerate(lines) if i not in lines[:n]]
            labels = [i for n, i in enumerate(labels) if i not in labels[:n]]

            # rotating x-axis labels of last sub-plot
            plt.xticks(rotation=45)

            fig.legend(lines, labels, loc='outside right')
            plt.show()

    @staticmethod
    def summation_MEAS_Barycenters(dict_dates, preview, seed):
        import random
        random.seed(seed)
        dates_aux = random.choices(list(dict_dates.keys()), k=preview)
        for d in dates_aux:
            plt.figure(figsize=(15, 5))
            for key, values in dict_dates[d].items():
                if key == 'PDC':
                    plt.plot(values, label=key, color='k', lw=3, marker='o')
                else:
                    plt.plot(values, label=key, ls='--')
            plt.title(d)
            plt.legend(loc="best")

            plt.show()

    @staticmethod
    def plt_global(dict_metrics, boxplot: bool = None, violinplot: bool = None):
        df_global = dict_metrics['global']
        if boxplot:
            # Boxplot
            if len(df_global.columns[1:]) == 1:
                sns.boxplot(data=df_global, x='model', y=df_global.columns[1:][0], fliersize=0)
                plt.title('Boxplot for clustering')
                plt.show()
            else:
                n = len(df_global.columns[1:])
                fig, axes = plt.subplots(n, 1, sharex=True)
                n = 1
                for k in df_global.columns[1:]:
                    sns.boxplot(ax=axes[n], data=df_global, x='model', y=k, fliersize=0)
                    n += 1
                fig.suptitle('Boxplot for clustering')
                plt.show()

        if violinplot:
            # Violinplot
            # Boxplot
            if len(df_global.columns[1:]) == 1:
                sns.violinplot(data=df_global, x='model', y=df_global.columns[1:][0], fliersize=0)
                plt.title('Violinplot for clustering')
                plt.show()
            else:
                n = len(df_global.columns[1:])
                fig, axes = plt.subplots(n, 1, sharex=True)
                n = 1
                for k in df_global.columns[1:]:
                    sns.violinplot(ax=axes[n], data=df_global, x='model', y=k, fliersize=0)
                    n += 1
                fig.suptitle('Violinplot for clustering')
                plt.show()

    @staticmethod
    def plt_partial(dict_metrics, boxplot: bool = None, violinplot: bool = None):
        df_partial = dict_metrics['partial']
        if boxplot:
            fig2, axes = plt.subplots(3, 1, figsize=(18, 10))
            fig2.suptitle('Boxplot for clustering')
            sns.boxplot(ax=axes[0], data=df_partial[df_partial.model == 'mean'], x='Nro', y='MAPE', fliersize=0)
            sns.lineplot(ax=axes[1], data=df_partial[df_partial.model == 'mean'], x='Nro', y='MAPE')
            sns.catplot(ax=axes[2], data=df_partial, x='Nro', y='MAPE', hue='model', kind="point")
            # sns.boxplot(ax=axes[2], data=df_metric_min, x='model', y='MAPE')
            sns.boxplot()
