from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile
from PgGUI import SimpleGUI
from PIL import Image
import pygame 
import base64
import math
import io
import ast
import sys
import win32api
import win32con
import win32gui
import pygame.font


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    global win,is_desktop,DesktopWindow
    if not is_desktop:
        x, y = event.x - lastClickX + win.winfo_x(), event.y - lastClickY + win.winfo_y()
        win.geometry("+%s+%s" % (x , y))
    else:
        x, y = event.x - lastClickX + DesktopWindow.winfo_x(), event.y - lastClickY + DesktopWindow.winfo_y()
        DesktopWindow.geometry("+%s+%s" % (x , y))


def SelectPen():
    global is_desktop,pen_mode,hwnd,DrawButton,selected_object,DeleteImageButton,all_events
    if not is_desktop:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR))
        if pen_mode == 0:
            EraseButton.config(bg="#1c161f")
        elif pen_mode == -1:
            MoveButton.config(bg="#1c161f")
        pen_mode = 1
        DrawButton.config(bg="red")
        selected_object = None
        DeleteImageButton.pack_forget()
        win32gui.SetFocus(hwnd)
        all_events = []


def SelectEraser():
    global is_desktop,pen_mode,hwnd,selected_object,DeleteImageButton,all_events
    if not is_desktop:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_NO))
        if pen_mode == 1:
            DrawButton.config(bg="#1c161f")
        elif pen_mode == -1:
            MoveButton.config(bg="#1c161f")
        pen_mode = 0
        EraseButton.config(bg="red")
        selected_object = None
        DeleteImageButton.pack_forget()
        win32gui.SetFocus(hwnd)
        all_events = []


def SelectMove():
    global is_desktop,pen_mode,hwnd,all_events
    if not is_desktop:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEALL))
        if pen_mode == 1:
            DrawButton.config(bg="#1c161f")
        elif pen_mode == 0:
            EraseButton.config(bg="#1c161f")
        pen_mode = -1
        MoveButton.config(bg="red")
        win32gui.SetFocus(hwnd)
        all_events = []


def ClearAll():
    global is_desktop,pixel_list,image_list,textbox_list,hwnd,selected_object,DeleteImageButton,all_events
    if not is_desktop:
        pixel_list = []
        image_list = []
        textbox_list=[]
        if selected_object!=None:
            DeleteImageButton.pack_forget()
        selected_object = None
        win32gui.SetFocus(hwnd)
        all_events = []


def SaveAll():
    global is_desktop,hwnd,pixel_list,image_list,textbox_list,Saved_Changes,all_events
    if not is_desktop:
        try:
            saving_location = asksaveasfile(title='Save ClassBoard File:',filetypes = filetypes, defaultextension = filetypes)
            if saving_location!=None:
                with open(f"{saving_location.name}", f"{saving_location.mode}") as f:
                    saving_data = ""
                    saved_pixels = []
                    saved_images = []
                    saved_textboxes = []
                    for p in pixel_list:
                        saved_pixels.append([p.sx,p.sy,p.ex,p.ey,p.size,p.color])
                    for image in image_list:
                        saved_images.append([image.rect.x,image.rect.y,image.data,image.rect.width,image.rect.height])
                    for text in textbox_list:
                        saved_textboxes.append([text.rect.x, text.rect.y, text.rect.width, text.rect.height ,text.color, text.font_size, text.text_lines])
                    saving_data = f"{saved_pixels} , {saved_images} , {saved_textboxes}"
                    f.write(str(saving_data))
                    Saved_Changes = True
        except:
            pass
        win32gui.SetFocus(hwnd)
        all_events = []


def OpenFile(file=None):
    global is_desktop,pixel_list,hwnd,image_list,textbox_list,Saved_Changes,all_events
    if not is_desktop:
        if file == None:
            location = filedialog.askopenfilename(title='Select ClassBoard File:',initialdir='/',filetypes=filetypes)
        else:
            location = file
        if location!="":
            try:
                with open(location,'r') as f:
                    file_data = f.read()
                    file_data = file_data.split(" , ")
                    try:
                        file_data_pixels = ast.literal_eval(file_data[0])   
                    except:
                        file_data_pixels = []
                    try:  
                        file_data_images = ast.literal_eval(file_data[1])
                    except:
                        file_data_images = [] 
                    try:
                        file_data_textbox= ast.literal_eval(file_data[2])
                    except:
                        file_data_textbox = []
                    pixel_list = []
                    image_list = []
                    textbox_list = []
                    for p in file_data_pixels:
                        Draw(p[0],p[1],p[2],p[3],p[4],p[5])
                    for image in file_data_images:
                        ImageObject(image[2],image[0],image[1],[image[3],image[4]])
                    for text in file_data_textbox:
                        #[text.rect.x, text.rect.y, text.rect.width, text.rect.height ,text.color, text.font_size, text.text_lines]
                        TextBox(text[0], text[1], text[2], text[3], None, text[5], text[4], text[6])
                    Saved_Changes = True
            except Exception as e:
                messagebox.showerror("Class Board",f"Your file could not be opened due to an unexpected error!\n\nPlease try another file and make sure that the data saved in the file is not corrupted.\n\nIf the file is corrupted or saved improperly, part of the data can be saved.\n\nError:'{e}'")
        win32gui.SetFocus(hwnd)
        all_events = []


def PenColor():
    global is_desktop,pen_color,hwnd,all_events
    if not is_desktop:
        color = askcolor(title="Select Color")[0]
        if color != None:
            pen_color = color
        win32gui.SetFocus(hwnd)
        all_events = []
        SelectPen()


def CanvasColor():
    global is_desktop,background_color,hwnd,all_events
    if not is_desktop:
        color = askcolor(title="Select Color")[0]
        if color != None:
            background_color = color
        win32gui.SetFocus(hwnd)
        all_events = []


def Normal():
    global size,hwnd,all_events
    if not is_desktop:
        if size == 5:
            MediumSize.config(bg="#1c161f")
        elif size == 8:
            HugeSize.config(bg="#1c161f")
        size = 2
        NormalSize.config(bg="red")
        win32gui.SetFocus(hwnd)
        all_events = []


def Medium():
    global size,hwnd,all_events
    if not is_desktop:
        if size == 2:
            NormalSize.config(bg="#1c161f")
        elif size == 8:
            HugeSize.config(bg="#1c161f")
        size = 5
        MediumSize.config(bg="red")
        win32gui.SetFocus(hwnd)
        all_events = []


def Huge():
    global size,hwnd,all_events
    if not is_desktop:
        if size == 2:
            NormalSize.config(bg="#1c161f")
        elif size == 5:
            MediumSize.config(bg="#1c161f")
        size = 8
        HugeSize.config(bg="red")
        win32gui.SetFocus(hwnd)
        all_events = []


def DesktopMode():
    global is_desktop,all_events
    is_desktop=not is_desktop
    if not is_desktop:
        win.deiconify()
        win.geometry(f"+{DesktopWindow.winfo_x()}+{DesktopWindow.winfo_y()}")
        DesktopWindow.withdraw()
        win32gui.SetFocus(hwnd)
        all_events = []
    else:
        DesktopWindow.deiconify()
        DesktopWindow.geometry(f"+{win.winfo_x()}+{win.winfo_y()}")
        DesktopWindow.geometry(f"{win.winfo_width()}x{DesktopWindow.winfo_height()}")
        win.withdraw()


def Quit():
    global run, pixel_list, image_list, textbox_list, Saved_Changes,all_events
    response = False
    if (len(pixel_list)>100 or len(image_list)>0 or len(textbox_list)>0) and Saved_Changes == False:
        response = messagebox.askyesnocancel("Quit ClassBoard?","          Would you like to save your ClassBoard\n          file before closing?          ")
    if response == False:
        run = False
    elif response == True:
        SaveAll()
        run = False 
    elif response == None:
        win32gui.SetFocus(hwnd)
        all_events = []


def rect_corners(rect):
    return [(rect.left, rect.top), 
            (rect.right, rect.top), 
            (rect.right, rect.bottom), 
            (rect.left, rect.bottom)]


class Draw:
    def __init__(self,sx,sy,ex,ey,size,color):
        global pixel_list
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.size = size
        self.color = color
        pixel_list.append(self)


class ImageObject:
    def __init__(self,file, x, y,scale = None):
        global image_list
        self.data = file
        output = io.BytesIO(base64.b64decode(self.data))
        self.original_image = pygame.image.load(output)
        self.image = self.original_image
        if scale!=None:
            self.image = pygame.transform.scale(self.original_image, (scale[0], scale[1]))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        image_list.append(self)
class TextBox:
    def __init__(self, x, y, width, height, font, font_size, color, text_lines=None):
        global textbox_list
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(font, font_size)
        self.color = color
        self.font_size = font_size
        if text_lines != None:
            self.text_lines = text_lines
        else:
            self.text_lines = [""]
        self.caret_pos = [0, 0]
        self.caret_visible = True
        self.caret_blink_time = 500 
        self.last_blink = pygame.time.get_ticks()
        textbox_list.append(self)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.add_newline()
            elif event.key == pygame.K_BACKSPACE:
                self.delete_character()
            elif event.key == pygame.K_LEFT:
                self.move_caret_left()
            elif event.key == pygame.K_RIGHT:
                self.move_caret_right()
            elif event.key == pygame.K_UP:
                self.move_caret_up()
            elif event.key == pygame.K_DOWN:
                self.move_caret_down()
            elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                clip_board = pygame.scrap.get("text/plain;charset=utf-8")
                if clip_board!=None:
                    for character in clip_board.decode():
                        if ord(character) > 31 and ord(character) < 127:
                            self.add_character(character)
                        elif ord(character) == 10:
                            self.add_newline()
            elif event.key > 31 and event.key < 127:
                self.add_character(event.unicode)

    def add_character(self, char):
        line_index, char_index = self.caret_pos
        current_line = self.text_lines[line_index]
        new_line = current_line[:char_index] + char + current_line[char_index:]

        self.text_lines[line_index] = new_line
        self.caret_pos[1] += 1

        self.wrap_text()

    def delete_character(self):
        line_index, char_index = self.caret_pos
        if char_index > 0:
            self.text_lines[line_index] = (
                self.text_lines[line_index][:char_index-1] +
                self.text_lines[line_index][char_index:]
            )
            self.caret_pos[1] -= 1
        elif line_index > 0:
            previous_line = self.text_lines[line_index-1]
            self.caret_pos = [line_index-1, len(previous_line)]
            self.text_lines[line_index-1] += self.text_lines[line_index]
            del self.text_lines[line_index]
        self.wrap_text()

    def add_newline(self):
        line_index, char_index = self.caret_pos
        current_line = self.text_lines[line_index]
        self.text_lines[line_index] = current_line[:char_index]
        self.text_lines.insert(line_index+1, current_line[char_index:])
        self.caret_pos = [line_index+1, 0]
        self.wrap_text()

    def move_caret_left(self):
        line_index, char_index = self.caret_pos
        if char_index > 0:
            self.caret_pos[1] -= 1
        elif line_index > 0:
            self.caret_pos = [line_index-1, len(self.text_lines[line_index-1])]

    def move_caret_right(self):
        line_index, char_index = self.caret_pos
        if char_index < len(self.text_lines[line_index]):
            self.caret_pos[1] += 1
        elif line_index < len(self.text_lines) - 1:
            self.caret_pos = [line_index+1, 0]

    def move_caret_up(self):
        line_index, char_index = self.caret_pos
        if line_index > 0:
            self.caret_pos = [line_index-1, min(char_index, len(self.text_lines[line_index-1]))]

    def move_caret_down(self):
        line_index, char_index = self.caret_pos
        if line_index < len(self.text_lines) - 1:
            self.caret_pos = [line_index+1, min(char_index, len(self.text_lines[line_index+1]))]

    def wrap_text(self):
        max_width = self.rect.width
        wrapped_lines = []
        new_caret_pos = list(self.caret_pos)

        for line_index, line in enumerate(self.text_lines):
            while self.font.size(line)[0] > max_width:
                wrap_index = max_width_index = 1
                while self.font.size(line[:wrap_index])[0] < max_width and wrap_index < len(line):
                    wrap_index += 1
                    if line[wrap_index - 1] == ' ':
                        max_width_index = wrap_index

                if max_width_index == 1:  # No spaces found, wrap character by character
                    max_width_index = wrap_index - 1

                wrapped_lines.append(line[:max_width_index].rstrip())
                line = line[max_width_index:].lstrip()

                if line_index == new_caret_pos[0] and new_caret_pos[1] > max_width_index:
                    new_caret_pos[0] += 1
                    new_caret_pos[1] -= max_width_index

            wrapped_lines.append(line)

        max_lines = self.rect.height // self.font.get_height()
        self.text_lines = wrapped_lines[:max_lines]

        if new_caret_pos[0] >= len(self.text_lines):
            new_caret_pos[0] = len(self.text_lines) - 1
            new_caret_pos[1] = len(self.text_lines[new_caret_pos[0]])

        self.caret_pos = new_caret_pos

    def render(self, surface):
        y = self.rect.y
        for line in self.text_lines:
            text_surface = self.font.render(line, True, self.color)
            surface.blit(text_surface, (self.rect.x, y))
            y += self.font.get_height()
        
        if self.caret_visible and self == selected_object:
            caret_x = self.rect.x + self.font.size(self.text_lines[self.caret_pos[0]][:self.caret_pos[1]])[0]
            caret_y = self.rect.y + self.caret_pos[0] * self.font.get_height()
            pygame.draw.line(surface, (255,10,10), (caret_x, caret_y-1), (caret_x, caret_y-1 + self.font.get_height()), int(self.font_size/15))

        current_time = pygame.time.get_ticks()
        if current_time - self.last_blink >= self.caret_blink_time:
            self.caret_visible = not self.caret_visible
            self.last_blink = current_time


def InsertImage():
    global is_desktop, hwnd, image_list,all_events
    if not is_desktop:
        image_file = filedialog.askopenfilename(title='Insert Image ', initialdir='/', filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if image_file:
            try:
                image = Image.open(image_file)
                img_byte_array = io.BytesIO()
                image.save(img_byte_array, format='PNG')
                img_byte_array = img_byte_array.getvalue()
                base64_data = base64.b64encode(img_byte_array).decode('utf-8')
                ImageObject(base64_data, 0, 0)
            except:
                messagebox.showerror("", "Failed to insert image!\nPlease try again later or a different file type!")
    win32gui.SetFocus(hwnd)
    all_events = []


def InsertText():
    global is_desktop, hwnd, image_list, selected_object, pen_mode, select_textbox
    if not is_desktop:
        text = TextBox(50, 50, 300, 200, None, size*15, color=pen_color)
        selected_object = text
        SelectMove()
        select_textbox = True 
        DeleteImageButton["text"] = "Delete Text"
        DeleteImageButton.pack(fill="x",pady=1)



def DeleteSelectedObject():
    global selected_object, image_list, textbox_list, DeleteImageButton
    DeleteImageButton.pack_forget()
    if selected_object in image_list:
        image_list.remove(selected_object)
    elif selected_object in textbox_list:
        textbox_list.remove(selected_object)
    selected_object = None
    win32gui.SetFocus(hwnd)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
pygame.scrap.init()
pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
pygame.display.set_caption("ClassBoard")
win = Tk()
W = win.winfo_screenwidth()
H = win.winfo_screenheight()
TrippleButtonWidth = 7
lastClickX = 0 
lastClickY = 0
MenuFontSize = int(win.winfo_screenwidth()/100)
ThemeColor = "#1c161f"
MenuFontName = "Arial Black"
win.config(bg="black",padx=1,pady=1)
win.attributes("-topmost",True)
win.overrideredirect(True)

QuitButton = Button(win,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg="red",fg="white",activebackground="#110d12",activeforeground="white",text = "Quit",command=Quit)
QuitButton.pack(fill="x")

ToolsContainer= Frame(win,bg="black")
ToolsContainer.pack(fill="x")
DrawButton = Button(ToolsContainer,width=TrippleButtonWidth,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text="Pen",command=SelectPen)
DrawButton.grid(row=0,column=0,padx=1,pady=1)
EraseButton = Button(ToolsContainer,width=TrippleButtonWidth,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text="Erase",command=SelectEraser)
EraseButton.grid(row=0,column=1,padx=1,pady=1)
MoveButton = Button(ToolsContainer,width=TrippleButtonWidth,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "Move",command=SelectMove)
MoveButton.grid(row=0,column=2,padx=1,pady=1)
ColorsContainer = Frame(win,bg="black")
ColorsContainer.pack(fill="x")
PenColorButton = Button(ColorsContainer,width=int(3*TrippleButtonWidth/2),relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "Pen🎨",command=PenColor)
PenColorButton.pack(fill="both",side="left",expand=True,padx=1,pady=1)                                                                                                                                                                              
CanvasColorButton = Button(ColorsContainer,width=int(3*TrippleButtonWidth/2),relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "Canvas🎨",command=CanvasColor)
CanvasColorButton.pack(fill="both",side="right",expand=True,padx=1,pady=1)

SizeContainer= Frame(win,bg="black")
SizeContainer.pack(fill="x")
NormalSize = Button(SizeContainer,width=TrippleButtonWidth,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "I",command=Normal)
NormalSize.grid(row=0,column=0,padx=1,pady=1)
MediumSize = Button(SizeContainer,width=TrippleButtonWidth,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "II",command=Medium)
MediumSize.grid(row=0,column=1,padx=1,pady=1)
HugeSize = Button(SizeContainer,width=TrippleButtonWidth,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "III",command=Huge)
HugeSize.grid(row=0,column=2,padx=1,pady=1)
ActionsContainer = Frame(win,bg="black")
ActionsContainer.pack(fill="x")
ClearButton = Button(ActionsContainer,width=TrippleButtonWidth,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "Clear",command=ClearAll)
ClearButton.grid(row=0,column=0,padx=1,pady=1)
SaveButton = Button(ActionsContainer,width=TrippleButtonWidth,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "Save",command=SaveAll)
SaveButton.grid(row=0,column=1,padx=1,pady=1)
OpenButton = Button(ActionsContainer,width=TrippleButtonWidth,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "Open",command=OpenFile)
OpenButton.grid(row=0,column=2,padx=1,pady=1)

InsertContainer = Frame(win,bg="black")
InsertContainer.pack(fill="x")
InsertImageButton = Button(InsertContainer, width=TrippleButtonWidth, relief="flat", font=(MenuFontName, MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0, bg=ThemeColor, fg="white", activebackground="#110d12", activeforeground="white", text="Image", command=InsertImage)
InsertImageButton.pack(fill="x",expand=True,side="left",padx=1,pady=1)
InsertTextButton = Button(InsertContainer, width=TrippleButtonWidth, relief="flat", font=(MenuFontName, MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0, bg=ThemeColor, fg="white", activebackground="#110d12", activeforeground="white", text="Text", command=InsertText)
InsertTextButton.pack(fill="x",expand=True,side="right",padx=1,pady=1)

DeleteImageButton = Button(win, width=TrippleButtonWidth, relief="flat", font=(MenuFontName, MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0, bg="red", fg="white", activebackground="#110d12", activeforeground="white", text="Delete Image", command=DeleteSelectedObject)
DeleteImageButton.pack(fill="x",pady=1)
DeleteImageButton.pack_forget()

DesktopButton = Button(win,relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "Desktop",command=DesktopMode)
DesktopButton.pack(fill="x",pady=1)

SpaceLabel_1 = Label(win,font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg="red",fg="grey",text="")
SpaceLabel_1.pack(fill="x",pady=1)

win.update()
win.geometry(f"+{W-int(QuitButton.winfo_width()+2)}+0")

SpaceLabel_1.bind('<Button-1>', SaveLastClickPos)
SpaceLabel_1.bind('<B1-Motion>', Dragging)
win.update()

DesktopWindow = Tk()
DesktopWindow.config(bg="black",padx=1,pady=1)
DesktopWindow.attributes("-topmost",True)
DesktopWindow.overrideredirect(True)
DesktopButton = Button(DesktopWindow,width = int(3*TrippleButtonWidth),relief="flat",font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg=ThemeColor,fg="white",activebackground="#110d12",activeforeground="white",text = "Desktop",command=DesktopMode)
DesktopButton.pack(fill="x",pady=1)
SpaceLabel_2 = Label(DesktopWindow,font=(MenuFontName,MenuFontSize,"bold"),borderwidth=0,padx=0,pady=0,bg="red",fg="grey",text="")
SpaceLabel_2.pack(fill="x",pady=1)
SpaceLabel_2.bind('<Button-1>', SaveLastClickPos)
SpaceLabel_2.bind('<B1-Motion>', Dragging)
DesktopWindow.withdraw()

# initializam valorile pentru : - dimensiunea uneltei
#                               - variabila run - ce opreste aplicatia daca devine False
#                               - pozitia initiala a uneltei
#                               - daca unealta este folosita sau nu (este click ul apasat)
#                               - modul initial selectat al uneltei
#                               - imaginea selectata de pe panza
#                               - daca este sau nu activat modul de 'Desktop'
size = 2
NormalSize.config(bg="red")
run = True 
past_x = 0
past_y = 0
pen_down = False
pen_color = (255,255,255)
pen_mode = 1 # 1==draw  0==erase  -1==move screen
DrawButton.config(bg="red")
background_color = (0,0,0)
selected_object = None
is_desktop = False
resized_textbox_wrap = False
Saved_Changes = False
all_events = []

clk = pygame.time.Clock()
pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR))
fuchsia = (224, 224, 224)

hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
win32gui.SetFocus(hwnd)

filetypes = (
        ('Class Board', '*.cls'),
    )

if len (sys.argv)>1:
    pixel_list = []
    image_list = []
    textbox_list = []
    OpenFile(sys.argv[1])
    Saved_Changes = True
else:
    pixel_list = []
    image_list = []
    textbox_list=[]

icon_data = """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"""
output = io.BytesIO(base64.b64decode(icon_data))
icon_image = pygame.image.load(output)
pygame.display.set_icon(icon_image)

while run:
    win.update()
    if not is_desktop:
        screen.fill(background_color)
        for image in image_list:
            if image.rect.x>-image.rect.width and image.rect.x<W+image.rect.width and image.rect.y>-image.rect.height and image.rect.y<H+image.rect.height:
                screen.blit(image.image,image.rect)
                if image == selected_object:
                    pygame.draw.rect(screen,(255,10,10),pygame.rect.Rect(image.rect.x,image.rect.y,image.rect.width,image.rect.height),1)
                    for corner in rect_corners(image.rect):
                        pygame.draw.circle(screen, (255,10,10), corner, 10)
        for pixel in pixel_list:
            if pixel.ex>-100 and pixel.ex<W+100 and pixel.sy>-100 and pixel.sy<H+100:
                pygame.draw.line(screen,pixel.color,(pixel.sx,pixel.sy),(pixel.ex,pixel.ey),pixel.size)
        for text in textbox_list:
            if text.rect.x>-text.rect.width and text.rect.x<W+text.rect.width and text.rect.y>-text.rect.height and text.rect.y<H+text.rect.height:
                if pen_mode == -1:
                    pygame.draw.rect(screen,(10,10,10),pygame.rect.Rect(text.rect.x,text.rect.y,text.rect.width,text.rect.height),1)
                if text == selected_object:
                        pygame.draw.rect(screen,(255,10,10),pygame.rect.Rect(text.rect.x,text.rect.y,text.rect.width,text.rect.height),1)
                        for corner in rect_corners(text.rect):
                            pygame.draw.circle(screen, (255,10,10), corner, 10)
                text.render(screen)
    else:
        screen.fill(fuchsia)
    all_events = pygame.event.get()
    for text in textbox_list:
        if text == selected_object:
            for event in all_events:
                text.handle_event(event)
    for event in all_events:
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.MOUSEMOTION:
            x,y = event.pos
            if pen_down == True and pen_mode==1 and not pygame.rect.Rect(win.winfo_x(),win.winfo_y(),win.winfo_width(),win.winfo_height()).collidepoint(x,y):
                if Saved_Changes == True:
                    Saved_Changes = False
                new = Draw(past_x,past_y,x,y,size,pen_color)
            if pen_down == True and pen_mode==-1:
                select_photo = False
                select_textbox = False
                for image in image_list:
                    if image.rect.x-10<past_x and image.rect.x+image.rect.width+10>past_x and image.rect.y-10<past_y and image.rect.y+image.rect.height+10>past_y and image == selected_object:
                        select_photo = True
                        if image.rect.x+int(image.rect.width/10)<past_x and image.rect.x+image.rect.width-int(image.rect.width/10)>past_x and image.rect.y+int(image.rect.height/10)<past_y and image.rect.y+image.rect.height-+int(image.rect.height/10)>past_y and image == selected_object:
                            if past_x<x:
                                    image.rect.x+=x-past_x
                            if past_x>x:
                                    image.rect.x+=x-past_x
                            if past_y<y:
                                    image.rect.y+=y-past_y
                            if past_y>y:
                                    image.rect.y+=y-past_y
                        else:
                            for corner in rect_corners(image.rect):
                                if pygame.Rect(corner[0] - 10, corner[1] - 10, 20, 20).collidepoint(past_x,past_y):
                                    if rect_corners(image.rect).index(corner) == 0:
                                        image.rect.x += event.rel[0]
                                        image.rect.y += event.rel[1]
                                        image.rect.width -= event.rel[0]
                                        image.rect.height -= event.rel[1]
                                    elif rect_corners(image.rect).index(corner) == 1:
                                        image.rect.y += event.rel[1]
                                        image.rect.width += event.rel[0]
                                        image.rect.height -= event.rel[1]
                                    elif rect_corners(image.rect).index(corner) == 2:
                                        image.rect.width += event.rel[0]
                                        image.rect.height += event.rel[1]
                                    elif rect_corners(image.rect).index(corner) == 3:
                                        image.rect.x += event.rel[0]
                                        image.rect.width -= event.rel[0]
                                        image.rect.height += event.rel[1]
                            image.rect.width = max(20, image.rect.width) 
                            image.rect.height = max(20, image.rect.height)
                            image.image = pygame.transform.scale(image.original_image, (image.rect.width, image.rect.height))
                for text in textbox_list:
                    if text.rect.x-10<past_x and text.rect.x+text.rect.width+10>past_x and text.rect.y-10<past_y and text.rect.y+text.rect.height+10>past_y and text == selected_object:
                        select_photo = True
                        if text.rect.x+int(text.rect.width/10)<past_x and text.rect.x+text.rect.width-int(text.rect.width/10)>past_x and text.rect.y+int(text.rect.height/10)<past_y and text.rect.y+text.rect.height-+int(text.rect.height/10)>past_y and text == selected_object:
                            if past_x<x:
                                    text.rect.x+=x-past_x
                            if past_x>x:
                                    text.rect.x+=x-past_x
                            if past_y<y:
                                    text.rect.y+=y-past_y
                            if past_y>y:
                                    text.rect.y+=y-past_y
                        else:
                            for corner in rect_corners(text.rect):
                                if pygame.Rect(corner[0] - 10, corner[1] - 10, 20, 20).collidepoint(past_x,past_y):
                                    if resized_textbox_wrap == False:
                                        resized_textbox_wrap = True
                                    if rect_corners(text.rect).index(corner) == 0:
                                        text.rect.x += event.rel[0]
                                        text.rect.y += event.rel[1]
                                        text.rect.width -= event.rel[0]
                                        text.rect.height -= event.rel[1]
                                    elif rect_corners(text.rect).index(corner) == 1:
                                        text.rect.y += event.rel[1]
                                        text.rect.width += event.rel[0]
                                        text.rect.height -= event.rel[1]
                                    elif rect_corners(text.rect).index(corner) == 2:
                                        text.rect.width += event.rel[0]
                                        text.rect.height += event.rel[1]
                                    elif rect_corners(text.rect).index(corner) == 3:
                                        text.rect.x += event.rel[0]
                                        text.rect.width -= event.rel[0]
                                        text.rect.height += event.rel[1]
                            text.rect.width = max(100, text.rect.width)  
                            text.rect.height = max(text.font.get_height(), text.rect.height) 
                if select_photo == False and select_textbox == False:
                    selected_object = None
                    if past_x<x:
                        for pixel in pixel_list:
                            pixel.sx+=x-past_x
                            pixel.ex+=x-past_x
                        for image in image_list:
                            image.rect.x+=x-past_x
                        for text in textbox_list:
                            text.rect.x+=x-past_x
                    if past_x>x:
                        for pixel in pixel_list:
                            pixel.sx+=x-past_x
                            pixel.ex+=x-past_x
                        for image in image_list:
                            image.rect.x+=x-past_x
                        for text in textbox_list:
                            text.rect.x+=x-past_x
                    if past_y<y:
                        for pixel in pixel_list:
                            pixel.sy+=y-past_y
                            pixel.ey+=y-past_y
                        for image in image_list:
                            image.rect.y+=y-past_y
                        for text in textbox_list:
                            text.rect.y+=y-past_y
                    if past_y>y:
                        for pixel in pixel_list:
                            pixel.sy+=y-past_y
                            pixel.ey+=y-past_y
                        for image in image_list:
                            image.rect.y+=y-past_y
                        for text in textbox_list:
                            text.rect.y+=y-past_y

            past_x,past_y = x,y
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            pen_down = True
            past_x,past_y = x,y
            if pen_mode == -1:
                select_photo = False
                select_textbox = False
                for image in image_list:
                    if image.rect.x-10<past_x and image.rect.x+image.rect.width+10>past_x and image.rect.y-10<past_y and image.rect.y+image.rect.height+10>past_y:
                        select_photo = True 
                        if selected_object == None:
                            DeleteImageButton["text"] = "Delete Image"
                            DeleteImageButton.pack(fill="x",pady=1)
                        if selected_object!=image:
                            selected_object = image
                            DeleteImageButton["text"] = "Delete Image"
                            image_list.remove(selected_object)
                            image_list.append(selected_object)
                for text in textbox_list:
                    if text.rect.x-10<past_x and text.rect.x+text.rect.width+10>past_x and text.rect.y-10<past_y and text.rect.y+text.rect.height+10>past_y:
                        select_textbox = True 
                        if selected_object == None:
                            DeleteImageButton["text"] = "Delete Text"
                            DeleteImageButton.pack(fill="x",pady=1)
                        if selected_object!=text:
                            selected_object = text
                            DeleteImageButton["text"] = "Delete Text"
                            textbox_list.remove(selected_object)
                            textbox_list.append(selected_object)
                if select_photo == False and select_textbox == False:
                    if selected_object!=None:
                        DeleteImageButton.pack_forget()
                    selected_object = None
            if pen_mode == 1 and not pygame.rect.Rect(win.winfo_x(),win.winfo_y(),win.winfo_width(),win.winfo_height()).collidepoint(x,y):
                new = Draw(past_x,past_y,x,y,size,pen_color)
        if event.type == pygame.MOUSEBUTTONUP:
            x,y = event.pos
            if pen_mode == -1 and resized_textbox_wrap == True and selected_object!=None:
                resized_textbox_wrap = False 
                selected_object.wrap_text()
            pen_down = False
        if event.type == pygame.KEYDOWN:
            if event.unicode == '\x13':
                SaveAll()
            if event.unicode == '\x0f':
                OpenFile()

    if pen_down == True and pen_mode==0:
        x,y = pygame.mouse.get_pos()
        if Saved_Changes == True:
            Saved_Changes = False
        for pixel in pixel_list:
            if math.dist([pixel.sx,pixel.sy],[x,y]) < size*(10):
                pixel_list.remove(pixel)
    
    clk.tick(200)
    pygame.display.update()
win.destroy()#
