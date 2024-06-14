import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib as mpl
from tigramite import data_processing as pp
from tigramite import plotting as tp
from tigramite.pcmci import PCMCI
import pandas as pd


def pcmci_graph_tau_bootstrap(DATA: pd.DataFrame, cond_ind_test: str, tau_min: int, tau_list: list, pc_alpha: float, alpha_level: float, mask_threshold: float, boot_samples: int) -> None:
    """
    Perform PCMCI graph bootstrap analysis for varying tau_max values.

    Parameters:
    DATA (pd.DataFrame): Input data with time series.
    cond_ind_test (str): Conditional independence test method.
    tau_min (int): Minimum time lag.
    tau_list (list): List of maximum time lags to iterate over.
    pc_alpha (float): Significance level for PC algorithm.
    alpha_level (float): Significance level for conditional independence tests.
    mask_threshold (float): Threshold for masking data.
    boot_samples (int): Number of bootstrap samples.
    """
    
    i: int = 0
   
    fig, ax = plt.subplots(2, 3, figsize=(60, 30), facecolor='w')
    ax = ax.flatten()

    for tau_max in tau_list:

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
        link_assumptions: dict = {j: {(i, -tau): 'o?o' for i in range(N) for tau in range(1, tau_max + 1) if (i, -tau) != (j, 0)} 
                                  for j in range(N)}

        link_assumptions[1] = {(i, -tau): '-?>' for i in range(N) for tau in range(1, tau_max + 1)
                               if ((i, -tau) not in [(1, 0), (1, 2), (1, 3), (1, 4), (1, 5)] and i not in [0, 1, 2, 3, 4, 5])} 
                                
        lvTmp: np.ndarray = np.linspace(0.1, 0.8, (256) - 1)
        cmTmp: np.ndarray = mpl.cm.OrRd(lvTmp)
        newCmap: mcol.ListedColormap = mcol.ListedColormap(cmTmp)

        pcmci: PCMCI = PCMCI(dataframe=dataframe, cond_ind_test=cond_ind_test, verbosity=0) 
        boot_blocklength: int = 1
        # Call bootstrap for the chosen method (here 'run_pcmciplus') and pass method arguments  
        results: dict = pcmci.run_bootstrap_of(
            method='run_pcmci', 
            method_args={'tau_min': tau_min, 'tau_max': tau_max, 'pc_alpha': pc_alpha, 'alpha_level': alpha_level, 'link_assumptions': link_assumptions}, 
            boot_samples=boot_samples,
            boot_blocklength=boot_blocklength,
            seed=123
        )
        
        # Output graph, link frequencies (confidence measure), and mean test statistic values (val_mat)
        boot_linkfreq: np.ndarray = results['summary_results']['link_frequency']
        boot_graph: np.ndarray = results['summary_results']['most_frequent_links']
        val_mat: np.ndarray = results['summary_results']['val_matrix_mean']

        # Plot graph
        axs = ax[i]
        
        i += 1
        
        axs.set_title('tau_max = ' + str(tau_max), fontsize=50)
        axs.set_facecolor(color='w')
        axs.set_facecolor(color=(0.94117647, 0.97254902, 1.))
        axs.patch.set_alpha(0.2)

        # Plot causal graph
        tp.plot_graph(
            val_matrix=val_mat,
            graph=boot_graph,
            var_names=var_names,
            link_width=boot_linkfreq,
            link_colorbar_label='cross-MCI',
            node_colorbar_label='auto-MCI',
            label_fontsize=30,
            fig_ax=(fig, axs),
            figsize=(10, 4), node_label_size=50, node_size=0.55, link_label_fontsize=40, arrow_linewidth=15, cmap_edges='RdBu_r', cmap_nodes=newCmap, 
            vmin_nodes=0, vmax_nodes=1, node_ticks=0.5, edge_ticks=0.5, show_colorbar=False, node_aspect=None, curved_radius=0.2
        )
        plt.tight_layout()

    plt.show()