import numpy as np
import cv2
import time
#import ROOT
#from ROOT import TFile, TMatrixD

def draw_grid(image,grid):
    height,width=image.shape[:2]
    for i in range(grid[0]):
        for j in range(grid[1]):
            cv2.rectangle(image,(i*width//grid[0],j*height//grid[1]),((i+1)*width//grid[0]+1,(j+1)*height//grid[1]),(255,255,255),1)

def check_light(gray,grid):
    lux_matrix=np.zeros((grid[1],grid[0]))
    height,width=gray.shape[:2]
    cell_height=height//grid[1]
    cell_width=width//grid[0]
    for i in range(grid[0]):
        for j in range(grid[1]):
            sum=0.0
            count=0
            for y in range(cell_height):
                for x in range(cell_width):
                    if y+j*cell_height<height and x+i*cell_width<width:
                        sum+=gray[y+j*cell_height][x+i*cell_width]
                        count+=1
            if count!=0:
                lux_matrix[j][i]=sum/count
            else:
                lux_matrix[j][i]=0
    return lux_matrix
    
def draw_light_with_lim(image,lux_matrix,grid,lim=2):
    height,width=image.shape[:2]
    cell_height=height//grid[1]
    cell_width=width//grid[0]
    light_matrix=np.empty((grid[1],grid[0]),dtype="bool")
    for i in range(grid[0]):
        for j in range(grid[1]):
            if lux_matrix[j][i]>lim:
                cv2.rectangle(image,(i*width//grid[0],j*height//grid[1]),((i+1)*width//grid[0]+1,(j+1)*height//grid[1]),(0,0,255),2)
                light_matrix[j][i]=True
            else:
                light_matrix[j][i]=False
    return light_matrix
    
def draw_light_with_difference(image,lux_matrix,old_lux_matrix,grid,diff_lim=5):
    height,width=image.shape[:2]
    cell_height=height//grid[1]
    cell_width=width//grid[0]
    light_matrix=np.empty((grid[1],grid[0]),dtype="bool")
    for i in range(grid[0]):
        for j in range(grid[1]):
            if lux_matrix[j][i]-old_lux_matrix[j][i]>diff_lim:
                cv2.rectangle(image,(i*width//grid[0],j*height//grid[1]),((i+1)*width//grid[0]+1,(j+1)*height//grid[1]),(0,0,255),2)
                light_matrix[j][i]=True
            else:
                light_matrix[j][i]=False
    return light_matrix
                
def check_if_muon(light_matrix):
    muon_frame_count=0
    for x in range(0,grid[0]):
        lumen=0
        for y in range(0,grid[1]):
            if light_matrix[y][x]:
                lumen+=1
        if lumen>=2:
            muon_frame_count+=1
    return muon_frame_count

#file=TFile("datas.root","RECREATE")

interesting_frame_count=1

with open("datas.txt","w") as file:
    

    muon_count=0
    grid=(10,14)
    cap=cv2.VideoCapture("muons_final.mp4")
    old_lux_matrix=np.zeros((grid[1],grid[0]))
    frame_count=0
    while cap.isOpened():
        frame_count+=1
        ret,frame=cap.read()
        if not ret:
            break

        frame=cv2.resize(frame,(int(frame.shape[1]/3),int(frame.shape[0]/3)))

        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        draw_grid(frame,grid)
        
        lux_matrix=check_light(gray,grid)
        
        #light_matrix=draw_light_with_lim(frame,lux_matrix,grid)
        light_matrix=draw_light_with_difference(frame,lux_matrix,old_lux_matrix,grid)
        
        '''light_matrix_for_root=TMatrixD(light_matrix.shape[0],light_matrix.shape[1])
        for i in range(light_matrix.shape[0]):
            for j in range(light_matrix.shape[1]):
                light_matrix_for_root[i][j]=light_matrix[i][j]
        
        light_matrix_for_root.Write(f"light_matrix{frame_count}")'''
        for i in range(light_matrix.shape[0]):
            for j in range(light_matrix.shape[1]):
                if light_matrix[i][j]:
                    file.write("1")
                else:
                    file.write(" ")
                file.write("\n")
        file.write("\n#--------------------\n")
        
        muon_frame_count=check_if_muon(light_matrix)
        
        muon_count+=muon_frame_count
        
        cv2.imshow("Original Video", frame)

        old_lux_matrix=lux_matrix.copy()    
        
        count_true=0
        for i in range(grid[1]):
            for j in range(grid[0]):
                if light_matrix[i][j]:
                    count_true+=1
        
        if count_true>4:
            cv2.imwrite(f"image{interesting_frame_count}.jpg", frame)
            interesting_frame_count+=1
        
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break
        
        print(muon_count)
        
    cap.release()
    cv2.destroyAllWindows()
file.close()