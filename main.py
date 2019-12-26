import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import dlib
import imutils
from imutils import face_utils

print("[INFO] loading facial landmark predictor...")

detector = dlib.get_frontal_face_detector()
model = "data\\shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(model)

class App(tkinter.Tk):
    # def __init__(self, window, window_title, video_source=0):
    def __init__(self, video_source=0):
        tkinter.Tk.__init__(self)
        self.title("FaceIT")
        self.configure(background='dark slate gray')
        self.geometry('660x290+700+120')
        self.resizable(width=True, height=True)
        self.minsize(width=660, height=290)
        self.maxsize(width=1320, height=600)
        # containers for ui
        self.tb = tkinter.Frame(self,background='gray',height=50)
        self.addButtonsInToolbar()
        self.tb.pack(fill='both',expand=False)
        self.frame = tkinter.Frame(self,background='dim gray')

        # Create a canvas that can fit the above video source size
        # self.canvas = tkinter.Canvas(self.frame, width = self.vid.width, height = self.vid.height)
        self.canvas1 = tkinter.Canvas(self.frame,background='slate gray', width = 320, height = 240)
        self.canvas1.pack(side=tkinter.LEFT,fill="both", expand=True)
        self.canvas2 = tkinter.Canvas(self.frame,background='rosy brown', width = 320, height = 240,cursor='cross')
        self.canvas2.pack(side=tkinter.LEFT,fill="both", expand=True)
        self.frame.pack(fill="both", expand=True)
        self.status = tkinter.Label(self, text="loading..Done", bd=1, relief='sunken', anchor='w')
        self.status.pack(side="bottom", fill='both')
        # NON WINDOW STUFF (TECH)
        self.video_source = video_source
        self.vid = None
        self.x = self.y = 0
        self.isSel = False
        self.selRect = None
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        # finalize stuff
        self.setupEvents()
        # self.window.mainloop()
    def addButtonsInToolbar(self):
        self.btnStart = tkinter.Button(self.tb, text="Start",  command=self.startCam)
        self.btnStart.pack(side="left", fill='both')
        self.btnStop = tkinter.Button(self.tb, text="Stop",  command=self.stopCam)
        self.btnStop.pack(side="left", fill='both')
        self.btnFaceDetect = tkinter.Button(self.tb, text="FaceDetector",  command=self.snapshot)
        self.btnFaceDetect.pack(side="left", fill='both')
        self.StartServer = tkinter.Button(self.tb, text="Snapshot",  command=self.snapshot)
        self.StartServer.pack(side="left", fill='both')
        self.btnEnd = tkinter.Label(self.tb, text="-", bd=1, relief='sunken', anchor='w')
        self.btnEnd.pack(side="left", fill='both')
    def setupEvents(self):
        self.canvas1.bind('<Configure>',self.resize)
        self.canvas1.bind("<Button-1>", self.callback)
        self.canvas1.bind("<Key>", self.key) # not working somehow
        self.canvas1.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas1.bind("<B1-Motion>", self.on_move_press)
        self.canvas1.bind("<ButtonRelease-1>", self.on_button_release)

    def snapshot(self):
        if self.vid:
            ret, frame = self.vid.get_frame()
            if ret:
                cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    def faceDetector(self,gray):
        global detector,predictor
        # detect faces in the grayscale frame
        rects = detector(gray, 0)
        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
    
            # loop over the (x, y)-coordinates for the facial landmarks
            # and draw them on the image
            for (x, y) in shape:
                cv2.circle(gray, (x, y), 1, (0, 0, 255), -1)
        return gray
    def update(self):
        if self.vid:
            ret, frame = self.vid.get_frame()
            frame2 = imutils.resize(frame, width=320)
            gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            if ret:
                gray = self.faceDetector(gray)
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(gray))
                self.canvas1.create_image(0, 0, image = self.photo, anchor = tkinter.NW,tags="image")
                self.canvas2.create_image(0, 0, image = self.photo2, anchor = tkinter.NW,tags="image")
        if self.isSel :
            self.canvas1.tag_raise('rect')
            self.canvas1.coords(self.selRect, (self.start_x, self.start_y, self.curX, self.curY))    
            # self.canvas1.coords(self.selRect)    
        self.after(self.delay, self.update)
    def startCam(self):
        # open video source (by default this will try to open the computer webcam)
        if not self.vid:
            self.vid = MyVideoCapture(self.video_source)
            self.status.text = "Starting Camera"
    def stopCam(self):
        if self.vid:
            del self.vid
            self.vid = None
            
    def callback(self,event):
        print ("clicked at", event.x, event.y)
        print ("EVENT TYPE:", event.type) # ButtonPress
        # print ("keyCode:", event.keycode)
        # print (dir(event))
    def key(self,event):
        print ("pressed", repr(event.char))
    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y
        self.curX = event.x
        self.curY = event.y
        # create rectangle if not yet exist
        #if not self.rect:
        self.isSel = True
        print ("Selection STARTED.. ")
        self.selRect = self.canvas1.create_rectangle(self.x, self.y, 1, 1, fill="",outline='white',tags="rect")
        
    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.canvas1.coords(self.selRect, self.start_x, self.start_y, self.curX, self.curY)
    def on_button_release(self, event):
        self.isSel = False
        print ("Selection FINISHED")
        if self.selRect:
            self.canvas1.delete(self.selRect)
            del self.selRect
            self.selRect = None
    def resize(self,event):
        print ("MAIN WINDOW: %s}"%(self.geometry()))
        print ("EVENT: %s,%s"%(event.width,event.height))
        print ("FRAME:",self.frame.winfo_width(),self.frame.winfo_height())
        print ("CANVAS1:",self.canvas1.winfo_width(),self.canvas1.winfo_height())
        print ("CANVAS2:",self.canvas2.winfo_width(),self.canvas2.winfo_height())
        # print ("CANVAS1: %s,%s"%(self.canvas1.winfo_width(),self.canvas1.winfo.height()))
        # print ("CANVAS2: %s,%s"%(self.canvas2.winfo_width(),self.canvas2.winfo.height()))

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print ("CAM RES: %s , %s"%(self.width,self.height))

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                small = cv2.resize(frame,(320,240))
                return (ret, cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
# App(tkinter.Tk(), "Tkinter and OpenCV")

if __name__ == "__main__":
    app = App()
    app.mainloop()