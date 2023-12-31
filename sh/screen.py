import numpy as np
import os
import cv2
# import pyautogui

# RES_SCREEN = pyautogui.size() # RES_SCREEN[0] -> width
                              # RES_SCREEN[1] -> heigth
class Screen:
    """
    Class for a screen
    Attributes:
        screen: numpy array representing the screen view
        background_color: the background color of the screen
        width: screen width in pixels
        height: screnn height in pixels
        current_answer: current selected answer between 'yes' or 'no'
    """
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.background_color = (200,225,240, 255)
        self.screen = np.ones((self.height, self.width, 4), np.uint8)
        self.screen[:] = self.background_color
        self.current_answer = None
        self.print_instructions()
        self.print_title()

    def clean_answers(self):
        cv2.rectangle(self.screen, (0,self.height // 3), (self.width, self.height), self.background_color, -1)
        self.print_answers()

    def color_answers(self):
        cv2.rectangle(self.screen, (0,self.height // 3), (self.width, self.height), self.background_color, -1)
        if self.current_answer == 'yes':
            cv2.rectangle(self.screen, (0, self.height // 3), (self.width // 2, self.height), (0,0,255), -1)

        if self.current_answer == 'no':
            cv2.rectangle(self.screen, (self.width // 2, self.height // 3), (self.width, self.height), (0,0,255), -1)
        self.print_answers()

    def confirm_answer(self, answer):
        cv2.rectangle(self.screen, (0,self.height // 3), (self.width, self.height), self.background_color, -1)
        if answer == 'yes':
            cv2.rectangle(self.screen, (0, self.height // 3), (self.width // 2, self.height), (0,255,0), -1)

        if answer == 'no':
            cv2.rectangle(self.screen, (self.width // 2, self.height // 3), (self.width, self.height), (0,255,0), -1)
        self.print_answers()

    def update_direction(self, direction):
        if direction == 'left':
            self.current_answer = 'yes'
        if direction == 'right':
            self.current_answer = 'no'

    def clean(self):
        self.screen = np.ones((self.height, self.width, 4), np.uint8)
        self.screen[:] = self.background_color

        if os.path.isfile((os.path.join('resources', 'sorting_hat.png'))):
            sh_image = cv2.imread(os.path.join('resources','sorting_hat.png'), cv2.IMREAD_UNCHANGED)

            height, width, channels = sh_image.shape

            ratio = (self.height/3) / height
            sh_image = cv2.resize(sh_image, (int(width * ratio),int(height * ratio)))

            height, width, channels = sh_image.shape
            offset_x = self.width - width
            offset_y = 0

            background = self.screen[offset_y:offset_y + height, offset_x:offset_x + width, :]
            foreground = sh_image

            # normalize alpha channels from 0-255 to 0-1
            alpha_background = background[:,:,3] / 255.0
            alpha_foreground = foreground[:,:,3] / 255.0

            # set adjusted colors
            for color in range(0, 3):
                background[:,:,color] = alpha_foreground * foreground[:,:,color] + alpha_background * background[:,:,color] * (1 - alpha_foreground)

            # set adjusted alpha and denormalize back to 0-255
            background[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255


    def print_answers(self):

        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 2
        th = 3

        answer = 'Look left\nfor YES'

        for i, line in enumerate(answer.split('\n')):
            textsize = cv2.getTextSize(line, font, fs, th)[0]
            x = (self.width // 2 - textsize[0]) // 2
            y0, dy = self.height // 3 + ((2 * (self.height // 3) + textsize[1]) // 2) - textsize[1], textsize[1] + 30
            y = y0 + i*dy
            cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)

        answer = 'Look right\nfor NO'

        for i, line in enumerate(answer.split('\n')):
            textsize = cv2.getTextSize(line, font, fs, th)[0]
            x = self.width // 2 + (self.width // 2 - textsize[0]) // 2
            y0, dy = self.height // 3 + ((2 * (self.height // 3) + textsize[1]) // 2) - textsize[1], textsize[1] + 30
            y = y0 + i*dy
            cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)


    def print_question(self, question):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 1.2
        th = 3

        y0, dy = int(0.15 * self.height), 35

        for i, line in enumerate(question.split('\n')):
            textsize = cv2.getTextSize(line, font, fs, th)[0]
            x = self.width // 4 + (self.width // 2 - textsize[0]) // 2
            y = y0 + i*dy
            cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)

    def print_title(self):

        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 1.7
        th = 5
        line = 'HI, I\'M THE SORTING HAT'
        textsize = cv2.getTextSize(line, font, fs, th)[0]
        x = self.width // 4 + (self.width // 2 - textsize[0]) // 2
        y = int(0.1 * self.height) + textsize[1]
        cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)


    def print_instructions(self):

        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 0.8
        th = 2
        x, y0, dy = int(0.02 * self.width), int(0.09 * self.height), 25

        instructions = "Press:\nESC to quit\ns to start quiz\nn to next question"

        for i, line in enumerate(instructions.split('\n')):
            y = y0 + i*dy
            cv2.putText(img=self.screen, text=line, org=(x, y), fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)

    def show_result(self, result):
        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 1.5
        th = 3
        line = 'The Sorting Hat says...'
        textsize = cv2.getTextSize(line, font, fs, th)[0]
        x = self.width // 4 + (self.width // 2 - textsize[0]) // 2
        y = int(0.15 * self.height) + textsize[1]
        cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)

        font = cv2.FONT_HERSHEY_SIMPLEX
        fs = 2.5
        th = 5
        line = result.upper()
        textsize = cv2.getTextSize(line, font, fs, th)[0]
        x = (self.width - textsize[0]) // 2
        y = int(0.85 * self.height) - textsize[1]
        cv2.putText(img=self.screen, text=line, org=(x, y),fontFace=font, fontScale=fs, color=(0,0,0), thickness=th)

        if os.path.isfile((os.path.join('resources', result.lower()+'.png'))):
            house_image = cv2.imread(os.path.join('resources',result.lower()+'.png'), cv2.IMREAD_UNCHANGED)

            height, width, channels = house_image.shape

            ratio = self.height / height
            house_image = cv2.resize(house_image, (int(width * ratio),int(height * ratio)))

            height, width, channels = house_image.shape
            offset_x = self.width - width
            offset_y = 0

            self.screen[offset_y:offset_y + height, offset_x:offset_x + width, :] = self.background_color
            background = self.screen[offset_y:offset_y + height, offset_x:offset_x + width, :]
            foreground = house_image

            # normalize alpha channels from 0-255 to 0-1
            alpha_background = background[:,:,3] / 255.0
            alpha_foreground = foreground[:,:,3] / 255.0

            # set adjusted colors
            for color in range(0, 3):
                background[:,:,color] = alpha_foreground * foreground[:,:,color] + alpha_background * background[:,:,color] * (1 - alpha_foreground)

            # set adjusted alpha and denormalize back to 0-255
            background[:,:,3] = (1 - (1 - alpha_foreground) * (1 - alpha_background)) * 255


        self.show()

    def show(self):
        print("hellow")
        # cv2.namedWindow("screen")
        # cv2.moveWindow("screen", int(RES_SCREEN[0] / 2 - self.width/2), 0)

#        cv2.namedWindow("screen", cv2.WND_PROP_FULLSCREEN)
#        cv2.setWindowProperty("screen",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
#         cv2.imshow("screen", self.screen)



