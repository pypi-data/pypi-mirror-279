import matplotlib.pyplot as plt
import seaborn as sns

def scatter_plot(df, x_col, y_col, title="Scatter Plot"):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x=x_col, y=y_col)
    plt.title(title)
    plt.show()
