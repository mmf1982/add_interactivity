import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import TextBox


def add_interactivity(legend=None, lines=None, fig=None, lines2=None, ncol=1, loc=0, ax=None):
    """
    Function to add basic interactivity to an axes

    Add the following interactivity to an axis:
    - with any button pressed on the legend outside a legend line, drag and drop
    - press the left mouse button on top of a legend line to turn it off/ on
    - down/ up while pressing left button, de-/increases marker size/ line width
    - right mouse button on top of legend line (not label) to bring it to front
    - middle button on top of legend line to open textbox to enter line name

    Parameters:
    -----------
    (legend: legend handle
        a specific already existing legend can be passed. If none, a new legend
        is created)
    (lines: list of line handles
        a list of line handles corresponding to the legend. If None, all lines
        that are currently present in the plot are extracted. This can lead to
        problems if the legend that is passed does not contain all lines that
        are extracted)
    (fig: figure handle
        if None, the figure is assumed to be the figure of the axes supplied, or
        if no axis is supplied, the figure of the current active axis)
    (lines2: list of line handles
        instead of binding a legend to the lines in a figure, lines from another
        axis are made clickable)
    (ncol: integer
        number of columns in which to distribute the legend)
    (loc: integer
        passed to the legend creation. 0 for "best", see matplotlib.pylot.legend
        "loc" for help on parameters.
    """
    if fig is None:
        fig = plt.gcf()
    if ax is None:
        ax = plt.gca()
    if lines is None:
        lines = ax.get_lines()
    for line in lines:
        if line.get_label()[0] == "_":
            line.set_label(line.get_label()[1:])
    if legend is None:
        legend = ax.legend(loc=loc, ncol=ncol)
    if int(matplotlib.__version__[0]) >= 3:
        legend.set_draggable(True)
    else:
        legend.draggable(True)
    linedic = {}
    for legline, line, text in zip(legend.get_lines(), lines, legend.get_texts()):
        if legline.get_linestyle() is "None":
            print("detected none")  # mention problems with linestyle is None
            legline.set_linewidth(0)
            legline.set_linestyle("-")
        linedic[legline] = (line, text)
        legline.set_picker(5)
    if lines2 is not None:
        for line2, line in zip(lines2, lines):
            linedic[line2] = (line, " ")
            line2.set_picker(5)

    def onpick(event):
        """
        function to be called on click (left, middle, right) on an artist
        """
        leg = event.artist
        try:
            (plotline, mtext) = linedic[leg]
            isline = True
        except:
            isline = False
            plotline = None
            mtext = None
        if event.mouseevent.button == 3 and isline:
            maxordernow = np.nanmax(
                np.array([linedic[ll][0].get_zorder() for ll in linedic]))
            plotline.set_zorder(maxordernow + 1)
            legend.set_zorder(maxordernow + 2)
        elif event.mouseevent.button == 1 and isline:
            if event.mouseevent.key is None:
                vis = not plotline.get_visible()
                plotline.set_visible(vis)
                if vis:
                    leg.set_alpha(1.0)
                    plotline.set_alpha(1.0)
                    leg._legmarker.set_alpha(1.0)  # for markers
                    mtext.set_visible(True)
                else:
                    mtext.set_visible(False)
                    leg.set_alpha(0.1)
                    plotline.set_alpha(0.0)  # for markers
                    leg._legmarker.set_alpha(0.1)  # for markers
                    leg.get_label()
            else:
                lw = leg.get_linewidth()
                ms = leg._legmarker.get_markersize()
                if event.mouseevent.key == "up":
                    if lw > 0:
                        leg.set_linewidth(lw + 1)
                        plotline.set_linewidth(lw + 1)
                    leg._legmarker.set_markersize(ms + 1)
                    plotline.set_markersize(ms + 1)
                elif event.mouseevent.key == "down":
                    if lw > 1:
                        leg.set_linewidth(lw - 1)
                        plotline.set_linewidth(lw - 1)
                    if ms > 1:
                        leg._legmarker.set_markersize(ms - 1)
                        plotline.set_markersize(ms - 1)
                else:
                    print("not implemented feature. Only down and up keys allowed")
        elif event.mouseevent.button == 2 and isline:
            print("Type the new label in the box")

            def submit(stext):
                print("you typed", stext)
                mtext.set_text(stext)
                ax2.remove()
                fig.canvas.draw()
                text_box.disconnect_events()

            ax2 = plt.axes([0.12, 0.05, 0.78, 0.075])
            text_box = TextBox(ax2, 'new leg ', initial="")
            text_box.on_submit(submit)
        fig.canvas.draw()

    _ = fig.canvas.mpl_connect('pick_event', onpick)
    return


if __name__ == "__main__":
    plt.plot(np.arange(10), lw=6)
    plt.plot(np.arange(10) ** 1.5, 'o', ms=12)
    plt.plot(np.sin(np.arange(10)) * 5, lw=6)
    print(
        "This is a simple plot to which interactivity has been added",
        "with any button pressed on the legend outside a legend line, you can drag and drop",
        "press the left mouse button on top of a legend line to turn it off/ on",
        "down/ up arrows holding while pressing left button, de-/increases marker size and line width",
        "press again the left mouse button on top of the same line to turn in on again",
        "press the right mouse button on top of a legend line (not label) to bring it to the front",
        "press the middle mouse button on top of a legend line to open a textbox",
        "in this text box, write the new label for that line, then press enter")
    add_interactivity()
    plt.show()
