#PRINT A PIE CHART TO REPRESENT DATA
#THIS WILL BE USED FOR EVERY FILE IN ORDER TO SHOW THE NUMBER OF REVISIONS EACH USER HAS MADE (% contribution)
#MATPLOTLIB API

#-----------------------------------------------------------------------------------------------

#BEFORE USING THE API YOU NEED TO INSTALL MATPLOTLIB

#1. OPEN COMMAND PROMPT
#2. TYPE IN   python -mpip install -U pip
#             python -mpip install -U matplotlib

#3. If this doesn't work, I recommend either reinstalling a later version of python which has pip installed. Otherwise you can just try to
# install pip separately, then try. This didn't work with my python 3.6 at home, but worked with python 3.7.
import time
import mpld3
import random
import matplotlib.pyplot as plt

#ignore this, was just for testing random values
import numpy as np
np.random.seed(int(time.time()))
#making a function which can be called from the flask file
def pie_chart(users):
    #LIST to hold the integer data (whatever it is we want that to be, for each pie chart)
    slices_numberOfRevisions = users.values()

    # LIST to hold colours for each modifying user
    color = ["red", "blue", "green", "yellow", "purple", "orange", "black"]

    # function to generate list with unique colors
    def select(data):
        if data != []:
            elem = random.choice(data)
            data.remove(elem)
            return elem
        else:
            return None

    # List generated to hold random colors for different users
    rand_colours = [select(color) for i in range(len(users))]

    #CALL the pie function from the api which takes the integer data, category data, colour data, starting angle of the pie chart segments (this doesn't matter), then autopct puts labels on the pie chart segments if it's wanted)
    plt.pie(slices_numberOfRevisions, labels=users, colors=rand_colours, startangle=90, autopct='%.1f%%', shadow=True,radius = 1)

    plt.title('Number of revisions per modifying user')
    plt.show()
    fig = plt.figure()
    mpld3.save_html(fig, "test.html")
    mpld3.fig_to_html(fig, template_type="simple")
    #mpld3.show()
    #DISPLAY the pie chart
    #mpld3.show()

    #------------------------------------------------------------------------------------------------
#test case

users = {
    'man': 100,
    'tito': 29,
    'jack': 4,
    'bhas': 70,
    'mike': 18
}
pie_chart(users)