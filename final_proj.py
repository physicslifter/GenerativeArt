'''
File name: final.py
Author: Patrick LaChapelle
Class: Computer Science 131
        Summer quarter 2017
Date created: 07/25/2017
Date last modified: 08/16/2017
'''

print("Welcome to the most optimal and shophisticated computer program mankind has ever created.") #welcome user to program
print("What would you like to do?") #ask user what they want to do
print("please choose one:") #prompt user to choose type of function
print("Image alteration") #show first option of functions to run
print("recursive function") #show second option of functions to run
print("name drawing") #show third option of functions to run
print("nested loop grid") #show fourth option of functions to run
print("enter type of function:")
functiontype=input()

###Image alteration

if functiontype == "Image alteration":
    print("What type of task would you like to perform? (Please type: grayscale or pixel)") #Asks user to choose what alteration they want to perform
    cType=str(input())  # takes type of user input
    from PIL import Image, ImageFilter  #import Image from the downloadable Python Pillow module


    print("enter image file:") # prompts user to enter the image 
    myimage = input() #input image file

    try:
        picture_file = Image.open(myimage) #looks for exception in code
        im = picture_file.load()
    except:
        print('Invalid file')

    opicture_file = Image.open(myimage)

    print(picture_file.format, picture_file.size, picture_file.mode) #tell user the information about the picture file

    x_max=picture_file.size[0] #set variable x_max to the maximum x value of function
    y_max=picture_file.size[1] #set variable y_max to the maximum y value of function

    for y in range(0, y_max): #sets range value for y
        row = ""
    for x in range(0, x_max): #sets range value for x
        row = ""

        R, G, B = im[x, y] #set the RGB values

    if cType=='pixel': #set parameters for when input is 'pixel'
        print("Enter coordinates of desired pixel in x,y form") #prompt the user to input the coordinates of the desired pixel
        specific_pixel = [int(x) for x in input().split(',')] #enter the coordinates using the for loop
        x, y = specific_pixel #change coordinates to be equal to x and y values
        R, G, B = im[x, y] #gets RGB values from the 
        print("R,G,B values corresponding with this pixel are:") # explains to the user what they are about to recieve
        print(R, G, B) #prints the RGB value corresponding with the particular

        print("enter new R,G,B values") #prompts user to enter adjusted rgb values
        new_RGB = [int(x) for x in input().split(',')] #allows input for new rgb values

        a, b, c = new_RGB #changes the rgb values to three seperate values

        im[x, y] = (a, b, c) #inputs user's rgb values for the pixel

        picture_file.save("newimage.png") #saves the new pixel
        picture_file.show("newimage.png") #displays the altered image

    elif cType=='grayscale': #provides code for when the user chooses "grayscale" as the type of function that they would like to perform
        for a in range(picture_file.size[0]): #allows a to be any value in the range
            a=int()
        for b in range(picture_file.size[1]): #allows b to be any value in the range
            b=int()
        x,y= [a,b] #sets x and y values to a and b, which allows x and y to be any value in the range
        R, G, B, = im[x,y] #gets the rgb values of any pixel
        gray_rgb = int((R * 0.299 + G * 0.587 + B * 0.114)) #changes RGB to a value that will be on the gray scale ###note: this uses the weighted method, which is optimal for the human viewer
        im[x, y] = (gray_rgb) #inputs the grayscale values for all pixels in the file
        picture_file.save("newimage.png") #saves the file
        picture_file.show("newimage.png") #displays the file

    else: #gives code for if user enters something other than one of the desired inputs
        print("error: input unreadable, please enter pixel or grayscale")

### recursive function

elif functiontype == "recursive function": #gives what to do if the user enters recursive function as what they want to do

    import turtle #import the module turtle
    
    print("choose shape (spiral or flower)") #prompts user for  type of shape input
    shapetype = input() #takes input from user
    print("choose size") #prompts user for size input
    size1=int(input()) #takes input from user
    print("choose width of line") #prompts user for width input
    width1 = int(input()) ##takes input from user
    print("choose number of repititions") #prompts user for repitition input
    rep = int(input()) #takes input from user
    print("choose background color") #prompts user for background color input
    bg_color1=input() #takes input from user
    print("choose color of line") #prompts user for line color input
    line_color1=input() #takes input from user

    turtle.bgcolor(bg_color1) #sets background color using the input from the user
    turtle.pencolor(line_color1) #sets the color of the line using the input from the user


    turtle.speed(0) #sets turtle to draw the recursive function as quickly as possible

    def shape(length,n,_width):#sets the code that defines the spiral
        if n==0: #sets perameter for if there is no input for repititions
            turtle.forward(length) 
        elif n<1: #sets perameter for if there is less than one repitition
            print("error: cannot generate less than 1 repititions of recursive shape") 
        else: #sets perameter for what to do if all goes according to plan
            turtle.width(_width) #sets width to desired width
            turtle.fd(length/4) #moves forward 1/4 of the length
            turtle.rt(60) #turns right 60 degrees
            turtle.fd(length / 4) #moves forward 1/4 of the length
            turtle.rt(60) #turns right 60 degrees
            turtle.fd(length / 4) #moves forward 1/4 of the length
            turtle.rt(60) #turns right 60 degrees
            turtle.circle(length) #creates circle of the length input
            turtle.rt(180) #turns 180 degrees (reverses direction)
            turtle.circle(length) #creates another circle or radius length
            turtle.rt(182) #turn right 182 degrees
            shape(length*1.1,n-1,_width) #repeat function w/ altered inputs
            turtle.exitonclick() #exits turtle window on click
            return

    def spiral2(length2,n2,_width2): #defines spiral function
        if n2==0: #defines what to do if number of repititions is not entered
            turtle.forward(length2) # move forward 2
        elif n2<1: #defines what to do if less than 1 repition is entered
            print("error: cannot generate less than 1 repititions of a recursive shape") 
        else: #defines what to do if a desired input is entered
            turtle.width(_width2) #penwidth is 2
            turtle.circle(length2) #create circle w/ radius double the length of length input
            turtle.rt(45) #turn right 45 degrees
            turtle.circle(length2) #create circle w/ radius twice of the length input
            turtle.rt(45) #turn right 45 degrees
            turtle.circle(length2) #create circle w/ radius twice of the length input
            turtle.rt(45) #turn right 45 degrees
            turtle.circle(length2) #create circle w/ radius twice of the length input
            turtle.rt(45) #turn right 45 degrees
            turtle.circle(length2) #create circle w/ radius twice of the length input
            turtle.rt(45) #turn right 45 degrees
            turtle.circle(length2) #create circle w/ radius twice of the length input
            turtle.rt(45) #turn right 45 degrees
            turtle.circle(length2) #create circle w/ radius twice of the length input
            turtle.rt(45) #turn right 45 degrees
            turtle.circle(length2) #create circle w/ radius twice of the length input
            turtle.rt(45) #turn right 45 degrees
            spiral2(length2*1.1,n2-1,_width2) #repeat function w/ altered inputs
            turtle.exitonclick() #exits turtle window on click
            return

    if shapetype=="spiral": #if spiral is the desired shape follow this
        print(shape(size1,rep,width1))
    elif shapetype == "flower": #if flower is the desired shape follow this
        print(spiral2(size1,rep,width1))
    else: #provides code for what to do if something other than one of the desired inputs is entered
        print("error: shape type not available. Please choose either spiral or flower") #if the input for the desired shape typeis anything other than spiral or flower, print this error statement
    turtle.exitonclick() #allows user to use a click of a mouse as a way to exit out of the turtle screen
              
### Nested Loop function

elif functiontype == "nested loop grid": #describes what to do if user enters nested loop grid as the type of function they would like to perform
    print("Enter height") #prompt user to enter the height of their desired 2d grid
    height=int(input()) #user enters their desired height
    print("enter width") #prompt user to enter the width of the desired 2d grid
    width=int(input()) #user enters the desired width

    grid = [[n]*height for n in range(width)] #defines grid of desired width and height
    
    print(grid) #display the grid

#### name drawing function

elif functiontype == "name drawing": #provides code for what to do if the user inputs name drawing as what they would like to perform

    print("enter name: ") #prompt user to enter their name or string
    name=input() #have the user input their string 
    print("enter line color") #prompt the user to enter their desired line color
    linecolor=input() #have the user enter their line color as input
    print("enter background color") #prompt the user to enter their desired background color
    bg_color = input() #have the user enter their line color as input
    print("enter width of line:") #prompt the user to enter their desired line width
    width = int(input()) #have the user enter the width as input

    name_list = list(name) #split out the string input as individual characters
    print (name_list) #print the individual characters

    import turtle #import the module turtle
    turtle.speed(0) #set the turtle speed to the max speed
    turtle.setworldcoordinates(0,-100,1000,200) #set the coordinates of the window
    turtle.color(linecolor) #set the color of the line to the input linecolor
    turtle.bgcolor(bg_color) #set the background color to the users input of the desired background color
    turtle.width(width) #set the width of the line to the users input for width

    for i in name_list: #turns each individual character into variable i
        character=ord(i) #turns the individual character into the integer number assigned to that variable
        if character == 97: #displays created code for 'a'
            turtle.pu()
            turtle.fd(30)
            turtle.pd()
            turtle.circle(30)
            turtle.pu()
            turtle.forward(30)
            turtle.left(90)
            turtle.forward(60)
            turtle.pd()
            turtle.right(180)
            turtle.forward(60)
            turtle.pu()
            turtle.lt(90)
            turtle.fd(20)
            turtle.pd()
        elif character == 98: #displays created code for 'b'
            turtle.left(90)
            turtle.forward(100)
            turtle.left(180)
            turtle.forward(100)
            turtle.left(90)
            turtle.pu()
            turtle.forward(60)
            turtle.left(90)
            turtle.forward(30)
            turtle.pd()
            turtle.circle(30)
            turtle.pu()
            turtle.right(180)
            turtle.forward(30)
            turtle.left(90)
            turtle.forward(20)
            turtle.pd()
        elif character == 99: #displays created code for 'c'
            turtle.pu()
            turtle.forward(40)
            turtle.left(90)
            turtle.forward(60)
            turtle.left(90)
            turtle.pd()
            turtle.forward(10)
            turtle.circle(30, 180)
            turtle.forward(10)
            turtle.pu()
            turtle.forward(20)
            turtle.pd()
        elif character == 100: #displays created code for 'd'
            turtle.pu()
            turtle.forward(30)
            turtle.pd()
            turtle.circle(30)
            turtle.pu()
            turtle.forward(30)
            turtle.left(90)
            turtle.pd()
            turtle.forward(100)
            turtle.left(180)
            turtle.forward(100)
            turtle.pu()
            turtle.left(90)
            turtle.forward(20)
            turtle.pd()
        elif character == 101: #displays created code for 'e'
            turtle.left(90)
            turtle.forward(30)
            turtle.right(90)
            turtle.forward(30)
            turtle.right(90)
            turtle.forward(15)
            turtle.right(90)
            turtle.forward(30)
            turtle.left(90)
            turtle.forward(15)
            turtle.left(90)
            turtle.forward(30)
            turtle.pu()
            turtle.forward(20)
            turtle.pd()
        elif character == 102: #displays created code for 'f'
            turtle.pu()
            turtle.forward(20)
            turtle.pd()
            turtle.left(90)
            turtle.forward(70)
            turtle.pu()
            turtle.right(90)
            turtle.forward(60)
            turtle.left(90)
            turtle.pd()
            turtle.circle(30, 180)
            turtle.forward(20)
            turtle.right(90)
            turtle.forward(20)
            turtle.right(180)
            turtle.forward(40)
            turtle.pu()
            turtle.right(90)
            turtle.forward(50)
            turtle.left(90)
            turtle.forward(30)
            turtle.pd()
        elif character == 103: #displays created code for 'g'
            turtle.pu()
            turtle.forward(30)
            turtle.pd()
            turtle.circle(30)
            turtle.pu()
            turtle.left(90)
            turtle.forward(60)
            turtle.right(90)
            turtle.forward(30)
            turtle.right(90)
            turtle.pd()
            turtle.forward(80)
            turtle.pu()
            turtle.right(90)
            turtle.forward(60)
            turtle.left(90)
            turtle.pd()
            turtle.circle(30, 180)
            turtle.pu()
            turtle.right(90)
            turtle.forward(20)
            turtle.left(90)
            turtle.forward(20)
            turtle.right(90)
            turtle.pd()
        elif character == 104: #displays created code for 'h'
            turtle.left(90)
            turtle.forward(100)
            turtle.right(90)
            turtle.pu()
            turtle.forward(60)
            turtle.right(90)
            turtle.forward(100)
            turtle.right(180)
            turtle.pd()
            turtle.forward(30)
            turtle.circle(30, 180)
            turtle.pu()
            turtle.forward(30)
            turtle.left(90)
            turtle.forward(80)
            turtle.pd()
        elif character == 105: #displays created code for 'i'
            turtle.left(90)
            turtle.forward(45)
            turtle.pu()
            turtle.forward(15)
            turtle.right(90)
            turtle.pd()
            turtle.circle(5)
            turtle.pu()
            turtle.right(90)
            turtle.forward(60)
            turtle.left(90)
            turtle.forward(20)
            turtle.pd()
        elif character == 106: #displays created code for 'j'
            turtle.pu()
            turtle.rt(90)
            turtle.forward(20)
            turtle.pd()
            turtle.circle(30, 180)
            turtle.forward(60)
            turtle.pu()
            turtle.forward(15)
            turtle.right(90)
            turtle.pd()
            turtle.circle(5)
            turtle.right(90)
            turtle.pu()
            turtle.forward(55)
            turtle.left(90)
            turtle.forward(25)
            turtle.pd()
        elif character == 107: #displays created code for 'k'
            turtle.left(90)
            turtle.forward(100)
            turtle.right(180)
            turtle.forward(70)
            turtle.left(135)
            turtle.forward((2 ** (-0.5)) * 60)
            turtle.right(180)
            turtle.forward((2 ** (-0.5)) * 60)
            turtle.left(90)
            turtle.forward((2 ** (-0.5)) * 60)
            turtle.left(45)
            turtle.pu()
            turtle.forward(20)
            turtle.pd()
        elif character == 108: #displays created code for 'l'
            turtle.left(90)
            turtle.forward(100)
            turtle.pu()
            turtle.right(90)
            turtle.forward(20)
            turtle.right(90)
            turtle.forward(100)
            turtle.left(90)
            turtle.pd()
        elif character == 109: #displays created code for 'm'
            turtle.left(90)
            turtle.forward(50)
            turtle.right(180)
            turtle.forward(15)
            turtle.left(90)
            turtle.pu()
            turtle.forward(40)
            turtle.left(90)
            turtle.pd()
            turtle.circle(10, 180)
            turtle.forward(13)
            turtle.right(180)
            turtle.forward(13)
            turtle.circle(10, 180)
            turtle.pu()
            turtle.right(270)
            turtle.forward(40)
            turtle.right(90)
            turtle.pd()
            turtle.forward(35)
            turtle.pu()
            turtle.left(90)
            turtle.forward(20)
            turtle.pd()
        elif character == 110: #displays created code for 'n'
            turtle.left(90)
            turtle.forward(50)
            turtle.right(180)
            turtle.forward(15)
            turtle.left(90)
            turtle.pu()
            turtle.forward(30)
            turtle.left(90)
            turtle.pd()
            turtle.circle(15, 180)
            turtle.left(90)
            turtle.pu()
            turtle.forward(30)
            turtle.right(90)
            turtle.pd()
            turtle.forward(35)
            turtle.pu()
            turtle.lt(90)
            turtle.forward(20)
            turtle.pd()
        elif character == 111: #displays created code for 'o'
            turtle.pu()
            turtle.forward(40)
            turtle.pd()
            turtle.circle(40)
            turtle.pu()
            turtle.forward(60)
            turtle.pd()
        elif character == 112: #displays created code for 'p'
            turtle.pu()
            turtle.fd(30)
            turtle.pd()
            turtle.circle(30)
            turtle.pu()
            turtle.bk(30)
            turtle.lt(90)
            turtle.fd(60)
            turtle.pd()
            turtle.bk(100)
            turtle.rt(90)
            turtle.pu()
            turtle.fd(80)
            turtle.lt(90)
            turtle.fd(40)
            turtle.rt(90)
            turtle.pd()
        elif character == 113: #displays created code for 'q'
            turtle.pu()
            turtle.fd(30)
            turtle.pd()
            turtle.circle(30)
            turtle.pu()
            turtle.fd(30)
            turtle.lt(90)
            turtle.fd(50)
            turtle.pd()
            turtle.bk(100)
            turtle.pu()
            turtle.fd(10)
            turtle.rt(90)
            turtle.fd(10)
            turtle.lt(180)
            turtle.pd()
            turtle.circle(10, 90)
            turtle.pu()
            turtle.lt(90)
            turtle.fd(20)
            turtle.lt(90)
            turtle.fd(50)
            turtle.rt(90)
            turtle.pd()
        elif character == 114: #displays created code for 'r'
            turtle.lt(90)
            turtle.fd(50)
            turtle.bk(20)
            turtle.rt(90)
            turtle.pu()
            turtle.fd(40)
            turtle.lt(90)
            turtle.pd()
            turtle.circle(20,180)
            turtle.lt(90)
            turtle.pu()
            turtle.fd(40)
            turtle.rt(90)
            turtle.pd()
            turtle.fd(10)
            turtle.pu()
            turtle.fd(20)
            turtle.lt(90)
            turtle.fd(20)
            turtle.pd()
        elif character == 115: #displays created code for 's'
            turtle.fd(30)
            turtle.circle(20, 90)
            turtle.fd(5)
            turtle.circle(20, 90)
            turtle.fd(10)
            turtle.pu()
            turtle.rt(90)
            turtle.fd(45)
            turtle.lt(90)
            turtle.pd()
            turtle.bk(30)
            turtle.fd(30)
            turtle.circle(20, 90)
            turtle.fd(5)
            turtle.circle(20, 90)
            turtle.pu()
            turtle.fd(50)
            turtle.rt(90)
            turtle.fd(40)
            turtle.lt(90)
            turtle.pd()
        elif character == 116: #displays created code for 't'
            turtle.pu()
            turtle.fd(25)
            turtle.lt(90)
            turtle.pd()
            turtle.fd(100)
            turtle.bk(50)
            turtle.lt(90)
            turtle.fd(25)
            turtle.bk(50)
            turtle.pu()
            turtle.bk(20)
            turtle.lt(90)
            turtle.fd(50)
            turtle.lt(90)
            turtle.pd()
        elif character == 117: #displays created code for 'u'
            turtle.pu()
            turtle.fd(40)
            turtle.lt(90)
            turtle.pd()
            turtle.fd(50)
            turtle.lt(90)
            turtle.pu()
            turtle.fd(40)
            turtle.pd()
            turtle.lt(90)
            turtle.fd(30)
            turtle.circle(20, 180)
            turtle.pu()
            turtle.bk(20)
            turtle.rt(90)
            turtle.fd(20)
            turtle.pd()
        elif character == 118: #displays created code for 'v'
            turtle.pu()
            turtle.lt(90)
            turtle.fd(40)
            turtle.pd()
            turtle.rt(135)
            turtle.fd(3200 ** 0.5)
            turtle.lt(90)
            turtle.fd(3200 ** 0.5)
            turtle.rt(45)
            turtle.pu()
            turtle.fd(20)
            turtle.rt(90)
            turtle.fd(40)
            turtle.lt(90)
            turtle.pd()
        elif character == 119: #displays created code for 'w'
            turtle.pu()
            turtle.lt(90)
            turtle.fd(50)
            turtle.pd()
            turtle.bk(35)
            turtle.rt(180)
            turtle.circle(15, 180)
            turtle.fd(10)
            turtle.bk(10)
            turtle.rt(180)
            turtle.circle(15, 180)
            turtle.fd(35)
            turtle.pu()
            turtle.bk(50)
            turtle.rt(90)
            turtle.fd(20)
            turtle.pd()
        elif character == 120: #displays created code for 'x'
            turtle.left(45)
            turtle.fd(5000 ** 0.5)
            turtle.left(135)
            turtle.pu()
            turtle.fd(50)
            turtle.lt(135)
            turtle.pd()
            turtle.fd(5000 ** 0.5)
            turtle.lt(45)
            turtle.pu()
            turtle.fd(20)
            turtle.pd()
        elif character == 121: #displays created code for 'y'
            turtle.left(90)
            turtle.pu()
            turtle.fd(50)
            turtle.pd()
            turtle.bk(30)
            turtle.rt(180)
            turtle.circle(20, 180)
            turtle.fd(30)
            turtle.bk(80)
            turtle.lt(90)
            turtle.pu()
            turtle.fd(40)
            turtle.lt(90)
            turtle.pd()
            turtle.circle(20, 180)
            turtle.fd(30)
            turtle.rt(90)
            turtle.pu()
            turtle.fd(20)
            turtle.pd()
        elif character == 122: #displays created code for 'z'
            turtle.fd(50)
            turtle.lt(90)
            turtle.pu()
            turtle.fd(50)
            turtle.lt(90)
            turtle.pd()
            turtle.fd(50)
            turtle.bk(50)
            turtle.lt(45)
            turtle.fd(5000 ** 0.5)
            turtle.lt(135)
            turtle.fd(50)
            turtle.pu()
            turtle.fd(20)
            turtle.pd()
        elif character == 32: #displays created code for a space in the string
            turtle.pu()
            turtle.fd(50)
            turtle.pd()
        else: #creates code for what to do if anything other than a lowercase number or space is entered into the string
            print("unable to read this character, please enter a lowercase alphabetical letter") #gives error statement to print in this scenario
    turtle.exitonclick() #allows the program to exit out of the turtle screen with a click from the user
else: #provides code for what to do if something other than one of the four desired inputs is entered at the beginning of the function
   print("error: unreadable input. Please enter one of the specified inputs at the beginning of the function. Please check spelling and capital/lowercase letters") #provides and prints error code 


print ("THANKYOU, HAVE A NICE DAY") #thank user for using program
print('G')
print('O')
print('O')
print('D')
print('B')
print('Y')
print('E')
print