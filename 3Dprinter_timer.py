# -*- coding: utf-8 -*-
"""
3D printer time calculator
Calculates total time to print a component
"""

def read_gcode(gcode_name,ac,amax,Vj,default_speed):
    gcode_file = open(gcode_name,'r')
    
    flag_relative = 0 # G90 -> absolute printing    
    
    coord_old = [0.0, 0.0, 0.0]
    coord_new = [0.0, 0.0, 0.0]
    
    length_total = 0.0
    total_time = 0.0
    nfil = 0
    
    Vprint = default_speed

    for line in gcode_file:
        
        #check if the printing speed is changed
        if line.find('F') >= 0:
            str_now = line.split('F')
            str_now = str_now[-1]
            
            flag_speed = -1
            cont_speed = -1
            while flag_speed == -1:
                cont_speed += 1
                str_i = str_now[cont_speed]
                if str_i == ' ' or str_i == '\n' or str_i == ';' or str_i == r'\\':
                    flag_speed = 1
                    
            Vprint = float(str_now[0:cont_speed])/60.0 #transforming to mm/s
                
#            str_now = str_now.replace('\n','')
#            str_now = str_now.replace(';','')
#            Vprint = float(str_now)/60.0 #transforming to mm/s
            
        if line == 'G90':
            flag_relative = 0
        elif line == 'G91':
            flag_relative = 1 # G91 -> absolute printing
            
        elif len(line)>= 2:
            aux_line = line[0:2] # reads the first 2 characters
            
            if aux_line == 'G1': #it means there is movement
                print('Reading movement')
                coord_new = define_movement(line, coord_old)
                length_now = calculate_L(coord_new,coord_old,flag_relative)
                time_i = time_calculate(length_now,ac,amax,Vj,Vprint)
                
                length_total += length_now
                total_time += time_i
                nfil += 1
            
    gcode_file.close()
    return length_total, nfil, total_time
#------------------------------------------------------------------------------
#Function that reads the new coordinates
def define_movement(str_move, coord_old):
    str_move = str_move.split(' ')
    
    str_move[-1] = str_move[-1].replace('\n','')
    
    coord_new = [coord_old[0], coord_old[1], coord_old[2]]
    
    for str_i in str_move:
        if str_i[0] == 'X': # nozzle moves in the x direction
            coord_new[0] = float(str_i[1::]) #assembly coordinate
        elif str_i[0] == 'Y': # nozzle moves in the y direction
            coord_new[1] = float(str_i[1::]) #assembly coordinate
        elif str_i[0] == 'Z': # nozzle moves in the z direction
            coord_new[2]= float(str_i[1::]) #assembly coordinate
            
    return coord_new
#------------------------------------------------------------------------------
def calculate_L(coord_new,coord_old,flag_relative):
    if flag_relative == 0:
        trick = 1.0
    else:
        trick = 0.0 #if it relative, the old coordinates are not taken into
        #account to calculate the length L
        
    aux_sum = 0.0
    for (pold,pnew) in zip(coord_old,coord_new):
        aux_sum = aux_sum + (pold*trick - pnew)**2
    L = aux_sum**0.5
    
    return L          
#------------------------------------------------------------------------------
def time_calculate(L,ac,amax,Vj,Vprint):
    if Vprint <= Vj:
        time = L/Vprint
    else:
        time = L/Vprint + Vprint/ac - 2.0*Vj/ac + Vj**2/(Vprint*ac)
        if time < 0.0:
            time = L/Vprint + Vprint/amax - 2.0*Vj/amax + Vj**2/(Vprint*amax)
            if time < 0.0:
                print('Errorx001: it is impossible to reach the desired printing speed')
                   
    return time
#------------------------------------------------------------------------------
# Main function    
def main():
    L_total, nfil, total_time = read_gcode(gcode_name,ac,amax,Vj,default_speed)
    
    print('Total travel %f (mm)' %(L_total))
    print('Total number of filaments = %d' %(nfil))
    print('Total time to print = %f [min]' %(total_time/60.0))
#------------------------------------------------------------------------------
amax = 2000.0 #maximum nozzle acceleration -mm/s^2
ac = 1200.0 #default nozzle acceleration -mm/s^2

Vj = 40.0 # nozzle jerk speed - mm/s

default_speed = 40.0 #default nozzle speed (before you set the printing speed)

gcode_name = 'ED_V16_0325_RE.gcode'
main()
            
    
    