import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib as mpl
from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
import pandas as pd

def pcmci_graph_bootstrap(DATA: pd.DataFrame, cond_ind_test: str, tau_min: int, tau_max: int, alpha_level: float, pc_alpha: float, mask_threshold: float, boot_samples: int) -> dict:
    """
    Perform PCMCI graph bootstrap analysis.

    Parameters:
    DATA (pd.DataFrame): Input data with time series.
    cond_ind_test (str): Conditional independence test method.
    tau_min (int): Minimum time lag.
    tau_max (int): Maximum time lag.
    alpha_level (float): Significance level for conditional independence tests.
    pc_alpha (float): Significance level for PC algorithm.
    mask_threshold (float): Threshold for masking data.
    boot_samples (int): Number of bootstrap samples.

    Returns:
    dict: Results of the bootstrap analysis including link frequencies, most frequent links, and mean test statistic values.
    """
    
    labels: list = list(DATA.columns)
    labels = [label.split(' w')[0] for label in labels]
    var_names: list = labels
    all_data_array: np.ndarray = np.array(DATA, dtype=float)
    data_mask: np.ndarray = np.zeros(all_data_array.shape)
    T: int = all_data_array.shape[0]

    for t in range(1, T):
        if all_data_array[t, 0] < mask_threshold: 
            data_mask[t, 0] = True

    T, N = all_data_array.shape

    datatime: np.ndarray = np.arange(T)
    dataframe: pp.DataFrame = pp.DataFrame(all_data_array, datatime=np.arange(len(all_data_array)), var_names=var_names, mask=data_mask)

    N: int = len(var_names)

    # Nothing can cause precipitation: masking precipitation links
    link_assumptions: dict = {j: {(i, -tau): 'o?o' for i in range(N) for tau in range(tau_min, tau_max + 1) if (i, -tau) != (j, 0)} 
                              for j in range(N)}

    link_assumptions[1] = {(i, -tau): '-?>' for i in range(N) for tau in range(tau_min, tau_max + 1)
                           if ((i, -tau) not in [(1, 0), (1, 2), (1, 3), (1, 4), (1, 5)] and i not in [0, 1, 2, 3, 4, 5])} 
                            
    lvTmp: np.ndarray = np.linspace(0.1, 0.8, (256) - 1)
    cmTmp: np.ndarray = mpl.cm.OrRd(lvTmp)
    newCmap: mcol.ListedColormap = mcol.ListedColormap(cmTmp)

    pcmci: PCMCI = PCMCI(dataframe=dataframe, cond_ind_test=cond_ind_test, verbosity=0) 

    boot_blocklength: int = 1
    # Call bootstrap for the chosen method (here 'run_pcmciplus') and pass method arguments  
    results: dict = pcmci.run_bootstrap_of(
        method='run_pcmci', 
        method_args={'tau_min': tau_min, 'tau_max': tau_max, 'alpha_level': alpha_level, 'pc_alpha': pc_alpha, 'link_assumptions': link_assumptions}, 
        boot_samples=boot_samples,
        boot_blocklength=boot_blocklength,
        seed=123
    )

    # Output graph, link frequencies (confidence measure), and mean test statistic values (val_mat)
    boot_linkfreq: np.ndarray = results['summary_results']['link_frequency']
    boot_graph: np.ndarray = results['summary_results']['most_frequent_links']
    val_mat: np.ndarray = results['summary_results']['val_matrix_mean']

    # Plot causal graph
    tp.plot_graph(
        val_matrix=val_mat,
        graph=boot_graph,
        var_names=var_names,
        link_width=boot_linkfreq,
        link_colorbar_label='cross-MCI',
        node_colorbar_label='auto-MCI',
        label_fontsize=20,
        figsize=(18, 12), node_label_size=30, node_size=0.5, link_label_fontsize=20, arrow_linewidth=10, cmap_edges='RdBu_r', cmap_nodes=newCmap, 
        vmin_nodes=0, vmax_nodes=1, node_ticks=0.5, edge_ticks=0.5, show_colorbar=True, node_aspect=None, curved_radius=0.2
    )

    plt.show()

    return results