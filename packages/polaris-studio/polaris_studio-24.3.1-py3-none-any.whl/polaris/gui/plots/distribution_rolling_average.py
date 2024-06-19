def start_distribution_chart(iterations, ax, table_name, window=300):
    time_field = "start_time" if table_name.lower() == "activity" else "start"
    for name, df in iterations.items():
        df = df.assign(stime=df[time_field].astype(int))
        df = df.groupby(["stime"]).size()
        df = df.rolling(window=window, center=True).mean().fillna(0)
        df1 = df.to_numpy()
        x = df.index.to_numpy()
        ax.plot(x, df1, label=name)
    ax.legend()
