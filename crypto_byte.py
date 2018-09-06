#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

class getsizeERRO(Exception):
    pass

def get_file_size(file_name):
    s = os.path.getsize(file_name)
    if s == 0:
        raise getsizeERRO('File Size value 0')
    else :
       return s

def save(file_name,data):
    f = open(file_name, 'w')
    f.write(data)
    f.close()

def strbin_to_byte(strbin):
    a = ''
    for s in strbin:
        for b in s :
            a += chr(int(b,2))
    return a

def byte_to_strbin(s):
    a = []
    for c in s:
        a.append(bin(ord(c)).replace('0b', ''))
    return a

def read_file(file_name,read_interval):
    print '* Read interval:%s' % str(read_interval)
    f = open(file_name,'r')
    data = ''
    dlen = 0
    file_bin = []
    f.seek(read_interval[0], 1)
    for i in xrange(read_interval[1]-read_interval[0]):
        data = data + f.read(1)
        dlen+=1
        if len(data) == 32:
            file_bin.append(byte_to_strbin(data))
            data = ''
        else :
            pass
        file_bin.append(byte_to_strbin(data))
        data = ''
    f.close()
    print '* Read done.\n* Datalen:%s' % dlen
    return file_bin

if __name__ == '__main__' :
    mode = 'test'
    if len(sys.argv) > 1 :
        for a in sys.argv:
            al = a.split('=')
            if al[0] == 'source_file':
                file_name = al[1]
            if al[0] == 'save_file':
                save_file = al[1]
            if al[0] == 'mode':
                mode = al[1]
            else :
                pass
    else :
        print 'crypto_byte.py  mode={encrypt|decrypt} source_file=/bin/bash save_file=bash'
        exit(0)
    try :
        file_size = get_file_size(file_name)
    except getsizeERRO as e:
        print '*' ,e ,', getFilesizeERRO block device?'
        file_size = int(raw_input('* Input stop_byte :'))
    except Exception as e:
        print e
        exit()

    if mode == 'test':
        strbin = read_file(file_name,[0,file_size])
        save(save_file,strbin_to_byte(strbin))
    elif mode == 'encrypt' :
        read_file(file_name,[0,file_size])
    elif mode == 'decrypt' :
        save(save_file,strbin_to_byte(strbin))
