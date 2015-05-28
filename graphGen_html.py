#Graphic Generator - version 0.0  -  05.26.2015
#
#The Graphic Generator creates a bullet type graphic simulating the evolution
#in a temperature range fed as input data for the generator.
#The output of is an html document which can be seen on the visor.
#
#INTRUCTIONS:
#Set the initial temperature [temp_i]
#Set the final temperature [temp_f]
#Set the time constant (by default tau = 120s) [tau]
#
#NOTE: The simulator has a set value of 10s as the basic time step
#this will be the minimum constant time. A First-Order model is used
#to generate the graphic.
#
h='''
***********************************************************
***********************************************************
Temperature Simulator - Graphic Generator  Version 0.0
Python version 2.7.9
Developed by: Alejandro Cadena
***********************************************************
***********************************************************
'''
#Module Import - Section
import math

#Temperature Simulator - Functions Section
#*******************************************************************
def psOng (ti,tf):
    tdiff=tf-ti
    if tdiff>0:
        return 400,True #Initial position for 1st graphic point [px]
    elif tdiff<0:
        return 0,False #Initial position for 1st graphic point [px]
    else:
        return 400,True

def fstOrd (xn,xn_1,rate): #First-Order Model
    y=xn_1+(rate*(xn-xn_1))          
    return y
                 
def pGen (temp,step,xbase,ybase,sen): #Graphic-Point Calculation
    if sen:
        top=xbase-math.ceil(temp)
    else:
        top=xbase+math.ceil(temp)

    point=[temp,step,top,ybase]

    return point

def simulator (ti,tf,tb,tau): #Temperature Simulator
    itop,uOd = psOng(ti,tf)
    ilef=50
    stp=1
    sim=[]
    punto=[]
    exr=tb/tau
    while stp<120:
        if stp<4:
            tn_1=ti
            tn=tn_1
        else:
            tn=tf

        temp=fstOrd(tn,tn_1,exr)
        tn_1=temp
        punto=pGen(temp,stp,itop,ilef,uOd)
        #print punto
        sim.append(punto)
        itop=itop-10
        ilef=ilef+10
        stp=stp+1
    
    return sim

#Graphic Generator HTML Format - Functions Section
#*******************************************************************
def get_html_open():
    doc_ini='''
<!DOCTYPE html>
<html>
<head>
    <title>Graphic - Bullet Type</title>
    <style>
      body {
        max-width: 1330px;
        max-height: 490px;
        font: 100% Tahoma;
        background-color: #000000
        }
      div {
        height : 10px;
        width : 10px;
        border-radius: 25px;
        padding: 0px;
        margin: 0px;

        }
        ul {
          /*position: relative;*/
          font-family: Tahoma;
          overflow: auto;
          padding-left: 360px;
          padding-right: 300px;
          margin: 1px;
        }
        li {
            float: left;
            text-align: center;
            vertical-align: center;
            width: 150px;
            height: 25px;
            background-color: #0000FF;
            color: white;
            padding-top: 2px;
            padding-left: 0px;
            padding-right: 0px;
            border-radius: 5px;
            margin: 1px;
            list-style-type: none;  
        }
      .punto {
        background-color: #FF9900; /*#00FFCC magenta #CC00CC morado #FF9900 naranja*/
        }
    </style>

    <script>
      function funGetData(n) {
        var temp
        var stpe
        var Tpos
        var Spos

        Tpos = "Temp"+ n.toString();
        Spos = "Step"+ n.toString();

        temp = document.getElementById(Tpos).innerHTML;
        stpe = document.getElementById(Spos).innerHTML;


         document.getElementById("datT").innerHTML = temp;
         document.getElementById("datS").innerHTML = stpe;
        }
    </script>
</head>

<body>

            <ul class="menu">
		            <li>Temperature:</li>
                <li id="datT"></li>
		            <li>Step:</li>
                <li id="datS"></li>           
            </ul>

            <hr>'''
    return doc_ini

def get_html_close():
    doc_fin='''
</body>

</html>'''
    return doc_fin

def graph_point_html(Tsim,pace,pX,pY):
    bs_1='''
<div class="punto" style="position: relative;top: '''+str(pX)+'px;left: '+str(pY)+'px" onclick="funGetData('+str(pace)+')">'
    bs_2='''
	<p id="Temp'''+str(pace)+'" style="display:none">'+str(Tsim)+'</p>'
    bs_3='''
	<p id="Step'''+str(pace)+'" style="display:none">'+str(pace)+'</p>'
    bs_4='''
</div>'''

    full=bs_1+bs_2+bs_3+bs_4
    return full

def getPoint_html(point):
    temp=point[0]
    step=point[1]
    top=point[2]
    left=point[3]
    return graph_point_html(temp,step,top,left)

def gPoints_html(sim_points):
    html_gpts=""
    for spoint in sim_points:
        point_html=getPoint_html(spoint)
        html_gpts=html_gpts+point_html
    return html_gpts

def get_graphic_html(lst_simul):
    HTML_1=get_html_open()
    HTML_2=gPoints_html(lst_simul)
    HTML_3=get_html_close()
    HTML_Doc=HTML_1+HTML_2+HTML_3
    return HTML_Doc

#Main Program - Section
#*******************************************************************
print h
try:
    temp_i=int(raw_input("Set the initial temperature value: "))
except ValueError:
    print "Invalid data..."
    temp_i=0
print 'Initial Temperature = ',temp_i," 'C"
try:
    temp_f=int(raw_input("Set the final temperature value: "))
except ValueError:
    print "Invalid data..."
    temp_f=0
print 'Final Temperature = ',temp_f," 'C"
keysel=raw_input("Do you want to use the Time Constant default value? (Y/N)")
if keysel =='Y' or keysel=='y':
    tau=120
elif keysel=='N' or keysel=='n':
    try:
        tau=int(raw_input("Set the constant time value: "))
    except ValueError:
        print "Invalid data..."
        tau=10
    #Data validation - Time constant no less that basic time step
    if tau<10:
        print 'Time Constant cannot be less than simulation step....'
        tau=10
else:
    tau=120
print 'Time Constant = ',tau,' seconds'
print '**************************************************************'
print '**************************************************************'
data=simulator(temp_i,temp_f,10.,tau)
gfica=get_graphic_html(data)
try:
    fhtml=open('GraphBullet.html','w')
    fhtml.write(gfica)
    fhtml.close()
    print 'Your Simulation has been saved in the HTML document "GraphBullet.html"'
    print 'To see the graphic, please load the HTML document in the Graphic-Visor'
except:
    print 'Unexpected Error has been happened, Graphic HTML document was not created!!!'





