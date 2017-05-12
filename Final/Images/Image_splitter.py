import image_slicer
import os.path

fullPath = '/Users/Alma/Documents/Processing/SignProject/Images/Images/Small/'
os.path.dirname(fullPath)

print fullPath

for image in range(20):
    image_slicer.slice(fullPath + 'Untitled-1-' + str(image+1).zfill(2) + '.png', 16)