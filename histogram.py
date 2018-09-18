#PRINT A HISTOGRAM TO REPRESENT ACTIONS PERFORMED FOR A FILE
#THIS WILL BE USED FOR EVERY FILE IN ORDER TO SHOW THE NUMBER OF CONTRIBUTIONS EACH USER IN THE TEAM_DRIVE HAS MADE (actual integer amounts for each action)
#MATPLOTLIB API

#-----------------------------------------------------------------------------------------------

#BEFORE USING THE API YOU NEED TO INSTALL MATPLOTLIB

#1. OPEN COMMAND PROMPT
#2. TYPE IN   python -mpip install -U pip
#             python -mpip install -U matplotlib

#3. If this doesn't work, I recommend either reinstalling a later version of python which has pip installed. Otherwise you can just try to
# install pip separately, then try. This didn't work with my python 3.6 at home, but worked with python 3.7.

import matplotlib.pyplot as plt
import numpy as np
#def histogram(users):
#name of file
fileName = 'File1'

#name of team drive
teamDrive = 'FIT2101'

#legend keys
legend = ['Jack', 'Manvendra', 'Mike', 'Vibhas', 'Tito']

#number of users in team_drive
N = 5

#creating a subplot (multiple bar graphs in one)
fig, ax = plt.subplots()

#x locations for each user on the x-axis
#ind = np.arange(len(users))
ind = np.arange(N)

#width of each individual bar
width = 0.15  

#INSERTIONS
#--------------------------------------------------------------------------------
#data for each user regarding insertions
insertionsCount = [43, 28, 74, 62, 12] 

#create the first bar which represents insertions, coloured red
insertions = ax.bar(ind, insertionsCount, width, color='r', bottom=0, label = 'Insertions')


#DELETIONS
#---------------------------------------------------------------------------------
#data for each user regarding deletions
deletionsCount = [193, 29, 78, 165, 200]

#create the second bar which represents deletions, coloured yellow
deletions = ax.bar(ind + width, deletionsCount, width, color='y', bottom=0, label = 'Deletions')

#COMMENTS
#---------------------------------------------------------------------------------
#data for each user regarding comments
commentsCount = [15, 21, 18, 9, 26]

#create the third bar which represents comments, coloured blue
comments = ax.bar(ind + (2*width), commentsCount, width, color='b', bottom=0, label = 'Comments')

#EDITS
#---------------------------------------------------------------------------------
editsCount = [insertionsCount[0] + deletionsCount[0] + commentsCount[0], insertionsCount[1] + deletionsCount[1] + commentsCount[1], insertionsCount[2] + deletionsCount[2] + commentsCount[2], insertionsCount[3] + deletionsCount[3] + commentsCount[3], insertionsCount[4] + deletionsCount[4] + commentsCount[4]]

edits = ax.bar(ind + 3*(width), editsCount, width, color='g', bottom=0, label = 'Total Edits')

#set the axis title
ax.set_title('Actions per user for ' + fileName + ' in team_drive' + teamDrive)

#set where the x labels will be (centred in the middle of all 4 columns)
ax.set_xticks(ind + width + width / 2)

#label these x-axis labels
ax.set_xticklabels(('Jack', 'Manvendra', 'Mike', 'Vibhas', 'Tito'))

#create the legend
#ax.legend((insertions[0], deletions[0], comments[0], edits[0]), ('Insertion', 'Deletion', 'Comments', 'Total Edits'))
ax.legend()
#autoscale the axes based on the data that is fed into the insertions/deletions/comments/edit lists
ax.autoscale_view()

def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')

#positioning the text label to display individual bar height
autolabel(insertions, "center")
autolabel(deletions, "center")
autolabel(edits,"center")
autolabel(comments,"center")
#DISPLAY the graph
plt.show()
