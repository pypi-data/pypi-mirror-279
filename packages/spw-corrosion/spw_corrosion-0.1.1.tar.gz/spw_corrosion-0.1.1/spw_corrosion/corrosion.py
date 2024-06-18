import numpy as np
from scipy.stats import norm, truncnorm
from scipy.integrate import trapz
from dataclasses import dataclass, field
import xarray as xr
from typing import Union
import warnings

warnings.filterwarnings("ignore")


CORR_GRID = np.ndarray["n_corr_grid", float]
COND_PF_GRID = np.ndarray["n_pf_grid", float]
C50_GRID = np.ndarray["n_C50_grid", float]
PRIOR_PDF = np.ndarray["n_pf_grid", float]

PARAM = Union[np.ndarray[("n_C50_grid", "n_pf_times", 1), float],
              np.ndarray[("n_C50_grid", "n_obs_times", 1), float]]
CORR_PDF = Union[np.ndarray[("n_C50_grid", "n_pf_times", "n_corr_grid"), float],
                 np.ndarray[("n_C50_grid", "n_obs_times", "n_corr_grid"), float]]
PDF_DOT_PF = Union[np.ndarray[("n_C50_grid", "n_pf_times", "n_corr_grid"), float],
                   np.ndarray[("n_C50_grid", "n_obs_times", "n_corr_grid"), float]]
PARAM_TIME = Union[np.ndarray[("n_true_C50", "n_obs_times", 1), float],
                   np.ndarray[("n_true_C50", "n_pf_times", 1), float]]
PF_TIME = Union[np.ndarray["n_pf_times", int], np.ndarray["n_pf_times", float]]
OBS_TIME = Union[np.ndarray["n_obs_times", int], np.ndarray["n_obs_times", float]]
POST_PDF = np.ndarray[("n_corr_grid", "n_obs_timelines", "n_true_C50"), float]  # Type hints for xarray?
PF = np.ndarray[("n_true_C50", "n_pf_times"), float]
C50_TYPE = np.ndarray[(1, "n_true_C50"), float]
OBS = np.ndarray[("n_obs_times", "n_obs_timelines", "n_true_C50"), float]  # Type hints for xarray?


@dataclass
class Config:
    corrosion_grid: CORR_GRID
    cond_pf_grid: COND_PF_GRID
    n_C50_grid: int = 1_000
    C50_mu: float = 1.5
    C50_CoV: float = 0.5
    C50_scale: float = field(init=False)
    C50_lower: float = field(init=False)
    C50_upper: float = field(init=False)
    C50_prior_pdf: C50_GRID = field(init=False)
    C50_grid: C50_GRID = field(init=False)
    obs_error_std: float = 0.1
    corrosion_rate: float = 0.22
    start_thickness: Union[int, float] = 10.0  # BZ17 starting thickness

    def __post_init__(self):
        self.C50_grid = np.linspace(self.start_thickness / self.n_C50_grid, self.start_thickness, self.n_C50_grid)
        self.C50_scale = self.C50_mu * self.C50_CoV
        self.C50_lower = (0 - self.C50_mu) / self.C50_scale
        self.C50_upper = (self.start_thickness - self.C50_mu) / self.C50_scale
        C50_prior_model = truncnorm(loc=self.C50_mu, scale=self.C50_scale, a=self.C50_lower, b=self.C50_upper)
        self.C50_prior_pdf = C50_prior_model.pdf(self.C50_grid)


class CorrosionModel:
    """
    According to EC:
    C_t = C50 * (1 + 0.22 * (t - 50))    {50 <= t <= 100}                          {1}
    C50 ~ TruncN(1.5[mm], (1.5*0.5)**2 [mm**2], a=0, b=start_thickness)            {2}
    {1} + {2} -->
    mu = 1.5 * (1 + 0.22 / 1.5 * (t - 50))
    std = (1.5 * (1 + 0.22 / 1.5 * (t - 50))*0.5)**2 [mm**2]
    C_t ~ TruncN(mu, std ** 2, , a=0, b=start_thickness)  {3}

    "param" is the mean of corrosion distribution (as a function of time).
    """

    def __init__(self, config: Config, to_xarray: bool = False) -> None:
        self.config = config
        self.to_xarray = to_xarray

    def corrosion_model_params(self, param):
        scale = param * self.config.C50_CoV
        lower_trunc = (0 - param) / scale
        upper_trunc = (self.config.start_thickness - param) / scale
        return scale, lower_trunc, upper_trunc

    def get_pdf(self, param: PARAM) -> CORR_PDF:
        """
        PDF according to EC model.
        :param param: Mean of corrosion distribution (as a function of time)
        :return:
        """
        # return stats.beta(a=param, b=param+1).pdf(self.config.corrosion_grid)

        scale, lower_trunc, upper_trunc = self.corrosion_model_params(param)
        corrosion_pdf = truncnorm(loc=param, scale=scale, a=lower_trunc, b=upper_trunc).pdf(self.config.corrosion_grid)
        return corrosion_pdf

    def _product(self, pdf: CORR_PDF) -> PDF_DOT_PF:
        return np.multiply(pdf, self.config.cond_pf_grid)

    def pf_cond_C50(self, times: PF_TIME) -> np.ndarray["n_C50_grid", float]:

        param = self._timemodel(times, self.config.C50_grid)
        corrosion_pdf = self.get_pdf(param)
        product = self._product(corrosion_pdf)
        pf = trapz(product, self.config.corrosion_grid, axis=-1)

        """ To xarray """
        if self.to_xarray:
            coords = dict(C50_grid=self.config.C50_grid, times=times)
            pf = xr.DataArray(data=pf, dims=['C50_grid', 'times'], coords=coords)

        return pf

    def pf(self, pdf: POST_PDF, times: PF_TIME) -> PF:

        pf_cond_C50 = self.pf_cond_C50(times)

        """ To xarray """
        if self.to_xarray:
            pf_cond_C50 = pf_cond_C50.to_numpy()
            C50 = pdf.C50
            pdf = pdf.to_numpy()

        pf = np.multiply(pf_cond_C50[:, np.newaxis, np.newaxis, :], pdf[..., np.newaxis])
        pf = trapz(pf, self.config.C50_grid, axis=0)

        """To xarray"""
        if self.to_xarray:
            coords = dict(mc=np.arange(1, pf.shape[0] + 1), C50=C50, times=times)
            pf = xr.DataArray(data=pf, dims=['mc', 'C50', 'times'], coords=coords)

        """ Average over of #n_timelines Monte-Carlo draws of timelines of observations. """
        pf = pf.mean(axis=0)

        return pf

    def _timemodel(self, times: Union[PF_TIME, OBS_TIME], C50: C50_TYPE) -> PARAM_TIME:
        C50 = C50[..., np.newaxis]
        param = C50 * (1 + self.config.corrosion_rate / self.config.C50_mu * (times - 50))
        return param[..., np.newaxis]

    def generate_observations(self, rng: np.random.Generator, obs_times: OBS_TIME, C50: C50_TYPE,
                              n_timelines: int = 1) -> OBS:

        # param = self._timemodel(obs_times, C50)
        # param = np.transpose(param, (1, 2, 0))

        """ n_timelines controls the number of Monte-Carlo samples for generating timelines of observations """

        """ rng lacks truncnorm -> Improvise """
        # cdf_samples = rng.uniform(0, 1, size=(1, n_timelines, C50.size))
        # param = truncnorm(loc=self.config.C50_mu, scale=self.config.C50_scale,
        #                   a=self.config.C50_lower, b=self.config.C50_upper).ppf(cdf_samples)
        # scale, lower_trunc, upper_trunc = self.corrosion_model_params(param)

        # cdf_samples = np.repeat(cdf_samples, obs_times.size, axis=0)
        # obs = truncnorm(loc=param, scale=scale, a=lower_trunc, b=upper_trunc).ppf(cdf_samples)

        # TODO: To add randomness in the problem, the following statement is loosened
        """
        Corrosion observations over a timeline are fully correlated -> there is only one truly random variable for
        for generating observations: C50
        """

        n_times = obs_times.size
        obs_times = obs_times[:, np.newaxis, np.newaxis]
        obs_mean = C50[np.newaxis, np.newaxis, :] *\
                   (1 + self.config.corrosion_rate / self.config.C50_mu * (obs_times - 50))
        obs_error = rng.normal(loc=0, scale=1, size=(n_times, n_timelines, C50.size))
        obs_error = np.cumsum(obs_error, axis=0)
        obs = obs_mean + obs_error * self.config.obs_error_std

        """ To xarray """
        if self.to_xarray:
            coords = dict(obs_times=obs_times, mc=np.arange(1, obs.shape[1] + 1), C50=C50)
            obs = xr.DataArray(data=obs, dims=['obs_times', 'mc', 'C50'], coords=coords)

        return obs

    def bayesian_updating(self, obs: OBS, obs_times: OBS_TIME) -> POST_PDF:

        log_prior = np.log(self.config.C50_prior_pdf)
        # param = self._timemodel(obs_times, self.config.C50_grid)
        # param = param[..., np.newaxis]
        # scale, lower_trunc, upper_trunc = self.corrosion_model_params(param)

        # TODO: To add randomness in the problem, the following statement is loosened
        """
        Corrosion observations over a timeline are fully correlated -> there is only one truly random variable for
        for generating observations: C50 -> There is one truly random observation
        """

        C50 = self.config.C50_grid
        C50 = C50[:, np.newaxis, np.newaxis, np.newaxis]

        obs_times = obs_times[np.newaxis, :, np.newaxis, np.newaxis]
        C_mu = C50 * (1 + self.config.corrosion_rate / self.config.C50_mu * (obs_times - 50))
        C_deviations = (obs - C_mu) / self.config.obs_error_std
        C_deviations = C_deviations.squeeze()
        C_deviations = np.concatenate((C_deviations[:, 0, ...][:, np.newaxis, ...], np.diff(C_deviations, axis=1)), axis=1)
        A = C_deviations[0, ..., 0]

        loglikes = norm(loc=0, scale=1).logpdf(C_deviations)
        loglike = loglikes.sum(axis=1)

        log_post = log_prior[..., np.newaxis, np.newaxis] + loglike
        post = np.exp(log_post)
        post /= trapz(post, self.config.C50_grid, axis=0)[np.newaxis, ...]

        """To xarray"""
        if self.to_xarray:
            coords = dict(
                C50_grid=self.config.C50_grid,
                mc=np.arange(1, obs.shape[1] + 1),
                C50=np.arange(1, obs.shape[2] + 1)
            )
            post = xr.DataArray(data=post, dims=['C50_grid', 'mc', 'C50'], coords=coords)

        return post


if __name__ == "__main__":

    pass

