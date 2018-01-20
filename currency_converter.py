# -*- coding: utf-8 -*-
"""
Created on Tue May 24 21:07:22 2016

@author: Mateusz
"""

from tkinter import *
from tkinter.ttk import Frame,Label,Entry
import xml.etree.ElementTree as ET
from urllib.request import urlopen, URLError
from tkinter import messagebox
from datetime import *
import numpy as np

class CCurrencyConverter(Frame):
    '''CCurrencyConverte which has following methods: 
        __init__ initialize Curency Converter Window
        check_if_number checks is entry is correct
        xml_to_python take data from .xml from "www.nbp.pl/kursy/xml/a136z170717.xml" 
        callback_calc creates new labels
        error_in_entry1 shows error if user press CONVERT button without entering amount of money
        callback_swap swaps two currencies
        option_changed follows changes in choice of currencies
        initUI creates starting labels, option menu, buttons and entry box
        internet_connection_error shows info that there was connection error 
        other methods ...
    '''
    def __init__(self,parent):
        Frame.__init__(self,parent)
        
        self.parent=parent
        self.initUI()
        
    def check_if_number(self,event):
        if event.char in ('1','2','3','4','5','6','7','8','9','0','.','\b'):
            if event.char in ('1','2','3','4','5','6','7','8','9','0','\b'):
                return event.char
            elif self.entry1.get().count('.')>0:
                return 'break'
        else:
            return 'break'
			
    def xml_to_python(self):
     try:
        f=urlopen('http://www.nbp.pl/kursy/xml/a136z170717.xml')
        self.set_date()
        currency=ET.parse(f)
        root1=currency.getroot()
        currency_list=[]
        currency_cost_list=[]
        
        for position in root1.findall('pozycja'):
            name=position.find('nazwa_waluty').text
            shortcut=position.find('kod_waluty').text
            real_name=shortcut+'-'+name
            currency_list.append(real_name)
            currency_cost=position.find('kurs_sredni').text
            currency_cost=float(currency_cost.replace(',','.'))
            currency_cost=float("{0:.4f}".format(currency_cost))
            currency_cost_list.append(currency_cost)

        currency_cost_list.insert(0, int('1'))
        currency_list.insert(0,'PLN-zlotowka polska')
        self.currency_dict=dict(zip(currency_list, currency_cost_list))
        self.save_currency(self.currency_dict)
        
     except URLError as err: 
        self.internet_connection_error()
        self.currency_dict = dict(self.get_currency())     
     return self.currency_dict

    def callback_calc(self):
       if len(self.entry1.get())!=0:
        self.lbl4_1.config(text=self.entry1.get())
        self.lbl5_1.config(text=self.option_changed())
        self.result=self.option_changed()*float(self.entry1.get())
        self.result=float("{0:.4f}".format(self.result))
        self.lbl6_1.config(text=self.result)
       else:
           self.error_in_entry1()
         
    def clear_doc(self,file):
        f = open(file,'w')
        f.close()
        
    def set_date(self):
        self.clear_doc('date.txt')
        file = 'date.txt'
        with open(file,'w') as f:
            f.write(str(date.today())[:19])
            
    def get_date(self):
        file = 'date.txt'
        f = open(file,'r')
        date = ' ' + str(f.readline())
        return date
        
    def save_currency(self,data):
        file = 'currency.npy'
        self.clear_doc(file)
        np.save(file,data)
               
    def get_currency(self):
        file = 'currency.npy'
        currency = np.load(file).item()
        return currency
        
    def error_in_entry1(self):
        messagebox.showinfo("ERROR", "Try again!")
        
    def internet_connection_error(self):
        messagebox.showinfo("ERROR", "There was a problem with Internet connection. Exchange Rates from date " + str(self.get_date()))
        
    def callback_swap(self):
        temp=self.wal1.get()
        self.wal1.set(self.wal2.get())
        self.wal2.set(temp)
        
    def option_changed(self,*args):
        converter=self.currency_dict[self.wal1.get()]/self.currency_dict[self.wal2.get()] 
        converter=float("{0:.4f}".format(converter))
        return converter
        
    def initUI(self):
        self.parent.title("Currency converter ")
        self.pack(fill=BOTH)
        
        frame1=Frame(self)
        frame1.pack(fill=X)
        
        lbl1=Label(frame1, text="Amount of money which I have ")
        lbl1.pack(side=LEFT,padx=5,pady=15)
        
        self.entry1=Entry(frame1,justify='center')
        self.entry1.pack(fill=X,padx=5,pady=15)
        self.entry1.bind('<KeyPress>', self.check_if_number)

        frame2=Frame(self)
        frame2.pack(fill=X)
        
        lbl2=Label(frame2, text="Currency I have      \t")
        lbl2.pack(side=LEFT,padx=5,pady=15)
        
        self.wal1=StringVar(frame2)
        self.wal1.set('PLN-zlotowka polska')
        self.wal1.trace("w",self.option_changed)
        
        self.choices=self.xml_to_python()
        option=OptionMenu(frame2, self.wal1, *self.choices)
        option.pack(fill=X, padx=5, pady=15)
        
        frame_button=Frame(self)
        frame_button.pack()
        
        swap=Button(frame_button, text="Swap currencies ", command=self.callback_swap)
        swap.pack()
        
        frame3=Frame(self)
        frame3.pack(fill=X)
    
        lbl3=Label(frame3, text="Currency I want     \t")
        lbl3.pack(side=LEFT,padx=5,pady=15)
        
        self.wal2=StringVar(frame3)
        self.wal2.set('EUR-euro')
        
        option=OptionMenu(frame3,self. wal2, *self.choices)
        option.pack(fill=X, padx=5,pady=15)
        
        frame_button2=Frame(self)
        frame_button2.pack()

        calc=Button(frame_button2, text="Calculate", command=self.callback_calc)
        calc.pack()        
        
        self.frame4=Frame(self)
        self.frame4.pack(fill=X)
        
        lbl4=Label(self.frame4, text="The converter according to the average exchange rate ")
        lbl4.pack(pady=15)
        
        self.frame5=Frame(self)
        self.frame5.pack(fill=X)
        
        lbl4=Label(self.frame5, text="Money which I have     ")
        lbl4.pack(side=LEFT,padx=5,pady=5)
         
        self.lbl4_1=Label(self.frame5)
        self.lbl4_1.pack(padx=5,pady=5)       
                
        self.frame6=Frame(self)
        self.frame6.pack(fill=X)    
        
        lbl5=Label(self.frame6,text="Exchange rate                ")
        lbl5.pack(side=LEFT,padx=5,pady=5)
        
        self.lbl5_1=Label(self.frame6)
        self.lbl5_1.pack(padx=5,pady=5)
        
        self.frame7=Frame(self)
        self.frame7.pack(fill=X)
        
        lbl6=Label(self.frame7, text="Money which I will have")
        lbl6.pack(side=LEFT, padx=5, pady=5)
		
        self.lbl6_1=Label(self.frame7)
        self.lbl6_1.pack(padx=5,pady=5)
        
def main():
    root=Tk()
    root.geometry('350x400+0+10')
    root.resizable(0,0)
    CCurrencyConverter(root)
    root.mainloop()
    
if __name__=='__main__':
    main()
