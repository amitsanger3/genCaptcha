# for documentation visit: https://www.amitsanger.site/2020/03/generating-captchas-with-python-2.html

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math
import os
import random
from itertools import permutations, combinations


class Captcha(object):
    """
    Generate captchas of desired fonts and colours
    """

    def __init__(self, base_img, fonts, font_size, output_dir, x_range, y_range):
        """
        Initializing Captcha object
        :param base_img: str
            path + base image file name
        :param fonts: str
            path where fonts in .ttf & .otf extensions are save
        :param font_size: array
            array of int for the fonts size
        :param output_dir: str
            path where you want to save captcha
        :param x_range: tuple of 2 ints
            close ends range where x point of text be located
            Note: (a,b) --> both a & b are inclusive.
        :param y_range: tuple of 2 ints
            close ends range where y point of text be located
            Note: (a,b) --> both a & b are inclusive.
        """

        self.base_img = base_img
        self.fonts = [fonts+i for i in os.listdir(fonts)]
        self.font_size = font_size
        self.output_dir = output_dir
        self.x_range = x_range
        self.y_range = y_range
        self.save_dir = output_dir

    def genrate_chars(self, characters, r):
        """
        Generate all possible permutations of given array of
        characters in a tuple
        :param characters: array
            characters you want permutations
        :param r: int
            number of characters in a permutation
        :return: object
        """

        return permutations(characters, r)

    def get_font(self):
        """
        Randomly chosen font
        :return: str
            file name of font
        """

        return random.choice(self.fonts)

    def get_font_size(self):
        """
        Randomly chosen font size
        :return: int
        """

        return random.choice(self.font_size)

    def string(self, char):
        """
        Get string of characters from an array
        :param char: array/ tup
            tup of characters
        :return: str
        """

        return "".join([str(i) for i in char])

    def xy_cordinates(self):
        """
        Random starting x & y coordinates by given
        x_range & y_range
        :return: tup
        """

        return random.randint(self.x_range[0], self.x_range[1]), random.randint(self.y_range[0], self.y_range[1])

    def get_rgb(self):
        """
        Get Randomly Generate R,G & B colours.
        :return: tuple of 3 ints
            (R,G,B)
        """

        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)

        if (r == g == b) and (r & g & b > 200):
            self.get_rgb()

        return r,g,b

    def get_color(self):
        """
        Get color string in RGB Format.
        :return: str
        """

        rgb = self.get_rgb()

        return "rgb("+ ", ".join([str(i) for i in rgb])+")"

    def captcha(self, message):
        """
        Generate & save captcha image of given text
        :param message: str
        :return: None
        """

        base_image = Image.open(self.base_img)
        draw_image = ImageDraw.Draw(base_image)
        image_font = ImageFont.truetype(font=self.get_font(), size=self.get_font_size())
        draw_image.text(self.xy_cordinates(), message, fill=self.get_color(), font=image_font)
        base_image.save(self.output_dir+message+'.png')

    def genrate_captchas(self, iteration, characters, r):
        """
        Generate & save captcha image of the given characters
        of the given number in set. This function will create
        directories of the given number of iterations & each
        directory has len(characters)!/(len(characters)-r)!
        images.
        :param iteration: int
            number of time you want to run permutations to get
            captcha. The basic idea is to get captcha of one
            single text in different fonts in many times i.e.
            number of iteration
        :param characters: array
            characters you want in your captcha.
        :param r: int
            number of characters in a permutation
        :return: None
        """

        num_permutation = (math.factorial(len(characters))/math.factorial(len(characters)-r))*iteration
        n = 1

        for i in range(iteration):
            self.output_dir = self.save_dir+str(i)+"/"
            if os.path.isdir(self.output_dir) is False:
                os.mkdir(self.output_dir)
            chars = self.genrate_chars(characters, r)
            for tup in chars:
                message = self.string(tup)
                self.captcha(message)
                if n % 1000 == 0:
                    print(1-(n/num_permutation), "% REMAINING")
                n+=1

    def test_font(self, message = "012374"):
        """
        Test all the fonts you have with all font sizes
        that they are printing text in a way you want.

        This attribute genrates directory for each font
        with their respective index number at the end &
        every directory has captcha images of that perticular
        font in all font sizes you given while object
        Initializing.

        :pram message = string
            default "012347" --> as I want captcha text
            as a set of 4 integers, this string carryies
            every possible curve that all integers could
            have.
        :return None
        """
        n=0
        for font in self.fonts:
            self.output_dir = self.save_dir+"test_font"+str(n)+"/"
            if os.path.isdir(self.output_dir) is False:
                os.mkdir(self.output_dir)
            n+=1
            m = 0
            for size in self.font_size:
                base_image = Image.open(self.base_img)
                draw_image = ImageDraw.Draw(base_image)
                image_font = ImageFont.truetype(font=font, size=size)
                draw_image.text(self.xy_cordinates(), message, fill=self.get_color(), font=image_font)
                base_image.save(self.output_dir+message+str(m)+'.png')
                m+=1

    def remove_unwanted_fonts(self, unwanted_fonts):
        """
        Remove all unwanted fonts set only those fonts
        you want.

        :param unwanted_fonts: array
            array of index numbers of all unwanted fonts.
        """
        fonts = [self.fonts[i] for i in unwanted_fonts] # collect all fonts paths with file name

        for font in fonts:
            try:
                self.fonts.remove(font)
            except:
                continue

        return None
