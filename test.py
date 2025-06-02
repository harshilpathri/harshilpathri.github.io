import os

for i in os.listdir("images/cards"):
    newName = i[0].upper() + i.split('_')[-1][0].upper() + ".png"
    os.rename("images/cards/" + i, "images/cards/" + newName)