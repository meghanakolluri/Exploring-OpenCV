import cv2
import numpy as np
import os
shapes = {}

def scan_image(img_file_path):

   
    """
    Purpose:
    ---
    this function takes file path of an image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image

    Returns:
    ---
    `shapes` :              [ dictionary ]
        details of colored (non-white) shapes present in image at img_file_path
        { 'Shape' : ['color', Area, cX, cY] }
    
    Example call:
    ---
    shapes = scan_image(img_file_path)
    """

    global shapes
    li=[[]]
    d={}
    di={}
    l=[]
    color=""
    area=0
    cX=0
    cY=0
    m1=0
    m2=0
    m3=0
    m4=0
    img=cv2.imread(img_file_path)
    img2=cv2.imread(img_file_path)
    font = cv2.FONT_HERSHEY_COMPLEX
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgbim=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    ret,thresh = cv2.threshold(hsv,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    lower_red=np.array([27,27,179])
    upper_red=np.array([97,105,255])
    mask=cv2.inRange(rgbim,lower_red,upper_red)
    for c in contours:
        shape = "unidentified"
        a=[]
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.009 * cv2.arcLength(c, True), True) 
        if len(approx)==3:
            shape="Triangle"
        elif len(approx) == 4:
               cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)  
               n = approx.ravel()  
               i = 0
               for j in n : 
                    if(i % 2 == 0): 
                       x = n[i] 
                       y = n[i + 1] 
                       string = str(x) + " "+ str(y)  
                       li.append(list(map(int,string.split()))) 
                    i = i + 1
               if(len(li[0])!=0): 
                   m1=(int(li[1][1]-li[0][1]))/(int(li[1][0]-li[0][0]))
                   m2=(li[2][1]-li[1][1])/(int(li[2][0]-li[1][0]))
                   m3=(li[3][1]-li[2][1])/(li[3][0]-li[2][0])
                   m4=(li[0][1]-li[3][1])/(li[0][0]-li[3][0])
                   if((round(m1*m2)==-1 and round(m2*m3)==-1 and round(m3*m4)==-1 and round(m4*m1)==-1)):
                        m5=((li[2][1]-li[0][1])/(li[2][0]-li[0][0]))
                        m6=((li[3][1]-li[1][1])/(li[3][0]-li[1][0]))
                        if((round(m5*m6))==-1 or (int(1/m5)==m6)):
                          shape="Square"
                        else:
                          shape="Rectangle"
                   elif(m1==m3 and m2==m4):
                          m5=((li[2][1]-li[0][1])/(li[2][0]-li[0][0]))
                          m6=((li[3][1]-li[1][1])/(li[3][0]-li[1][0]))
                          if((round(m5*m6))==-1 or (int(1/m5)==m6)):
                              shape="Rhombus"
                          else:
                              shape="Parallelogram"
                   elif(m1==m3 or m2==m4):
                          shape="Trapezium"
                   else:
                          shape="Quadrilateral"
        elif len(approx) == 5:
	           shape = "Pentagon"
        elif len(approx)==6:
                   shape="Hexagon"
        else:
	           shape = "Circle"
        if (len(approx)!=4 or (len(li)>2 and li[1][0]!=0 and li[1][1]!=0)):	      
           area = cv2.contourArea(c)
           M = cv2.moments(c)
           cX = int(M["m10"] / M["m00"])
           cY = int(M["m01"] / M["m00"])
           if cv2.contourArea(c) >200: # filter small contours
              x,y,w,h = cv2.boundingRect(c) # offsets - with this you get 'mask'
              cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
              l=np.array(cv2.mean(img[y:y+h,x:x+w])).astype(np.uint8)
              l=list(l)
              maxi=l.index(max(l))
              if maxi==0:
                color="blue"
              elif maxi==1:
                color="green"
              else:
                color="red" 
           a.append(color)
           a.append(float(round(area,1)))
           a.append(cX)
           a.append(cY)
           d[shape]=a
        li.clear()
    shapes={k: v for k, v in sorted(d.items(), key=lambda item: item[1][1],reverse=True)}
    return shapes

# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes 'Sample1.png' as input and runs scan_image function to find details
#                   of colored (non-white) shapes present in 'Sample1.png', it then asks the user whether
#                   to repeat the same on all images present in 'Samples' folder or not

if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    print('Currently working in '+ curr_dir_path)

    # path directory of images in 'Samples' folder
    img_dir_path = curr_dir_path + '/Samples/'
    
    # path to 'Sample1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'Sample' + str(file_num) + '.png'

    print('\n============================================')
    print('\nLooking for Sample' + str(file_num) + '.png')

    if os.path.exists('Samples/Sample' + str(file_num) + '.png'):
        print('\nFound Sample' + str(file_num) + '.png')
    
    else:
        print('\n[ERROR] Sample' + str(file_num) + '.png not found. Make sure "Samples" folder has the selected file.')
        exit()
    
    print('\n============================================')

    try:
        print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
        shapes = scan_image(img_file_path)

        if type(shapes) is dict:
            print(shapes)
            print('\nOutput generated. Please verify.')
        
        else:
            print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
        exit()

    print('\n============================================')

    choice = input('\nWant to run your script on all the images in Samples folder ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = 2
        
        for file_num in range(file_count):

            # path to image file
            img_file_path = img_dir_path + 'Sample' + str(file_num + 1) + '.png'

            print('\n============================================')
            print('\nLooking for Sample' + str(file_num + 1) + '.png')

            if os.path.exists('Samples/Sample' + str(file_num + 1) + '.png'):
                print('\nFound Sample' + str(file_num + 1) + '.png')
            
            else:
                print('\n[ERROR] Sample' + str(file_num + 1) + '.png not found. Make sure "Samples" folder has the selected file.')
                exit()
            
            print('\n============================================')

            try:
                print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
                shapes = scan_image(img_file_path)

                if type(shapes) is dict:
                    print(shapes)
                    print('\nOutput generated. Please verify.')
                
                else:
                    print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
                    exit()

            except Exception:
                print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
                exit()

            print('\n============================================')

    else:
        print('')
