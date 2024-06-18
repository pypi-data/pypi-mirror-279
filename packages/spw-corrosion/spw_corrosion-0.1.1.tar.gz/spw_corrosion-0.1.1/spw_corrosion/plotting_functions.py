import numpy as np
from scipy.stats import norm
from typing import Optional
from spw_corrosion.corrosion import CorrosionModel
import matplotlib.pyplot as plt


def plot_posterior(model: CorrosionModel, post_pdf: np.ndarray, true_rate: np.ndarray,
                   fig_savefile: Optional[str] = None) -> None:

    colors = plt.cm.get_cmap('Spectral', true_rate.size)

    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    ax.plot(model.config.C50_grid, model.config.C50_prior_pdf, c='b')
    if true_rate.size > 1:
        for i, rate in enumerate(true_rate):
            for j in range(post_pdf.shape[-2]):
                post = post_pdf[:, j, i]
                ax2.plot(model.config.C50_grid, post, c=colors(i))
            ax.axvline(rate, c=colors(i), linestyle='--')
    else:
        for i in range(post_pdf.shape[-1]):
            for j in range(post_pdf.shape[-2]):
                post = post_pdf[:, j, i]
                ax2.plot(model.config.C50_grid, post, c=colors(i))
        ax.axvline(true_rate, c=colors(0), linestyle='--')
    ax.set_xlabel('Corrosion rate [??/yr]', fontsize=12)
    ax.set_ylabel('Prior density [-]', fontsize=12)
    ax2.set_ylabel('Posterior density [-]', fontsize=12)

    if fig_savefile is not None:
        plt.close()
        fig.savefig(fig_savefile)


def plot_pf_timeline(pf_timelines: np.ndarray, times: np.ndarray, true_rate: Optional[np.ndarray] = None,
                     fig_savefile: Optional[str] = None) -> None:

    colors = plt.cm.get_cmap('Spectral', pf_timelines.shape[0])
    add_label = true_rate is not None

    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    for i, pf in enumerate(pf_timelines):
        if add_label:
            ax.plot(times, pf, c=colors(i), label=true_rate[i])
        else:
            ax.plot(times, pf, c=colors(i))
    ax.set_xlabel('Time [yr]', fontsize=12)
    ax.set_ylabel('Log(${P}_{f}$) [-]', fontsize=12)
    ax.set_yscale('log', base=10)
    if add_label:
        ax.legend(title='True rate [??/yr]:', fontsize=10)

    if fig_savefile is not None:
        plt.close()
        fig.savefig(fig_savefile)


def plot_beta_timeline(pf_timelines: np.ndarray, times: np.ndarray, true_rate: Optional[np.ndarray] = None,
                     beta_req: Optional[float] = None, fig_savefile: Optional[str] = None) -> None:

    colors = plt.cm.get_cmap('Spectral', pf_timelines.shape[0])
    add_label = true_rate is not None

    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111)
    for i, pf in enumerate(pf_timelines):
        beta = -norm.ppf(pf, loc=0, scale=1)
        if add_label:
            ax.plot(times, beta, c=colors(i), label=true_rate[i])
        else:
            ax.plot(times, beta, c=colors(i))
    if beta_req is not None:
        ax.axhline(beta_req, linestyle='--', c='r', label='Reliability index\n requirement')
    ax.set_xlabel('Time [yr]', fontsize=12)
    ax.set_ylabel('Reliability index [-]', fontsize=12)
    # ax.set_yscale('log', base=10)
    if add_label:
        ax.legend(title='True rate [??/yr]:', fontsize=10)

    if fig_savefile is not None:
        plt.close()
        fig.savefig(fig_savefile)

