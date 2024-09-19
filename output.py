import cv2
import base64
import logging
import pyzbar
logging.getLogger("pyzbar").setLevel(logging.ERROR)

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None  

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
        byte = pyzbar.pyzbar.decode(img)
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
        print("File complete!")

b = Video()
b.to_byte("output.mp4")
b.to_zip("output.zip")