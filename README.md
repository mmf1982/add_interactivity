# add_interactivity

Adding a moveable and clickable legend (with function add_interactivity) and copy/ paset lines and delete lines (with function enable_copy_paste)

to run a test:

    python3.7 -m add_interactivity

This will open a plot with two axis (right panel empty) (left: 3 lines, where 2 lines and 1 with o marker). 

Functionality added by add_interactivity:

* click anywhere in the legend to move

* left click on a legend line toggles that line

* right click on a legend line bring it to the front

* middle click on a legend line opens a dialog to type a new name for that line, press enter when done.

* up/ down arrows together with left click in-/de-creases line thickness and/ or marker size.

* left/right changes legend font size 

* "l" + left click toggles the line (just the line, not marker)

* "+", "|", ">", "<", "1", "2", "3", "8", "D", "x", "X", "o", ".", "_", "|", "D" add or changes marker according to normal matplotlib rules (with the thick lines maybe not visible, decrease line thickness first).

* "r", "k", "g", "b", "c", "m", "y", "w" to change line/ marker color 

Functionality added by enable_copy_paste:

* double click on a line in the plot (not legend) removes the line

* right click on a line in the plot (not the legend) copies the line

* middle click in an axes adds the copied line, you can try in the same axis or in the empty one at the side

Save this file somewhere in your python path (e.g. .local/lib/site_packages/python3.7/add_interactivity) and then import it in your project as e.g.
    
    import add_interactivity as ai

You can then call it after you make your plot by:

    ai.add_interactivity(ax=None) # for the legend functionality on the current axis or the axis passed
    ai.add_ai_toall() # the same as ai.add_interactivity called on all open axes.
    ai.cp_one(mfig=None) # enable the copy/ paste delete functionality on the figure passed or active figure if none is passed
    ai.enable_copy_paste(figs=None)  #  same as cp_one on all figs:  (copy/ paste/ delete) functionality on all figures in list figs or on all open figures
    ai.interactive()  # to make both in one go on all open figures and axes.
    
If this file is left in the folder with the same name (i.e. add_interactivity, remember to use "from add_interactivity import add_interactivity as ai" instead).




