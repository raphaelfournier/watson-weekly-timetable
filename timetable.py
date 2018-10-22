#! /usr/bin/env python
# -*- coding: utf-8 -*-
# http://masudakoji.github.io/2015/05/23/generate-timetable-using-matplotlib/en/

import json
from pprint import pprint
import arrow
import argparse
import os, errno
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import matplotlib.pyplot as plt
import matplotlib.patches as patches

days=['Lundi','Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']


def duration_in_minutes(arrowdelta):
    hours,remainder = divmod(arrowdelta.seconds,3600)
    minutes,seconds = divmod(remainder,60)
    duration = 60 * hours + minutes
    return duration

def get_color(tags,colors):
    for c in colors:
        if c in tags:
            return colors[c]
    return colors["default"]

print("/usr/bin/watson log --week -j > ./datawatson.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate weekly graphical timetable from watson frames')

    parser.add_argument(
        '--configfile',
        type=str,
        help='the name of the json where frames are stored')

    args = parser.parse_args()

    config = configparser.ConfigParser(defaults = {'configfile': './timetable.cfg'})
    try:
        config.read(config.defaults()['configfile'])
    except:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), configfile)

    frames = []

    title = config._sections['output']['pngfile']
    colors = config._sections['colors']

    fig=plt.figure(figsize=(10,5.89))
    ax=fig.add_subplot(111)

    weekendstart = 10-0.1
    weekendend = 20+0.1
    rect = patches.Rectangle((6-0.44,weekendstart),0.48,weekendend-weekendstart+0.1,linewidth=1,edgecolor='k',facecolor=colors["offline"])
    ax.add_patch(rect)
    rect = patches.Rectangle((7-0.44,weekendstart),0.48,weekendend-weekendstart+0.1,linewidth=1,edgecolor='k',facecolor=colors["offline"])
    ax.add_patch(rect)

    inputfilename = config._sections['input']['framesfile']

    with open(inputfilename) as f:
        frames = json.load(f)

    for frame in frames:
        start = arrow.get(frame["start"])
        stop = arrow.get(frame["stop"])
        diff = stop - start

        day = start.weekday()+1
        hour = start.hour
        minute = start.minute
        event = frame["project"]

        jour  = float(day) - 0.48
        begin = float(hour)+float(minute)/60
        end   = begin + float(duration_in_minutes(diff))/60

        blockcolor = get_color(frame["tags"],colors)

        if end-begin > 0.3:
            if jour < 5:
                # plot event
                rect = patches.Rectangle((jour,begin),0.96,end-begin,linewidth=0.5,edgecolor='grey',facecolor=blockcolor)
                ax.add_patch(rect)
                # plot beginning time
                plt.text(jour+0.02, begin+0.05 ,'{0}:{1:0>2}'.format(int(hour),int(minute)), ha='left',va='top', fontsize=5)
                # plot event name
                plt.text(jour+0.5, begin+0.1, event[:15], ha='center', va='top', fontsize=5, wrap=True)
            else:
                rect = patches.Rectangle((jour+0.48,begin),0.48,end-begin,linewidth=0.5,edgecolor='grey',facecolor=blockcolor)
                ax.add_patch(rect)
                # plot beginning time
                plt.text(jour+0.52, begin+0.05 ,'{0}:{1:0>2}'.format(int(hour),int(minute)), ha='left',va='top', fontsize=5)
                # plot event name
                plt.text(jour+0.5, begin+0.25, event[:15], ha='left', va='top', fontsize=5, wrap=True)


    # Set Axis
    ax.yaxis.grid()
    ax.set_xlim(0.5,len(days)+0.5)
    ax.set_ylim(float(config._sections['output']['starthour']),float(config._sections['output']['endhour']))
    ax.set_xticks(range(1,len(days)+1))
    ax.set_xticklabels(days)
    ax.set_ylabel('')

    # Set Second Axis
    ax2=ax.twiny().twinx()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_ylim(ax.get_ylim())
    ax2.set_xticks(ax.get_xticks())
    ax2.set_xticklabels(days)
    ax2.set_ylabel('')

    plt.title(title,y=1.07)
    imagename = '{0}.png'.format(title)
    print("writing",imagename)
    plt.savefig(imagename, dpi=200)
