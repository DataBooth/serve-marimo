import marimo

__generated_with = "0.13.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return mo


@app.cell
def _(mo):
    import matplotlib.pyplot as plt

    x = [1, 2, 3, 4, 5]
    y = [i**2 for i in x]

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Square Numbers")
    ax.set_xlabel("x")
    ax.set_ylabel("y = x^2")
    # Instead of plt.show(), return the figure as a Marimo output:
    return mo.out(fig)


@app.cell
def _(mo):
    # You can also display markdown or other outputs
    return mo.md("## This is a demo Marimo notebook!")


if __name__ == "__main__":
    app.run()
