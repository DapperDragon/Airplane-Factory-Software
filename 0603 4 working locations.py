#import modules
import datetime
import json
import io
import os
import easygui
import gc
import mmap
from pprint import *
import pickle

#REMINDERS
#REEEEEEEEEEEE
#Remove numbers from component selection in menu

#Date portion of batch code - Finds todays date
manufacturedate = datetime.date.today()

#Batch class
class Batch:
    def __init__(self, manufacturedate, numberofcomponents, BatchComponentType, BatchComponentSize, location, status):
        self.manufacturedate = manufacturedate
        #Takes todays date and formats it to day/month/year plus current batch number, assigns it to self.batchcode
        self.batchcode = manufacturedate.strftime('%d%m%y') + str("{:0>4d}".format(LastBatchNumber+1))
        self.BatchComponentType = BatchComponentType
        self.BatchComponentSize = BatchComponentSize
        self.location = location
        self.status = status
        self.complist = []
        self.numberofcomponents = numberofcomponents

    #returns self.batchcode and self.complist as strings because reasons
    def __repr__(self):
        return '%s, %s, )' % (self.batchcode, self.complist)


    #Generate batch codes
    def batchcodegenerator(self):

        #If Date on last index in JSON list does not equal the current date reset to 0001 of new date or increment batch number
        if DateCheck != manufacturedate.strftime('%d%m%y'):
            self.batchcode = manufacturedate.strftime('%d%m%y') + str("{:0>4s}".format('0001'))
            return self.batchcode
        else:
            return self.batchcode




#Component Class Code
class Component:
    def __init__(self, componentid, comptype, size, manufacturedate, parentbatch, status, location):
        self.componentid = componentid
        self.comptype = comptype
        self.size = size
        self.manufacturedate = manufacturedate
        self.parentbatch = parentbatch
        self.status = status
        self.location = location
        print('comp instance created')

    #return string versions of attributes
    def __repr__(self):
        return '%s, %s, %s, %s, %s' % (self.componentid, self.comptype, self.size, self.manufacturedate, self.parentbatch)



#Menus
def menu():
    #set global variables, could probs be removed
    global mylist
    global LastBatch
    global LastBatchNumber
    global DateCheck
    global currentcomponent

    location = 'Factory Floor - Warehouse unassigned'
    status = 'Manufactured - Unfinished'

    # Opens BatchIndex JSON file, finds batch numbers, assigns them to mylist, closes file afterwards
    with open('BatchIndex.json', 'r') as f:
        indata = json.load(f)
        mylist = indata['batches']
        count = 0
        while count < len(mylist):
            count = count + 1
            if count == len(mylist):
                LastBatch = mylist[-1]
                LastBatchNumber = int(LastBatch[6:])
        DateCheck = LastBatch[0:6]
        f.close()

    #Start of menu GUI loop
    loop = 0
    while loop == 0:
        quitoption = easygui.buttonbox('Welcome to the PPEC inventory system main menu \n \n Please choose an option: ', 'PPEC inventory system main menu', ('Create a new batch', 'List All Previous Batches', 'View Details of a Batch', 'View Details of a Component', 'Allocate Manufactured Stock', 'Quit'))



        #Create New Batch option
        if quitoption == "Create a new batch":
            currentbatch = Batch(manufacturedate, 0, '', '', location, status)
            easygui.msgbox((currentbatch.batchcodegenerator()) ,'Batch created')

            #Takes user input for number of components (lowerbound of 1 stops number of components from being 0),
            numbercomponents = easygui.integerbox('How many components are in this batch?', 'Number of Components' , lowerbound=1, upperbound=9999)


            #Component type choice
            componentchoice = easygui.buttonbox('Select component type: ', 'Component Choice', ('Winglet Strut','Door Handle','Rudder Pin', 'Quit'))

            #Winglet Strut Size options
            if componentchoice == 'Winglet Strut':
                size = easygui.buttonbox('Select Fitment Type: ', 'Strut Choice', ('A320 Series', 'A380 Series', 'Quit'))
                if size == 'Quit':
                    loop ==1
                    quit()

            #Door Handles are a universal fit, no size options required,
            elif componentchoice == 'Door Handle':
                size = 'N/A - Handles are a universal fit'

            #Rudder Pin size options
            elif componentchoice == 'Rudder Pin':
                size = easygui.buttonbox('Select Rudder Pin Size: ', 'Rudder Pin Size', ('10mm Diameter x 75mm Length', '12mm Diameter x 100mm length', '16mm Diameter x 1500mm Length', 'Quit'))
                if size == 'Quit':
                    loop ==1
                    quit()

            #Quit button
            elif componentchoice == 'Quit':
                loop ==1
                quit()


            #creates instances of component class
            #generates serial numbers (ie '-0001' to number of components entered by user)
            #adds to list component classes to batch class
            currentcomponent = 0000
            for i in range(numbercomponents):
                currentcomponent += 1
                compnumber = (str("-{:0>4d}".format(currentcomponent)))
                componentinstance = Component(compnumber, componentchoice, size, manufacturedate, currentbatch.batchcode, status, location)
                print(componentinstance)
                currentbatch.complist.append(currentbatch.batchcode + componentinstance.componentid)

                #Pickling COMPONENT
                f = open(str(currentbatch.batchcode + componentinstance.componentid) + '.pck', "wb")
                #ID
                pickle.dump(currentbatch.batchcode + componentinstance.componentid, f, pickle.HIGHEST_PROTOCOL)
                #Type
                pickle.dump(str(componentinstance.comptype), f, pickle.HIGHEST_PROTOCOL)
                #Size
                pickle.dump(componentinstance.size, f, pickle.HIGHEST_PROTOCOL)
                #Manufacture Date
                pickle.dump(componentinstance.manufacturedate, f, pickle.HIGHEST_PROTOCOL)
                #Batch code
                pickle.dump(componentinstance.parentbatch, f, pickle.HIGHEST_PROTOCOL)
                #Status
                pickle.dump(componentinstance.status, f, pickle.HIGHEST_PROTOCOL)
                #Location
                pickle.dump(componentinstance.location, f, pickle.HIGHEST_PROTOCOL)
                #Close Pickle File after we are done with it
                f.close()


            #Appends batch codes to list
            mylist.append(currentbatch.batchcode)
            #usednumbers = [currentbatch.batchcode]
            #Adds usernumbers list to a dictionary
            outdata = {'batches' : mylist}

            #Displays number of components added to the list - taken from user input
            easygui.msgbox('added ' + str(numbercomponents) + ' components to the batch')
            currentbatch.numberofcomponents = numbercomponents
            currentbatch.BatchComponentType = componentchoice
            currentbatch.BatchComponentSize = size





            printoption = easygui.buttonbox('Do you want to print batch information?', 'Print?', ('Yes', 'Quit'))
            if printoption == 'Yes':
                batchInfo = easygui.textbox(
                                "Batch number: " + currentbatch.batchcode,
                                'Batch Information',
                                'Manufacture Date: ' + str(currentbatch.batchcode[:6])
                                + '\n' + '\n' +
                                'Component Type: ' + componentchoice
                                + '\n' + '\n' +
                                'Component size: '
                                + size + '\n' + '\n' +
                                'Number of components in batch: ' + str(numbercomponents)
                                + '\n' + '\n' +
                                'Serial Number(s): ' + '\n' + str(currentbatch.complist)
                                + '\n' + '\n' +
                                'Status: ' + '\n' + str(currentbatch.status)
                                + '\n' + '\n' +
                                'Location: ' + '\n' + str(currentbatch.location)
                                )







            #Pickling batch class
            f = open(str(currentbatch.batchcode) + '.pck', "wb")
            #batchcode
            pickle.dump(currentbatch.batchcode, f, pickle.HIGHEST_PROTOCOL)
            #Manufacturedate
            pickle.dump(str(currentbatch.manufacturedate), f, pickle.HIGHEST_PROTOCOL)
            #ComponentType
            pickle.dump(currentbatch.BatchComponentType, f, pickle.HIGHEST_PROTOCOL)
            #ComponentSize
            pickle.dump(currentbatch.BatchComponentSize, f, pickle.HIGHEST_PROTOCOL)
            #Number of components
            pickle.dump(currentbatch.numberofcomponents, f, pickle.HIGHEST_PROTOCOL)
            #All Serial Numbers
            pickle.dump(currentbatch.complist, f, pickle.HIGHEST_PROTOCOL)
            #Location
            pickle.dump(currentbatch.location, f, pickle.HIGHEST_PROTOCOL)
            #Status
            pickle.dump(currentbatch.status, f, pickle.HIGHEST_PROTOCOL)
            #Close Pickle File after we are done with it
            f.close()

            correctoption = easygui.buttonbox('Was the information correct?', 'Was the information correct?', ('Yes', 'No'))
            if correctoption == 'Yes':
                #JSON SAVING
                # checks if the json file exists and is accessible, if not, creates the file to avoid crashing
                if os.path.isfile('BatchIndex.json') and os.access('BatchIndex.json', os.R_OK):
                    # checks if file exists
                    with open('BatchIndex.json', 'w') as outfile:
                        json.dump(outdata, outfile)
                               # if the file does not exist, creates it
                else:
                    with io.open(os.path.join('BatchIndex.json'), 'w') as outfile:
                        json.dump(outdata, outfile)

            elif correctoption == 'No':
               for file in os.listdir():
                   if file.startswith(currentbatch.batchcode) and file.endswith(".pck"):
                       os.remove(file)



            #Go again?
            quitoption = easygui.buttonbox('Return to main menu?', 'Main Menu', ('Main Menu', 'Quit'))
            if quitoption == 'Quit':
                loop == 1
                quit()
            else:
                menu()

        elif quitoption == 'Allocate Manufactured Stock':
            allocatechoice = easygui.enterbox('Enter a Batch Number', 'Batch Number')
            for file in os.listdir():
                if file.startswith(allocatechoice) and len(file) == 14:
                    f = open((str(allocatechoice) + '.pck'), "rb")
                    Pbatchcode = (pickle.load(f))
                    pManufacturedate = (pickle.load(f))
                    pComponentType = (pickle.load(f))
                    pComponentSize = (pickle.load(f))
                    pNumberComp = (pickle.load(f))
                    pSerialNumbers = (pickle.load(f))
                    pLocation = str((pickle.load(f)))
                    pStatus = (pickle.load(f))

                    if pLocation != 'Factory Floor - Warehouse unassigned':
                        easygui.msgbox('This batch has already been allocated to a warehouse!')
                        menu()
                    else:
                        warehousechoice = easygui.buttonbox('Select a warehouse', 'Select a warehouse', ('Paisley Warehouse', 'Dubai Warehouse', 'Cancel'))
                        if warehousechoice == 'Paisley Warehouse':
                            easygui.msgbox('This batch has now been allocated, and will be shipped to, the Paisley warehouse','wefwef')



                            f = open((str(allocatechoice) + '.pck'), "wb")
                            #batchcode
                            pickle.dump(Pbatchcode, f, pickle.HIGHEST_PROTOCOL)
                            #Manufacturedate
                            pickle.dump(pManufacturedate, f, pickle.HIGHEST_PROTOCOL)
                            #ComponentType
                            pickle.dump(pComponentType, f, pickle.HIGHEST_PROTOCOL)
                            #ComponentSize
                            pickle.dump(pComponentSize, f, pickle.HIGHEST_PROTOCOL)
                            #Number of components
                            pickle.dump(pNumberComp, f, pickle.HIGHEST_PROTOCOL)
                            #All Serial Numbers
                            pickle.dump(pSerialNumbers, f, pickle.HIGHEST_PROTOCOL)
                            #Location
                            pickle.dump(warehousechoice, f, pickle.HIGHEST_PROTOCOL)
                            #Status
                            pickle.dump(pStatus, f, pickle.HIGHEST_PROTOCOL)
                            #Close Pickle File after we are done with it
                            f.close()

                        if warehousechoice == 'Dubai Warehouse':
                            easygui.msgbox('This batch has now been allocated, and will be shipped to, the Paisley warehouse','wefwef')
                            f = open((str(allocatechoice) + '.pck'), "wb")
                            #batchcode
                            pickle.dump(Pbatchcode, f, pickle.HIGHEST_PROTOCOL)
                            #Manufacturedate
                            pickle.dump(pManufacturedate, f, pickle.HIGHEST_PROTOCOL)
                            #ComponentType
                            pickle.dump(pComponentType, f, pickle.HIGHEST_PROTOCOL)
                            #ComponentSize
                            pickle.dump(pComponentSize, f, pickle.HIGHEST_PROTOCOL)
                            #Number of components
                            pickle.dump(pNumberComp, f, pickle.HIGHEST_PROTOCOL)
                            #All Serial Numbers
                            pickle.dump(pSerialNumbers, f, pickle.HIGHEST_PROTOCOL)
                            #Location
                            pickle.dump(warehousechoice, f, pickle.HIGHEST_PROTOCOL)
                            #Status
                            pickle.dump(pStatus, f, pickle.HIGHEST_PROTOCOL)
                            #Close Pickle File after we are done with it
                            f.close()




        #I can't believe its another quit button
        elif quitoption == 'Quit':
            loop ==1
            quit()

        #List all previous batches option
        elif quitoption == 'List All Previous Batches':
            previousbatchfiles = []
            previousbatchesdisplay = []
            #find all .pck files that are 14 characters long, should only be batch pickle files
            for file in os.listdir():
                if file.endswith(".pck") and len(file) == 14:
                    f = open((str(file)), "rb")
                    easygui.textbox('Batch Number' + BatchChoice[0:10])



        #View details of a previous batch, finds all pck files, adds them to a list
        elif quitoption == 'View Details of a Batch':
            BatchChoice = easygui.enterbox('Enter a Batch Number', 'Batch Number')
            for file in os.listdir():
                if file.startswith(BatchChoice) and len(file) == 14:
                    f = open((str(BatchChoice) + '.pck'), "rb")
                    easygui.textbox('Details of Batch ' + BatchChoice[0:10],'Batch Details','Batch Number: ' + str(pickle.load(f)) + '\n \n' + 'Manufacture Date: ' + str(pickle.load(f)) + '\n \n' + 'Component Type: ' + str(pickle.load(f)) + '\n \n' + 'Component Size: ' + str(pickle.load(f)) + '\n \n' + 'Number of Components: ' + str(pickle.load(f)) + '\n \n' + 'All Serial Numbers: ' + str(pickle.load(f)) + '\n \n' + 'Location: ' + str(pickle.load(f)) + '\n \n' + 'Status: ' + str(pickle.load(f)))
            if BatchChoice == None:
                easygui.textbox('Error', 'Error')
                menu()

        #View details of a previous batch, finds all pck files, adds them to a list
        elif quitoption == 'View Details of a Component':
            PreviousComponentChoice = easygui.enterbox('Enter a Component Serial Number', 'Serial Number')
            for file in os.listdir():
                if file.startswith(PreviousComponentChoice) and len(file) == 19:
                    f = open((str(PreviousComponentChoice) + '.pck'), "rb")
                    easygui.textbox('Details of Component ' + PreviousComponentChoice,'Batch Details','Component Serial Number: ' + str(pickle.load(f)) + '\n \n' + 'Component Type: ' + str(pickle.load(f)) + '\n \n' + 'Component Size: ' + str(pickle.load(f)) + '\n \n' + 'Manufacture Date: ' + str(pickle.load(f)) + '\n \n' + 'Batch Number: ' + str(pickle.load(f)) + '\n \n' + 'Status: ' + str(pickle.load(f)) + '\n \n' + 'Location: ' + str(pickle.load(f)))
            if PreviousComponentChoice == None:
                easygui.textbox('Error', 'Error')
                menu()

mylist = []
LastBatch = 0
LastBatchNumber = 0
DateCheck = 0
currentcomponent = 0000
menu()
