#!/usr/bin/env python

'''
tag_generator.py
Copyright 2017 Long Qian
Contact: lqian8@jhu.edu
This script creates tags for your Jekyll blog hosted by Github page.
No plugins required.

Modified by Michael Vaiana to handle tag lists of the form: [tag one, tag two, tagthree, ..., the last tag]
'''

import glob
import os
import re

post_dir = '_posts/'
tag_dir = 'tag/'

filenames = glob.glob(post_dir + '*md')

total_tags = []
for filename in filenames:
    f = open(filename, 'r', encoding="utf8")
    crawl = False
    for line in f:
        if crawl:
            current_tags = line.strip().split(':')
            #current tags = ['tags,', '[tag one, tag two, ... , tag N]']
            if current_tags[0] == 'tags':
                raw_tags = re.search(r'\[([^\]]*)',current_tags[1]).group(1).split(',')
                total_tags.extend(tag.strip() for tag in raw_tags)
                crawl = False
                break
        if line.strip() == '---':
            if not crawl:
                crawl = True
            else:
                crawl = False
                break
    f.close()
total_tags = set(total_tags)
print(total_tags)

old_tags = glob.glob(tag_dir + '*.md')
for tag in old_tags:
    os.remove(tag)

for tag in total_tags:
    tag_filename =  tag_dir + tag.replace(' ', '-')  + '.md'
    f = open(tag_filename, 'a')
    write_str = '---\nlayout: tagpage\ntitle: \"Tag: ' + tag + '\"\ntag: ' + tag + '\nrobots: noindex\n---\n'
    f.write(write_str)
    f.close()
print("Tags generated, count", total_tags.__len__())
