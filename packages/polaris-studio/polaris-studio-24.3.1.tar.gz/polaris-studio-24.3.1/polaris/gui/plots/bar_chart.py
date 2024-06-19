import pandas as pd


def bar_chart(iterations, ax, field_name, table_name):
    dt = []
    for name, df in iterations.items():
        summ = pd.DataFrame(df[field_name].value_counts()).rename(columns={"count": name})
        dt.append(summ)

    print_df = pd.concat(dt, axis=1).fillna(0).sort_index()
    if print_df.shape[0] == 0:
        print("No data found")
        return

    print_df.reset_index().plot(x=field_name, y=list(iterations.keys()), kind="bar", rot=0, ax=ax)
    ax.set_ylabel(f"{table_name} occurrences")
    ax.set_xlabel(field_name)
    ax.set_title(f"Frequency for {field_name} values on {table_name} across iterations")
    ax.legend()
