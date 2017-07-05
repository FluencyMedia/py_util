# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 19:11:17 2016

@author: lstanevich
"""
import gspread


from oauth import get_credentials  # Test comment

credentials = get_credentials()
gc = gspread.authorize(credentials)

ws = gc.open_by_key('1gYfWH2YraNia61cCAPKhsGudApyES7CqTSydcPvFl0w').sheet1
