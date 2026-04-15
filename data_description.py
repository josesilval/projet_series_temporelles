#### imports ####
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from sklearn.neighbors import KernelDensity

## tsa imports ##
from statsmodels.tsa.stattools import pacf, acf, adfuller
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf

#### import data ####
data = pd.read_csv('var_ipc.csv')
n, _ = data.shape

# parce date
data['date'] = pd.to_datetime(data['date'])

#### plot ####
data.plot(x = 'date', y = 'var_ipc', title = 'Monthly IPC Variation', ylabel='Variation [%]')
plt.savefig('figures/line_plot.png')
plt.show()

#### histogram ####
plt.hist(data['var_ipc'], bins = 20, edgecolor = 'black', density=True)
plt.title('Monthly IPC Variation Histogram');
plt.savefig('figures/histogram.png')
plt.show()

#### measures ####
description = data['var_ipc'].describe()

median = np.median(data['var_ipc'])
skewness = stats.skew(data['var_ipc'])
kurtosis = stats.kurtosis(data['var_ipc'])

description['median'] = median
description['skewness'] = skewness
description['kurtosis'] = kurtosis

# save measures
description.to_csv('description.csv', index=True, header=False)

#### kernel density ####
kde = KernelDensity(kernel='gaussian').fit(data['var_ipc'].values.reshape(-1,1))
sample = kde.sample(1000)
pd.DataFrame(sample, columns=['Estimated distribution']).plot.density(title = 'Kernel Density Distribution')
plt.savefig('figures/kernel_density.png')
plt.show()

#### pacf  and acf####
PACF = pacf(data['var_ipc'])
ACF = acf(data['var_ipc'])

autocorrs = pd.DataFrame(
    np.c_[PACF, ACF],
    columns = ['PACF', 'ACF']
)
autocorrs.reset_index(inplace=True)
autocorrs.rename(columns={'index':'lag'}, inplace=True)
autocorrs.to_csv('autocorrs.csv', index=False)

## plot pacf
fig = plot_pacf(data['var_ipc'].values, lags = int(n/4))
fig.savefig('figures/pacf.png')
plt.show()

## plot acf
fig = plot_acf(data['var_ipc'].values, lags = int(n/4))
fig.savefig('figures/acf.png')
plt.show()