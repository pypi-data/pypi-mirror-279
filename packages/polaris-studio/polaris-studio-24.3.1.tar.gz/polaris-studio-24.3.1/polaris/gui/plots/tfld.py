import numpy as np


def tfld(iterations, ax, table_name):
    time_field = "duration" if table_name.lower() == "activity" else "travel_distance"

    for name, df in iterations.items():
        dfa = df[df[time_field] > 0]

        # For large models, using 200 to 400 bins yields much better curves
        y, x = np.histogram(dfa[time_field].values / 1000, bins=120)
        ax.plot(x[1:], y, label=name)

    ax.set_ylabel("Frequency")
    ax.set_xlabel(time_field)
    ax.set_title(f"Trip Length Frequency Distribution: {table_name}")

    ax.legend()
