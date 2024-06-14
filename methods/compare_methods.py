import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib as mpl
from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
from tigramite.independence_tests.parcorr import ParCorr
import pandas as pd
import statsmodels.formula.api as smf

def compare_methods(data: pd.DataFrame, tau_min: int, tau_max: int, alpha_level: float) -> None:
    """
    Compare different causal inference methods and plot the results.

    Parameters:
    data (pd.DataFrame): Input data with time series.
    tau_min (int): Minimum time lag.
    tau_max (int): Maximum time lag.
    alpha_level (float): Significance level for conditional independence tests.
    """
    labels: pd.Index = data.columns
    all_data_array: np.ndarray = np.array(data)
    var_names: pd.Index = labels
    dataframe: pp.DataFrame = pp.DataFrame(all_data_array, datatime=np.arange(len(all_data_array)), var_names=var_names)

    fig, ax = plt.subplots(1, 3, figsize=(35, 12), rasterized=True)
    fig.subplots_adjust(wspace=0.01, hspace=0)
    plt.margins(x=0, y=0)

    lvTmp: np.ndarray = np.linspace(0.1, 0.8, 256 - 1)
    cmTmp: np.ndarray = mpl.cm.OrRd(lvTmp)
    newCmap: mcol.ListedColormap = mcol.ListedColormap(cmTmp)

    ax = ax.flatten()
    N: int = len(var_names)

    links: dict = {j: {(i, -tau): 'o?o' for i in range(N) for tau in range(1, tau_max + 1) if (i, -tau) != (j, 0)} for j in range(N)}
    links[1] = {(i, -tau): '-?>' for i in range(N) for tau in range(1, tau_max + 1)
                if ((i, -tau) not in [(1, 0), (1, 2), (1, 3), (1, 4), (1, 5)] and i not in [0, 1, 2, 3, 4, 5])}

    pcmci_parcorr: PCMCI = PCMCI(dataframe=dataframe, cond_ind_test=ParCorr(verbosity=0), verbosity=0)

    # Partial Correlation
    ax[0].set_title('Partial Correlation', fontsize=50)
    ax[0].set_facecolor(color='w')
    ax[0].set_facecolor(color=(0.94117647, 0.97254902, 1.))
    ax[0].patch.set_alpha(0.2)

    results: dict = pcmci_parcorr.get_lagged_dependencies(link_assumptions=links, tau_min=tau_min, tau_max=tau_max, val_only=False, alpha_level=0.05, fdr_method='none')
    tp.plot_graph(
        val_matrix=results['val_matrix'],
        graph=results['graph'],
        var_names=var_names,
        link_colorbar_label='cross-MCI',
        node_colorbar_label='auto-MCI',
        label_fontsize=30,
        fig_ax=(fig, ax[0]),
        figsize=(10, 4), node_label_size=30, node_size=0.4, link_label_fontsize=15, arrow_linewidth=10, cmap_edges='RdBu_r', cmap_nodes=newCmap,
        vmin_nodes=0, vmax_nodes=1, node_ticks=0.5, edge_ticks=0.5, show_colorbar=False, node_aspect=None, curved_radius=0.2,
    )
    del results['conf_matrix']

    # FullCI: Granger Causality
    ax[1].set_title('FullCI', fontsize=50)
    ax[1].set_facecolor(color='w')
    ax[1].set_facecolor(color=(0.94117647, 0.97254902, 1.))
    ax[1].patch.set_alpha(0.2)

    results = pcmci_parcorr.run_fullci(link_assumptions=links, tau_min=tau_min, tau_max=tau_max, val_only=False, alpha_level=0.05, fdr_method='none')
    tp.plot_graph(
        val_matrix=results['val_matrix'],
        graph=results['graph'],
        var_names=var_names,
        link_colorbar_label='cross-MCI',
        node_colorbar_label='auto-MCI',
        label_fontsize=30,
        fig_ax=(fig, ax[1]),
        figsize=(10, 4), node_label_size=30, node_size=0.4, link_label_fontsize=15, arrow_linewidth=10, cmap_edges='RdBu_r', cmap_nodes=newCmap,
        vmin_nodes=0, vmax_nodes=1, node_ticks=0.5, edge_ticks=0.5, show_colorbar=False, node_aspect=None, curved_radius=0.2,
    )
    del results['conf_matrix']

    # PCMCI
    ax[2].set_title('PCMCI', fontsize=50)
    ax[2].set_facecolor(color='w')
    ax[2].set_facecolor(color=(0.94117647, 0.97254902, 1.))
    ax[2].patch.set_alpha(0.2)

    results = pcmci_parcorr.run_pcmci(tau_max=tau_max, pc_alpha=0.05, alpha_level=alpha_level, link_assumptions=links)
    q_matrix: np.ndarray = pcmci_parcorr.get_corrected_pvalues(p_matrix=results['p_matrix'], tau_max=tau_max, fdr_method=None, exclude_contemporaneous=False)
    graph: dict = pcmci_parcorr.get_graph_from_pmatrix(p_matrix=q_matrix, alpha_level=alpha_level, tau_min=1, tau_max=tau_max)
    results['graph'] = graph

    tp.plot_graph(
        val_matrix=results['val_matrix'],
        graph=results['graph'],
        var_names=var_names,
        link_colorbar_label='cross-MCI',
        node_colorbar_label='auto-MCI',
        label_fontsize=30,
        fig_ax=(fig, ax[2]),
        figsize=(10, 4), node_label_size=30, node_size=0.4, link_label_fontsize=15, arrow_linewidth=10, cmap_edges='RdBu_r', cmap_nodes=newCmap,
        vmin_nodes=0, vmax_nodes=1, node_ticks=0.5, edge_ticks=0.5, show_colorbar=False, node_aspect=None, curved_radius=0.2,
    )
    del results['conf_matrix']

    plt.show()



def linear_regression_coefficients(DATA_graph: pd.DataFrame, max_lag: int = 10) -> pd.DataFrame:
    """
    Perform linear regression on the given data with specified maximum lag.

    Parameters:
    DATA_graph (pd.DataFrame): The input data frame containing the time series data.
    max_lag (int): The maximum lag to be considered for the regression. Default is 10.

    Returns:
    pd.DataFrame: A data frame containing the coefficients, p-values, and R-squared values of the regression model.
    """
    # Replace spaces in column names with underscores
    DATA_graph.columns = DATA_graph.columns.str.replace(' ', '_')

    # Normalize the data
    data_regression: pd.DataFrame = (DATA_graph - DATA_graph.min()) / (DATA_graph.max() - DATA_graph.min())

    # Create lagged columns
    for column in data_regression.columns[1:]:
        for lag in range(1, max_lag + 1):
            data_regression[f'{column}_lag{lag}'] = data_regression[column].shift(lag)

    # Drop rows with missing values
    data_regression = data_regression.dropna()

    # Define the formula for the regression model
    formula: str = 'IDP_Drought ~ ' + ' + '.join([f'{column}' for column in data_regression.columns[6:]])

    # Fit the regression model
    model = smf.ols(formula, data=data_regression).fit()

    # Get the R-squared value
    R2: float = model.rsquared

    # Create a data frame with the results
    results: pd.DataFrame = pd.DataFrame({'coefficients': model.params, 'pvalues': model.pvalues, 
                                          'R-squared': [R2]*len(model.params)})

    # Return the results with p-values less than 0.05
    return results[results['pvalues'] < 0.05]
