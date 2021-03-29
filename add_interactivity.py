""" Module to add interactivity to matplotlib legends"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import TextBox
coords = None
legn = None

def add_interactivity(legend=None, lines=None, fig=None, lines2=None, ncol=1, loc=0, ax=None, nodrag=False, legsize=12):
    """
    Function to add basic interactivity to an axes

    - with any button pressed on the legend outside a legend line, drag and drop
    - press the left mouse button on top of a legend line to toggle it off/ on
    - down/ up while pressing left button, de-/increases marker size/ line width
    - right mouse button on top of legend line (not label) to bring it to front
    - middle button on top of legend line to open textbox to enter line name

    Parameters:
    ------------
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
    (ax: axis handle
        axes to make interactive
    (nodrag: bool
        enable/ disable draggable legend
    (legsize: int
        font size of legend label

    """
    if fig is None:
        fig = plt.gcf()
    if ax is None:
        ax = plt.gca()
    if lines is None:
        lines = ax.get_lines()
        all_indices = []
        for iidd, line in enumerate(lines):
            if len(line.get_data()[0]) == 0 and not line.get_visible():
                all_indices.append(iidd)
        for in_iidd in all_indices[::-1]:
            _ = lines.pop(in_iidd)
    for line in lines:
        if line.get_label()[0] == "_":
            line.set_label(line.get_label()[1:])
    if legend is None:
        legend = ax.legend(loc=loc, ncol=ncol, prop={"size": legsize})
    if not nodrag:
        if int(matplotlib.__version__[0]) >= 3:
            legend.set_draggable(True)
        else:
            legend.draggable(True)
    linedic = {}
    for legline, line, text in zip(legend.get_lines(), lines, legend.get_texts()):
        if legline.get_linestyle() == "None":
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
        # print(event, event.mouseevent.button, leg, leg.get_label())
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
        elif event.mouseevent.button == 2 and isline and not nodrag:
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
        elif event.mouseevent.key == "left" and not isline and event.mouseevent.button == 1:
            if leg.parent == ax:
                if legend.texts[0].get_fontsize() > 1:
                    legend.texts[0].set_fontsize(legend.texts[0].get_fontsize()-1)
        elif event.mouseevent.key == "right" and not isline and event.mouseevent.button == 1:
            if leg.parent == ax:
                legend.texts[0].set_fontsize(legend.texts[0].get_fontsize()+1)
        fig.canvas.draw()
    _ = fig.canvas.mpl_connect('pick_event', onpick)

def add_ai_toall():
    '''
    add interactive legend to all axes in all open figures
    '''
    for mfignum in plt.get_fignums():
        mfig = plt.figure(mfignum)
        for ax in mfig.axes:
            add_interactivity(fig=mfig, ncol=1, loc=0, ax=ax, nodrag=False, legsize=10)

def enable_copy_paste():
    '''
    Function to call after plots are created to be able to copy paste line plots

    A pick event on lines is activated and will copy the line data if 'c' is
    pressed when the line is selected.

    Clicking in any axes that was already present before this function had been
    called, and clicking again while pressing 'v' will add the currently copied
    plot
    '''
    print("to copy a line, click the right mouse button on a line")
    print("to paste, press the middle mouse button in an axes")
    global coords, legn
    def onpick(event):
        global coords, legn, artist
        artist = event.artist
        if event.mouseevent.button == 3 and type(artist) != matplotlib.legend.Legend:
            try:
                leglines = event.artist.axes.get_legend().get_lines()
            except AttributeError:
                leglines = []
            if not artist in leglines:
                coords = artist.get_data()
                legn = artist.get_label()
                print("copied ",legn)
            else:
                pass
        else:
            pass
    def onclick(event):
        global coords, legn
        if event.button == 2:
            print("pasted ", legn)
            print("coordrange x: ", np.nanmin(coords[0]), np.nanmax(coords[0]))
            print("coordrange y: ", np.nanmin(coords[1]), np.nanmax(coords[1]))
            ax = event.inaxes
            ax.plot(coords[0], coords[1], label=legn)
            ax.figure.canvas.draw()
    for mfignum in plt.get_fignums():
        mfig = plt.figure(mfignum)
        for ax in mfig.axes:
            for lin in ax.lines:
                lin.set_picker(5)
        d = mfig.canvas.mpl_connect("pick_event", onpick)
        f = mfig.canvas.mpl_connect('button_press_event', onclick)

def main():
    fig, ax = plt.subplots(1,2)
    ax[0].plot(np.arange(10), lw=6)
    ax[0].plot(np.arange(10) ** 1.5, 'o', ms=12)
    ax[0].plot(np.sin(np.arange(10)) * 5, lw=6)
    print(
        "This is a simple plot to which interactivity has been added:\n",
        " \n",
        "* with any button pressed on the legend outside a legend line, you can drag and drop the legend\n",
        "* press the left mouse button on top of a legend line to turn it off/ on\n",
        "* down/ up arrows holding while pressing left button, de-/increases marker size and line width\n",
        "* press the right mouse button on top of a legend line (not label) to bring it to the front\n",
        "* press the middle mouse button on top of a legend line to open a textbox\n",
        "  in this text box, write the new label for that line, then press enter\n",
        "* press left/ right arrows while pressing left mouse button to in/de crease text size\n",
        "    New features: \n",
        "* a right mouse click on a line in the left plot copies the data.\n",
        "* click middle button in the right plot to paste it.\n")
    add_interactivity(ax=ax[0])
    enable_copy_paste()
    plt.show()


if __name__ == "__main__":
    main()
