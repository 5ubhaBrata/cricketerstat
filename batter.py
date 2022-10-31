#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 12:36:17 2022

@author: subhabrata
"""

import streamlit as st
import requests as r
from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image
import numpy as np

def batterlst(a):
    name=[]
    for i in range(len(a.split())):
       name += '+'+a.split()[i]
    name = "".join(name)
    
    req = r.get("https://search.espncricinfo.com/ci/content/site/search.html?search="+name+";type=player")
    bs = BeautifulSoup(req.text, features="html.parser")
    
    lst = []
    for soup_li in bs.find_all("h3"):
        if len(list(soup_li.children)) == 1 and soup_li.a:
            lst.append(soup_li.a["href"])
    return lst

def imgUrl(l):
    urls = []
    for i in range(len(l)):
        ro = r.get("https://search.espncricinfo.com" +l[i])
        bs = BeautifulSoup(ro.text, features="html.parser")
        
        img_url = bs.select_one('[property="og:image"]')['content']
        urls.append(img_url.split('?')[0] + '?type=original')
    return urls        
        
def battersc(l):
    score = []
    ro = r.get("https://search.espncricinfo.com" +l)
    bs = BeautifulSoup(ro.text, features="html.parser")
    
    tablehead = bs.find("thead")
    if tablehead != None:
        btags = [str(b.text).strip().strip(':') for b in tablehead.find_all("th")]
        tablebody = bs.find("tbody")
        bsibs = [str(b.text).strip().strip(':') for b in tablebody.find_all("td")]
        
        Test = dict(zip(btags, bsibs))
        ODI = dict(zip(btags, bsibs[15:]))
        T20I = dict(zip(btags, bsibs[30:]))
        score.append([Test, ODI, T20I])
    
    return score

def main():
    st.title("CRIC")
        
    name = st.text_input("Enter player name")
    if st.checkbox("Check"):
        listOfP = batterlst(name)
        imgurls = imgUrl(listOfP)
        imgs = []
        for i in range(len(imgurls)):
           imgs.append(Image.open(r.get(imgurls[i], stream=True).raw)) 
        if len(imgs) > 1:
            pick_img = st.radio("Which image?", 
               ["image " + str(x) for x in range( len(imgs))], horizontal = True)
    
            st.sidebar.image(imgs,caption=["image " + str(x) for x in range( len(imgs))])
            
            st.image(imgs[int(pick_img.split()[1])])
            st.dataframe(pd.DataFrame(battersc(listOfP[int(pick_img.split()[1])])[0][0].items()))
            st.dataframe(pd.DataFrame(battersc(listOfP[int(pick_img.split()[1])])[0][1].items()))
            st.dataframe(pd.DataFrame(battersc(listOfP[int(pick_img.split()[1])])[0][2].items()))

        else:
            st.image(imgs)
            st.dataframe(pd.DataFrame(battersc(listOfP[0])[0][0].items()))
            st.dataframe(pd.DataFrame(battersc(listOfP[0])[0][1].items()))
            st.dataframe(pd.DataFrame(battersc(listOfP[0])[0][2].items()))


if __name__ == '__main__':
    main()
