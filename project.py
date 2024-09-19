import qrcode
import cv2
import base64
import logging
import numpy as np
from pyzbar.pyzbar import decode
logging.getLogger("pyzbar").setLevel(logging.ERROR)

import time
start_time = time.time()

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None  

class QRCODE():
    def __init__(self):
        self.head = None
    
    def append(self, data):
        new = Node(data)

        current = self.head
        if current:
            while current.next:
                current = current.next
            current.next = new
        else:
                self.head = new
                    
    def to_img(self, file):
        self.zip = open(file,'rb')
        self.zip = self.zip.read()
        binary = base64.b64encode(self.zip)

        binary = self.split(binary, 2048)
        
        for i in binary:
            i = self.to_QR(i)
            self.append(i)
        self.length = len(binary)
        print(self.length, "Image Generated")

    def to_QR(self, data):
        qr = qrcode.QRCode(version=4,
                 error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return np.array(img).astype(np.uint8)*255
    
    def split(self, arr, size):
         arrs = []
         while len(arr) > size:
             pice = arr[:size]
             arrs.append(pice)
             arr   = arr[size:]
         arrs.append(arr)
         return arrs
     
    def to_video(self):
        out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'XVID'), 60, (900,900))
        
        if self.head == None:
            print("Empty list, please input zip file")
            return
        
        current = self.head
        while current:
            current.data = cv2.cvtColor(current.data, cv2.COLOR_GRAY2BGR)
            current.data = cv2.resize(current.data, (900,900))
            out.write(current.data)
            current = current.next
            
        out.release()
        print("Video Finished")

a = QRCODE()
a.to_img("input.zip")
a.to_video()
del a

class Video():
    def __init__(self):
        self.head = None

    def append(self, data):
        new = Node(data)

        current = self.head
        if current:
            while current.next:
                current = current.next
            current.next = new
        else:
                self.head = new
    
    def to_byte(self, video):
        cap = cv2.VideoCapture(video)
        count = 0
        
        while cap.isOpened():
            rep, frame = cap.read()    
            if rep == False:
                break    
            self.append(frame)
            count+=1
        cap.release()
        self.length = count
        
        current = self.head
        count=0
        while current != None:
            current.data = cv2.cvtColor(current.data, cv2.COLOR_BGR2GRAY)
            current.data = self.decode(current.data)
            current = current.next
            count+=1
            
            if count%100==0:
                print(int((count/self.length)*100),"%")

        print(count, "Frame decoded")
    
    def decode(self, img):
        byte = decode(img)
        byte = base64.b64decode(byte[0].data)
        return byte
    
    def to_zip(self, filename):
        self.bit = bytes()
        with open(filename, 'wb') as z:
            current = self.head

            while current != None:
                self.bit+=current.data
                current = current.next
            z.write(self.bit)


b = Video()
b.to_byte("output.mp4")
b.to_zip("output.zip")
print("--- %s seconds ---" % (time.time() - start_time))