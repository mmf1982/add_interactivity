import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import numpy as np


def add_interactivity(legend=None, lines=None, fig=None, lines2=None,ncol=1,loc=0, ax=None):
    global gid, text_box
    text_box = None
    if fig is None:
        fig= plt.gcf()
    if ax is None:
        ax = plt.gca()
    if lines is None:
        lines=ax.get_lines()
    for line in lines:
        if line.get_label()[0] == "_":
            line.set_label(line.get_label()[1:])
    if legend is None:
        legend =  ax.legend(loc=loc,ncol=ncol)
    if int(matplotlib.__version__[0]) >= 3:
        legend.set_draggable(True)
    else:
        legend.draggable(True)
    linedic = {}
    for legline, line, text in zip(legend.get_lines(), lines, legend.get_texts()):
        if legline.get_linestyle() is "None":
            print("detected none")  #mention problems with linestyle is None
            legline.set_linewidth(0)
            legline.set_linestyle("-")
        linedic[legline] = (line, text)
        legline.set_picker(5)
    if lines2 is not None:
        for line2, line in zip(lines2, lines):
            linedic[line2] = (line, " ")
            line2.set_picker(5)
    def onpick(event):
        global text_box
        leg = event.artist
        try:
            (plotline, mtext) = linedic[leg]
            isline = True
        except:
            isline = False
        #try:
        if event.mouseevent.button == 3 and isline:
            maxordernow = np.nanmax(
                np.array([linedic[ll][0].get_zorder() for ll in linedic]))
            plotline.set_zorder(maxordernow+1)
            legend.set_zorder(maxordernow+2)
        elif event.mouseevent.button == 1 and isline:
            vis = not plotline.get_visible()
            plotline.set_visible(vis)
            if vis:
                leg.set_alpha(1.0)
                plotline.set_alpha(1.0)
                leg._legmarker.set_alpha(1.0)  # for markers
                mtext.set_visible(True)
            else:
                #mtext.text = "bla"
                mtext.set_visible(False)
                leg.set_alpha(0.1)
                plotline.set_alpha(0.0)  # for markers
                leg._legmarker.set_alpha(0.1)  # for markers
                leg.get_label()
        elif event.mouseevent.button == 2 and isline:
            print("Type the new label in the box")
            #fig.canvas.mpl_disconnect(gid)
            def submit(text):
                # print("you typed", text)
                mtext.set_text(text)
                ax2.remove()
                fig.canvas.draw()
                #gid = fig.canvas.mpl_connect('pick_event', onpick)
            ax2 = plt.axes([0.1, 0.05, 0.8, 0.075])
            text_box = TextBox(ax2, 'change leg ', initial="")
            text_box.on_submit(submit)
            #gid = fig.canvas.mpl_connect('pick_event', onpick)
        #except:
        #    pass
        fig.canvas.draw()
    gid = fig.canvas.mpl_connect('pick_event', onpick)
    return text_box


if __name__ == "__main__":
    plt.plot(np.arange(10), lw=6)
    plt.plot(np.arange(10)**1.5, 'o', ms=12)
    plt.plot(np.sin(np.arange(10))*5, lw=6)
    print("This is a simple plot to which interactivity has been added")
    print("with any button pressed on the legend, you can drag and drop")
    print("press the left mouse button on top of a legend line to turn it off")
    print("press again the left mouse button on top of the same line to turn in on again")
    print("press the right mouse button on top of a legend line (not label) to bring it to the front")
    print("press the middle mouse button on top of a legend line to open a textbox", end=" ")
    print("in this text box, write the new label for that line, then press enter")
    ma = add_interactivity()
    plt.show()

