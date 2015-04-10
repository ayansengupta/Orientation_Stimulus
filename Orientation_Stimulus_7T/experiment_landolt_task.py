#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui, monitors
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import random
import os  # handy system and path functions
import combination_mh_asg as combi
import random
import Image
import codecs

total_runs = 10
screen_refresh = 60.0 # Hz
flicker_freq = 2.0 # Hz

# Store info about the experiment session
expName = u'Field_Strength_Comparison'  # from the Builder filename that created this script
#expInfo = {u'session': u'001', u'participant': u'', u'Speed of Reading in Hz': u'1'}
expInfo = {u'session': u'001', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName


# Setup files for saving
directory ='log_data_'+expName+os.path.sep+expInfo['participant']
if not os.path.isdir(directory):
    os.makedirs(directory)  # if this fails (e.g. permissions) we will get error
filename = directory + os.path.sep +'session_%s_%s' %(expInfo['session'], expInfo['date'])
logFile = logging.LogFile(filename+'.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

mon = monitors.Monitor('7T_Projector')#fetch the most recent calib for this monitor
mon.setDistance(100)


#create a window
win = visual.Window([1280,1024],monitor= mon, screen=1, units="deg", winType='pyglet', fullscr=1)
win.setMouseVisible(False)


#track all keypress
Keyinputs = event.getKeys(keyList=['t','1','2'], timeStamped=True)


#create instruction
Instructions = visual.TextStim(win=win, ori=0, name='Instructions_about_task',
    text=u'Bitte schauen Sie in die Mitte des Bildschirms. Bitte dr\xfccken Sie die linke Taste, wenn Sie bereit sind.',    font='Arial',
    units='deg', pos=[0, 0],alignHoriz='center',height=0.4,  wrapWidth=12,
    color='white', colorSpace='rgb', opacity=1,bold=True)
    
Instructions.setAutoDraw(True)
win.flip()
event.waitKeys(maxWait=500, keyList=['1'], timeStamped=True)
Instructions.setAutoDraw(False)

#create some stimuli

Swisher_LH = [visual.ImageStim(win=win, name='Swisher_LH',units=u'pix', 
    image='sin', mask=None, 
    ori=0, pos=[-320, 0], size=[640,1024],
    color=[1,1,1], colorSpace=u'rgb', opacity=1,
    interpolate=True, autoLog=True)for x in range(4)]

Swisher_RH = [visual.ImageStim(win=win, name='Swisher_RH',units=u'pix', 
    image='sin', mask=None,
    ori=0, pos=[320,0], size=[640, 1024],
    color=[1,1,1], colorSpace=u'rgb', opacity=1,
    texRes=128, interpolate=True, autoLog=True)for x in range(4)]

radius_of_ring_deg=0.12
Landolt_ring_outer = visual.Circle(win=win, name='Landolt_ring_outer',units='deg', fillColor=(-1.0, -1.0, -1.0), 
    radius=radius_of_ring_deg, ori=0, pos=[0, 0], lineColor=(-1.0, -1.0, -1.0), autoLog=True)
Landolt_ring_inner = visual.Circle(win=win, name='Landolt_ring_inner',units='deg', fillColor=(0.0, 0.0, 0.0), 
    radius=3/5*radius_of_ring_deg, ori=0, pos=[0, 0], lineColor=(0.0, 0.0, 0.0), autoLog=True)
Landolt_C = visual.Rect(win=win, name='Landolt_C',units='deg', fillColor=(0, 0, 0), 
    lineColor=(0, 0, 0), ori=0, pos=[-radius_of_ring_deg/2, 0], width=1.4*(radius_of_ring_deg), height=2/5*radius_of_ring_deg, autoLog=True)

#initialize the speed of flashing letters
logging.flush()


#Loop to execute the experimental runs
for exp_runN in range(total_runs):
    temporal_combi_list=combi.combination_for_run()
    Trial_times=[4 for i in xrange(len(temporal_combi_list))]

    Instructions = visual.TextStim(win=win, ori=0, name='Next_Scan_Ready', \
        text=u'Bitte machen Sie sich bereit für einen nächsten Scan',    font='Arial', \
        units='deg', pos=[0, 0],alignHoriz='center',height=0.4,  wrapWidth=12,bold=True, \
        color='white', colorSpace='rgb', opacity=1)
    Instructions.draw()
    win.flip()

    #wait for trigger and sychronize
    event.waitKeys(maxWait=6400, keyList=['t'], timeStamped=True)
    logging.flush()

    Run_clock = core.Clock()
    logging.setDefaultClock(Run_clock)


    logFile.write("\nTemporal_Combi:  %s \n" %str(temporal_combi_list))
    logFile.write("\nTrial_times_with_jitter:  %s \n" %str(Trial_times))
    start_run=Run_clock.getTime()
    logging.exp("Start of Experimental Run: "+str(exp_runN))

    intervals_of_landolt=range(len(temporal_combi_list))

    #inside one experimental run -> execute trials
    for trialN in range(len(temporal_combi_list)):
        start_trial=Run_clock.getTime()
        [l, r]=temporal_combi_list[trialN]


        LH_image_name=[]
        RH_image_name=[]

        print 'Before setting image %f'%Run_clock.getTime()

        if l==1:
            for i in range(4):
                Swisher_LH[i].setImage('orientation_images/LH_0'+'_'+str(i+1)+'.png')
                LH_image_name+=['orientation_images/LH_0'+'_'+str(i+1)+'.png']
        elif l==2:
            for i in range(4):
                Swisher_LH[i].setImage('orientation_images/LH_45'+'_'+str(i+1)+'.png')
                LH_image_name+=['orientation_images/LH_45'+'_'+str(i+1)+'.png']
        elif l==3:
            for i in range(4):
                Swisher_LH[i].setImage('orientation_images/LH_90'+'_'+str(i+1)+'.png') 
                LH_image_name+=['orientation_images/LH_90'+'_'+str(i+1)+'.png']
        elif l==4:
            for i in range(4):
                Swisher_LH[i].setImage('orientation_images/LH_135'+'_'+str(i+1)+'.png')
                LH_image_name+=['orientation_images/LH_135'+'_'+str(i+1)+'.png']
        else:  
            for i in range(4):
                Swisher_LH[i].setImage('orientation_images/Blank.png')
                LH_image_name+=['orientation_images/Blank.png']
                
        if r==1:
            for i in range(4):
                Swisher_RH[i].setImage('orientation_images/RH_0'+'_'+str(i+1)+'.png')
                RH_image_name+=['orientation_images/RH_0'+'_'+str(i+1)+'.png']
        elif r==2:
            for i in range(4):
                Swisher_RH[i].setImage('orientation_images/RH_45'+'_'+str(i+1)+'.png')
                RH_image_name+=['orientation_images/RH_45'+'_'+str(i+1)+'.png']
        elif r==3:
            for i in range(4):
                Swisher_RH[i].setImage('orientation_images/RH_90'+'_'+str(i+1)+'.png')
                RH_image_name+=['orientation_images/RH_90'+'_'+str(i+1)+'.png']
        elif r==4:
            for i in range(4):
                Swisher_RH[i].setImage('orientation_images/RH_135'+'_'+str(i+1)+'.png')
                RH_image_name+=['orientation_images/RH_135'+'_'+str(i+1)+'.png']
        else:  
            for i in range(4):
                Swisher_RH[i].setImage('orientation_images/Blank.png')
                RH_image_name+=['orientation_images/Blank.png']
                

        print 'After setting image %f'%Run_clock.getTime()

        count_trigger=1
        frameN = 0

        if trialN in intervals_of_landolt:
            print '\nLandolt\'s Ring setup for Trial %d'%trialN
            jitter_offset=randint(450)

        while True: #this creates a loop with frames

            frameN += 1
            if len(event.getKeys(["t"]))>0: 
                count_trigger+=1
                print 'Trigger %d is received'%count_trigger 
            if count_trigger==(Trial_times[trialN]+1):
                print '\nTrigger is received to start a new Trial at %f'%Run_clock.getTime()
                logging.flush()
                break

            if np.mod(frameN,15)==1:
                index=randint(4)
            if (Run_clock.getTime()-start_trial) <= 3.0:
                if np.mod((Run_clock.getTime()-start_trial),0.25)<=0.125:
                    Swisher_LH[index].draw()
                    Swisher_RH[index].draw()

            ###Landolt's task
            Landolt_ring_outer.draw()
            Landolt_ring_inner.draw()
            
            if trialN in intervals_of_landolt:
                if frameN == jitter_offset:
                    direction=random.choice([1,-1])
                    Landolt_C.pos*=direction
                    if float(Landolt_C.pos[0]) > 0.0:
                        logging.exp("Displaying Landolt's C.....Right")
                        print "\nDisplaying Landolt's C.....Right"
                    else:
                        logging.exp("Displaying Landolt's C.....Left")
                        print "\nDisplaying Landolt's C.....Left"

                if frameN>=jitter_offset and frameN<jitter_offset+13:
                    Landolt_C.draw()
            if len(event.getKeys(["1"]))>0: 
                logging.exp("Subject Response.....Left")
                print "Subject Response.....Left"
            elif len(event.getKeys(["2"]))>0:
                logging.exp("Subject Response.....Right")
                print "Subject Response.....Right"
            else:
                pass

            win.flip(clearBuffer=True)
  
            # TODO REPORT THIS TIME, but only when there is a new stimulus on the screen
            if frameN == 1:
                logging.exp("New stimulus presentation started for Trial %s.....%s    %s" % (str(trialN), str('_'.join(LH_image_name[index].split('/')[-1].split('.')[0].split('_')[0:2])), str('_'.join(RH_image_name[index].split('/')[-1].split('.')[0].split('_')[0:2]))))
               
            #break out from the whole experiment

            if len(event.getKeys(["escape"]))>0: 
                win.close()
                core.quit()
        print "Total trial time: %f" %(Run_clock.getTime()-start_trial)


#create the end screen with thank you. This screen is shown after all the runs are over...
Instructions = visual.TextStim(win=win, ori=0, name='Thank_you_end',
    text=u'Das war\'s. Vielen Dank!',    font='Arial',
    units='deg', pos=[0, 0],alignHoriz='center',height=0.4,  wrapWidth=12,bold=True,
    color='white', colorSpace='rgb', opacity=1)
    
Instructions.setAutoDraw(True)
win.flip() 

event.waitKeys(maxWait=10, keyList=['escape'], timeStamped=True)
  

#cleanup
event.clearEvents()
win.close()
core.quit()
