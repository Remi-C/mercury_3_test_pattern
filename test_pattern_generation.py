# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:20:59 2015

@author: Remi
""" 

#def svg_add_rec_text( ):
"""this method adds a rectangle and a text """

def plot_speed_range(speed_range):
    import matplotlib.pyplot as plt
    plt.plot(speed_range)
    
def compute_speed_color_var(output_file_path, min_speed, max_speed):
    """given min max speed, compute 15 linearly sampled colors and speed"""
    speed_var = []
    speed_var.append(1000) # first rectangle is always fastest possible
    speed_range = range(0,15)
    for i in range(0,15):
        speed_range[i] = int((1-(speed_range[i])/14.0) *( max_speed-min_speed) + min_speed)
    #plot_speed_range(speed_range)
    speed_var+=speed_range
    plot_speed_range(speed_var)
    
    color_var = []
    color_var.append(255) # first rectangle is always fastest possible
    color_range = range(0,15)
    for i in range(0,15):
        color_range[i] = 240 - 10*i
    #plot_speed_range(speed_range)
    
    color_var+= color_range 
    return speed_var, color_var
    
def create_svg( output_file_path, min_speed, max_speed, power=100):
    """ main function, creates the svg file for a 16 colors mire
        speed is expressed between 1000 and 1 , power is expressed between 1 and 100.
        Lower mean slower/weaker"""
    import svgwrite
    document_width = 100
    document_height = 150
    document_start = (10, 10)
    document_unit = "mm"
    
    laser_line_width = 0.001
    laser_line_width_unit = "mm"
    
    laser_line = str(laser_line_width)+laser_line_width_unit
    
    rect_size = (20, 4)
    rec_spacing = 4
    text_style = "font-size:%fmm; font-family:%s" % (0.5, "Courier New") 
    dist_rect_text = (5,-1)
    
    viewBox_size = "0 0 {:d} {:d}".format(document_width,document_height)
    print viewBox_size 
    #create document object
    svg_document = svgwrite.Drawing(filename = output_file_path+'.svg',
                                size = (str(document_width)+document_unit
                                    , str(document_height)+document_unit)
                                , viewBox=(viewBox_size)) 
               
    #prepare speed variations :
    speed_var, color_var = compute_speed_color_var(output_file_path, min_speed, max_speed)
    for i in range(0,16):
    #creating the first rectangle, always 1000 speed, (255,0,0)
        insert_rec = (document_start[0], document_start[1]+i*(rect_size[1]+rec_spacing))
        rec = svg_document.rect(insert = insert_rec,
                                           size = rect_size,
                                           stroke_width = laser_line, 
                                           stroke = "rgb({:d},0,0)".format(color_var[i])  ,
                                           fill = "none")
    
        
        text1 = svg_document.text("{:d} / {:d}".format(int(speed_var[i]), power)
                                , insert=(insert_rec[0]+rect_size[0]+dist_rect_text[0], insert_rec[1]+rect_size[1]+dist_rect_text[1])
                                , fill="none"
                                , stroke_width=laser_line
                                , stroke="rgb(255,0,0)"
                                , style=text_style)
        
        svg_document.add(rec)
        svg_document.add(text1)
    
    #svg_document.add(svg_document.text("Hello World", insert = (210, 110) ) )
     
    
    svg_document.save()
    return color_var, speed_var, power

    
def create_laser_config_file(file_name, color_var, speed_var, power):
    """ creates a .ME3 old version laser cuter configuration file with color matching hte one used in the svg """
    
    laser_header = """[VERSION]
MACH_NAME=MercuryIII
VERSION=303
[OPTION]
MARK_MODE=1
RESOLUTION=600
PPI=0
MIRROR=0
INVERT=0
IMMEDIATE=0
USE_ACC_AREA=0
[PEN]
"""
    laser_footer = """[ADVANCE]
SCALING_X=0
SCALING_Y=0
BORDER_CHECK=0
BORDER_VERTICAL_MARGIN=10000
BORDER_HORIZONTAL_MARGIN=10000
POSITION=2
VECTOR_FUNCTION=0
BOTTOM_UP=0
CLUSTER_CHECK=1
CLUSTER_DIST=10000
NO_SKIP_WHITE=0
LOW_SPEED=1
USE_ORIGINAL=0
USE_smartcenter=0
POSX=0
POSY=0
BANDINGFREE=0
[PAPER]
FIELD_X=635000
FIELD_Y=458000
UNIT=0
DUAL_HEAD=0
ROTARY=0
RO_OFFS=0
RO_DIAM=50000
EXTEND=0
HONEYCOMB=0
[RASTER]
CONTRAST=0
HALFTONE=0
DITHER_MX=8
DITHER_PT=0
DITHER_ENHANCE=0
ERR_DIFFU_TYPE=0
[STAMP]
PITCH=300
LEVEL_1=0
LEVEL_2=6
LEVEL_3=13
LEVEL_4=19
LEVEL_5=26
LEVEL_6=33
LEVEL_7=39
LEVEL_8=46
LEVEL_9=54
LEVEL_10=59
LEVEL_11=66
LEVEL_12=73
LEVEL_13=79
LEVEL_14=86
LEVEL_15=93
LEVEL_16=100
[LASER_TUNING]
LEVEL1_1=100
LEVEL1_2=0
LEVEL1_3=0
LEVEL1_4=0
LEVEL1_5=20
LEVEL1_6=30
LEVEL1_7=30
LEVEL1_8=30
LEVEL1_9=30
LEVEL1_10=40
LEVEL1_11=50
LEVEL1_12=62
LEVEL1_13=70
LEVEL1_14=80
LEVEL1_15=90
LEVEL1_16=100
LEVEL1_17=100
LEVEL1_18=100
LEVEL1_19=100
LEVEL1_20=100
LEVEL1_21=100
LEVEL1_22=100
LEVEL1_23=100
LEVEL1_24=100
LEVEL1_25=100
LEVEL1_26=100
LEVEL1_27=100
LEVEL1_28=100
LEVEL1_29=100
LEVEL1_30=100
LEVEL1_31=100
LEVEL1_32=100
[IMAGE_TUNING]
FACTOR=0
[LANGUAGE]
LANGUAGE=French"""
    #opening the output file, overwritting it if necessary
    import codecs
    config_file = codecs.open(file_name+'.ME3', 'w', encoding = 'utf-8')
    config_file.write(laser_header)
    for i in range(0,16):
        color_header = """PEN{0:d}R={1:d}
PEN{0:d}G=0
PEN{0:d}B=0
PEN{0:d}POWER={2:d}
PEN{0:d}SPEED={3:d}
PEN{0:d}RAST=0
PEN{0:d}VECT=1
PEN{0:d}PPI=400
PEN{0:d}BLOWR=0
PEN{0:d}BLOWV=0
PEN{0:d}AUTOFOCUS=0
""".format(i+1,color_var[i], power, speed_var[i]) 
        config_file.write(color_header)
    config_file.write(laser_footer)
    config_file.close()
    return


def main():
    """main function, creating the svg file and the corresponding ME3"""
     
    min_speed = 100
    max_speed = 1000
    power=25
    
    file_name = None
    if file_name is None: 
        file_name = "mire_from_{:d}_to_{:d}_power_{:d}".format(max_speed, min_speed, power)
      
      
    color_var, speed_var , power= create_svg(file_name , min_speed, max_speed, power)
    create_laser_config_file(file_name, color_var, speed_var,power)
    
main()