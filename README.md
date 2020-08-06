# add_interactivity

Adding a moveable and clickable legend:

to run a test:

    python3.7 -m add_interactivity

This will open a plot with 3 lines (2 lines and 1 with o marker). 

* click anywhere in the legend to move

* left click on a legend line toggles that line

* right click on a legend line bring it to the front

* middle click on a legend line opens a dialog to type a new name for that line, press enter when done.

* up/ down arrows together with left click in-/de-creases line thickness and/ or marker size.

Save this file somewhere in your python path (e.g. .local/lib/site_packages/python3.7/add_interactivity) and then import it in your project as e.g.
    
    import add_interactivity as ai

You can then call it after you make your plot by:

    ai.add_legend()
    
If no arguments are provided, it acts on the current active axis and creates a legend with automated names, i.e. if nothing was set as label, line0 etc...

However, ax=axis_on_which_to_act is also supported. See 

    help(ai.add_interactivity)
   
for more options.


