import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

rtt_min_df = pd.read_csv('graphs/rtt_min.csv', header = 0,index_col=0)
ax = sns.heatmap(rtt_min_df, annot=True, fmt=".0f")
plt.savefig('graphs/rtt_min_heatmap.eps')
plt.show()
