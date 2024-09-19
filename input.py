import qrcode
import cv2
import base64
import logging
import numpy as np
logging.getLogger("pyzbar").setLevel(logging.ERROR)

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

        binary = self.split(binary, 1024)
        
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