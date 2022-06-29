from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd
import os
import sys

test_file = 'D:\\Documents\\czu\\PhD\\UGS_2021_CuneiformRecognition\\img_splitter_python\\images\\tablet_figure.jpg'
test_path = 'D:\\Documents\\czu\\PhD\\UGS_2021_CuneiformRecognition\\img_splitter_python\\images\\cut_output'
test_width = 416 #px
test_height = 416 #px
test_oversize_background = (255, 255, 255) #white

def main():
    root = tk.Tk()
    root.title("IMG Croping tool (Czech University of Life Sciences)")
    root.geometry("1200x800")
    mainWindow = MainWindow(root)

    root.mainloop()

    #print('Croping img')
    #crop(test_path, test_file, test_width, test_height, 0, test_width/2, test_height/2, test_oversize_background)
    #print('Croping done')

class MainWindow:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        self.fileName = ""

        self.top = top
        self.top.bind("<Configure>", self.topResized)

        self.InputsFrame = tk.Frame(top)
        self.InputsFrame.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        #LOAD IMG BUTTON
        self.LoadIMGButton = tk.Button(self.InputsFrame, text="Choose image", font=("Arial", 20), command=self.loadIMGButton_click)
        self.LoadIMGButton.place(x=10, y=20, width=200, height=40)
        #CROP WIDTH
        self.CropWidthFrame = tk.Frame(self.InputsFrame)
        self.CropWidthFrame.place(x=260, y=20, width=250, height=40)
        self.CropWidthText = tk.Label(self.CropWidthFrame, text="Crop width (px):", font=("Arial", 20))
        self.CropWidthText.place(x=0, y=0, width=200, relheight=1)
        self.CropWidthInput = tk.Text(self.CropWidthFrame)
        self.CropWidthInput.insert(tk.END, "416")
        self.CropWidthInput.place(x=210, rely=0.25, width=40, relheight=0.5)
        #CROP HEIGHT
        self.CropHeightFrame = tk.Frame(self.InputsFrame)
        self.CropHeightFrame.place(x=520, y=20, width=250, height=40)
        self.CropHeightText = tk.Label(self.CropHeightFrame, text="Crop height (px):", font=("Arial", 20))
        self.CropHeightText.place(x=0, y=0, width=200, relheight=1)
        self.CropHeightInput = tk.Text(self.CropHeightFrame)
        self.CropHeightInput.insert(tk.END, "416")
        self.CropHeightInput.place(x=210, rely=0.25, width=40, relheight=0.5)
        #EXEC CROP BUTTON
        self.ExecCropButton = tk.Button(self.InputsFrame, text="Execute crop", font=("Arial", 20), command=self.execCropButton_click)
        inputsWidth = 1200
        self.ExecCropButton.place(x=int(inputsWidth-220), y=20, width=200, height=40)


        self.IMGFrame = tk.Frame(top)
        self.IMGFrame.place(relx=0, rely=0.2, relwidth=1, relheight=0.6)

        self.IMGLabel = tk.Label(self.IMGFrame, text="Choose image")
        self.IMGLabel.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.ProcessFrame = tk.Frame(top)
        self.ProcessFrame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        self.ProgressBar = ttk.Progressbar(self.ProcessFrame, orient=tk.HORIZONTAL, mode="determinate", length=100)
        self.ProgressBar.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.2)
        self.ProgressBar["value"] = 0

    def topResized(self, event):
        if(hasattr(self, "ExecCropButton") and (event.width - 220) > 0):
            #print(event.width)
            self.ExecCropButton.place_configure(x=int(event.width - 220))

    def loadIMGButton_click(self):
        file = tkfd.askopenfile(mode="r", title="Choose image to crop")
        self.fileName = file.name
        fileBaseName = os.path.basename(file.name).split('.')[-2]
        self.pathName = os.path.dirname(file.name) + "/" + fileBaseName
        image = Image.open(file.name)
        imgSizeRatio = image.width / image.height
        imgLabelWidth = self.IMGLabel.winfo_width()
        imgLabelHeight = self.IMGLabel.winfo_height()
        print("labelW: " + str(imgLabelWidth) + " | labelH: " + str(imgLabelHeight) + " | imgW: " + str(image.width) + " | " + "imgH: " + str(image.height))
        imgResizeWidth = imgLabelWidth
        imgResizeHeight = imgLabelWidth / imgSizeRatio
        if(abs(imgLabelWidth - image.width) > abs(imgLabelHeight - image.height)):
            imgResizeWidth = imgLabelHeight * imgSizeRatio
            imgResizeHeight = imgLabelHeight
        image_to_show = ImageTk.PhotoImage(image.resize((int(imgResizeWidth), int(imgResizeHeight))))
        #print("opening file:" + str(filename.name))
        self.IMGLabel.configure(image=image_to_show)
        self.IMGLabel.image = image_to_show
        #self.IMGLabel._backbuffer_ = image_to_show
        cropWidth = int(self.CropWidthInput.get("1.0", tk.END))
        cropHeight = int(self.CropHeightInput.get("1.0", tk.END))
        imagesCount = (int(round(image.width/(cropWidth/2), 0))) * (int(round(image.height/(cropHeight/2), 0))-1)
        print("imagesCount: " + str(imagesCount))

    def execCropButton_click(self):
        self.ProgressBar["value"] = 0
        self.top.update_idletasks()
        if(self.fileName != ""):
            cropWidth = int(self.CropWidthInput.get("1.0", tk.END))
            cropHeight = int(self.CropHeightInput.get("1.0", tk.END))
            crop(self.pathName, self.fileName, cropWidth, cropHeight, 0, cropWidth/2, cropHeight/2, (255, 255, 255), self.ProgressBar, self.top)

#overlap_width - redundantní část obrázku, překryv
def crop(path, input, width, height, k, overlap_width = 0, overlap_height = 0, oversize_background = (0, 0, 0), TKprogressBar = None, TKroot = None):
    im = Image.open(input)
    imgwidth, imgheight = im.size
    imagesCount = int(round(imgwidth/overlap_width, 0)) * (int(round(imgheight/overlap_height, 0))-1)
    if(not os.path.exists(path)):
        os.makedirs(path)
        print("Directory created")
    for i in range(0, imgheight, height - int(overlap_height)):
        for j in range(0, imgwidth, width - int(overlap_width)):
            if (j + width - int(overlap_width) < imgwidth) and (i + height - int(overlap_height) < imgheight):
                box_width = j + width
                box_height = i + height
                if (j + width > imgwidth): #zajištění aby crop neřezal víc než je velikost obrázku - aby nevznikal černý okraj
                    box_width = imgwidth
                if (i + height > imgheight):
                    box_height = imgheight
                box = (j, i, box_width, box_height)
                output_img = Image.new('RGB', (width, height), oversize_background)
                a = im.crop(box)
                output_img.paste(a)
                try:
                    save_path = os.path.join(path,"IMG-%03d.png" % k)
                    print(save_path)
                    output_img.save(save_path)
                except:
                    e = sys.exc_info()[0]
                    print(e)
                    pass
                if(TKroot != None and TKprogressBar != None):
                    TKprogressBar["value"] = (100 / imagesCount)*k
                    TKroot.update_idletasks()
                k +=1
    
    print("imgCountCalc: " + str(imagesCount) + " | imgCountFinal: " + str(k))


if __name__ == "__main__":
    main()