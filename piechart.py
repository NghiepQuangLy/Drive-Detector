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


import matplotlib.pyplot as plt

#ignore this, was just for testing random values
import numpy as np
np.random.seed(444)

#LIST to hold the integer data (whatever it is we want that to be, for each pie chart)
slices_numberOfRevisions = [69, 24, 36, 74, 109]

#LIST to hold the category data (whatever it is we want that to be, for each pie chart)
users = ['Jack', 'Manvendra', 'Mike', 'Vibhas', 'Tito']

#LIST to hold colours for each modifying user
colors = ['r', 'g', 'b', 'c', 'm']

#CALL the pie function from the api which takes the integer data, category data, colour data, starting angle of the pie chart segments (this doesn't matter), then autopct puts labels on the pie chart segments if it's wanted)
plt.pie(slices_numberOfRevisions, labels=users, colors=colors, startangle=90, autopct='%.1f%%')

plt.title('Number of revisions per modifying user')
           
#DISPLAY the pie chart
plt.show()

#------------------------------------------------------------------------------------------------



