import cv2 as cv
import random as r

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt2.xml')
cap = cv.VideoCapture(0)

time = 0
dir_x = 0
dir_y = 0
delta_x = 0
delta_y = 0
i_x = 1
i_y = 1

while True:
    ret, img = cap.read()
    gris = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gris, 1.3, 5)
    time += 1
    
    
    
    
    
    for(x,y,w,h) in rostros:
        
        if(dir_x == delta_x): i_x = 0
        if(dir_y == delta_y): i_y = 0
    
    
        if((dir_x == delta_x) and (dir_y == delta_y)):
            print("Entramos a chambear")
            dir_x = r.randint(int(-1*(w//16)),int(1*(w//16)))
            dir_y = r.randint(int(-1*(w//16)),int(1*(w//16)))
            
            if(dir_x > delta_x): 
                i_x = 1
                print("IX")
            else: 
                i_x = -1
                print("-IX")
                
            if(dir_y > delta_y): 
                i_y = 1
                print("IY")
            else: 
                i_y = -1
                print("-IY")
            
        delta_x += i_x
        delta_y += i_y
        
        print(f"DIR: {dir_x},{dir_y}")
        print("")
        print(f"DELTA: {delta_x},{delta_y}")
        print("")
        print(f"I: {i_x},{i_y}")
        print("")
        
        
        res = int((w+h)/8)
        
        img = cv.rectangle(img, (x,y), (x+w, y+h), (234, 23,23), 5)
        img = cv.rectangle(img, (x,int(y+h/2)), (x+w, y+h), (0,255,0),5 )

        img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , w//16, (0, 0, 0), -1 )
        img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , w//16, (0, 0, 0), -1 )
        
        if( time <= 10):
            img = cv.circle(img, (x + int(w*0.3), y + int(h*0.4)) , w//17, (255, 255, 255), -1 ) # Esclerotica
            img = cv.circle(img, (x + int(w*0.3) + delta_x, y + int(h*0.4) + delta_y) , w//50, (0, 0, 255), -1 )     # Pupila
            
            img = cv.circle(img, (x + int(w*0.7), y + int(h*0.4)) , w//17, (255, 255, 255), -1 ) # Esclerotica
            img = cv.circle(img, (x + int(w*0.7) + delta_x, y + int(h*0.4) + delta_y) , w//50, (0, 0, 255), -1 )     # Pupila
        else:
            if(time >= 15): time = 0
            
        
        img = cv.rectangle(img, (x + int(w*0.36), y + int(h*0.375)), (x + int(w*0.6), y + int(h*0.65)), (234,0,234), 5) # Nariz
        
        # img = cv.circle(img, (x + int(w*0.6), y + int(h*0.65)) , w//50, (0, 0, 255), -1 )
        img = cv.rectangle(img, (x+ int(w*.35), y+int(h*0.78)), (x + int(w*0.6), y + int(h*0.85)), (87,122,185), 5) # Boca
        
        # img = cv.rectangle(img, (x+ int(w*.09), y+int(h*0.375)), (x + int(w*0.15), y + int(h*0.65)), (71,190,155), 5) # Oreja 1
        # img = cv.rectangle(img, (x+ int(w*.85), y+int(h*0.375)), (x + int(w*0.91), y + int(h*0.65)), (71,190,155), 5) # Oreja 2
        
        # Sombrero
        img = cv.rectangle(img, (x+ int(w*.15), y+int(h*.05)), (x + int(w*0.85), y + int(h*-.5)), (0,0,0), -1)
        img = cv.rectangle(img, (x+ int(w*-.15), y+int(h*.08)), (x + int(w*1.15), y + int(h*.05)), (0,0,0), -1)
        
    cv.imshow('img', img)
    if cv.waitKey(1)== ord('q'):
        break
    
cap.release
cv.destroyAllWindows()