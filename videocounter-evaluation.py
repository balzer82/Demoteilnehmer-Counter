
# coding: utf-8

# # `Automatisierte` SCHÄTZUNG TEILNEHMERZAHL PEGIDA 18.05.2015
# 
# Evaluation des Algorithmus für neues Video

# ### 1. Download Video from YouTube

# In[16]:

#!youtube-dl https://www.youtube.com/watch?v=TMBY1Sb712k


# ### 2. Extract 1 image every 10 seconds
# 
# this depends, for sure, on the original fps of the video and the walking speed of the people
# 
# see http://www.linuxers.org/tutorial/how-extract-images-video-using-ffmpeg

# In[17]:

#!ffmpeg -i Pegida\ Demonstration\ 18.05.2015\ in\ Dresden-TMBY1Sb712k.mp4 -qscale:v 2 -r 1/10 -s hd720 screenshots/pegida_demo_18052015_%3d.jpg


# ### 3. Code some Stuff

# In[18]:

import cv2
print cv2.__version__

get_ipython().magic(u'matplotlib inline')
import numpy as np
import matplotlib.pyplot as plt
import Image

import os


# this little helper code is from here, in case you want to mark people in images: http://stackoverflow.com/questions/28476343/how-to-correctly-use-peopledetect-py-in-opencv

# In[19]:

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


# In[20]:

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)


# ### Histogram of oriented gradients (HOG) Descriptor for People Detection
# 
# see undocumented OpenCV: https://github.com/Itseez/opencv/blob/master/samples/python2/peopledetect.py

# In[21]:

def detectpeople(img, hitThreshold=-0.3, winStride=(6,6), padding=(32,32), scale=1.05, crowd_factor=1.8, save_result_as='None'):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    found, w = hog.detectMultiScale(img, hitThreshold=hitThreshold, winStride=winStride, padding=padding, scale=scale)
    
    found_filtered = []
    for ri, r in enumerate(found):
        for qi, q in enumerate(found):
            if ri != qi and inside(r, q):
                break
        else:
            found_filtered.append(r)

    #print '%d (%d) found' % (len(found_filtered), len(found))
    
    # because of hidden people behind others,
    # we multiply with empirically choosen crowd factor 
    people = int(len(found_filtered)*crowd_factor)

    
    if save_result_as!='None':
        #draw_detections(img, found)
        draw_detections(img, found_filtered, 3)

        plt.title(u"%i Personen in Bild #%s geschätzt" % (people, save_result_as[-14:-11]))
        plt.imshow(img, cmap='gray')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(save_result_as, dpi=150)
        plt.close()

    return people


# # Look at all the Pegidas!
# 
# ![](http://i.imgur.com/aW8KocQ.jpg)

# In[22]:

screenshots = [f for f in os.listdir('./screenshots') if f.endswith('.jpg') and not f.endswith('marked.jpg')]


# In[23]:

#screenshots = ['pegida_demo_11052015_022.jpg']


# In[24]:

demonstrationszug = []
for jpg in screenshots:
    
    jpgname = './screenshots/' + jpg
    
    capture = cv2.cv.CaptureFromFile(jpgname)
    if not capture:
        print "Error loading video file"
        break

    img = cv2.cv.QueryFrame(capture)
    img = np.array(img[:])

    people = detectpeople(img, save_result_as=jpgname[:-4]+'_marked.jpg')
    
    print(u'%i Teilnehmer auf \'%s\' geschätzt.' % (people, jpg))
    
    demonstrationszug.append(people)


# In[25]:

plt.bar([b+5 for b in range(len(demonstrationszug))], demonstrationszug)
plt.xlabel('Bild #')
plt.ylabel('Anzahl Personen im Bild')


# In[26]:

print('Insgesamt %i Teilnehmer.' % np.sum(demonstrationszug))


# manuell wurden durch [STUDENTENGRUPPE "DURCHGEZAEHLT"](https://durchgezaehlt.wordpress.com) 2.601 Personen im Demonstrationszug gezählt

# ## Fehlerquellen
# 
# * doppelt gezähle Personen (auf 2 Fotos abgebildet)
# * nicht gezählte Personen (Verdeckte)
# * falscher `crowd_factor` (dieser stimmt mit Sicherheit nur für dieses Beispiel)
# 
# Fragen? [@Balzer82](https://twitter.com/balzer82)

# `CC-BY-SA 2.0 Lizenz`
