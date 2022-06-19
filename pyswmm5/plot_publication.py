# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  : Plot for academic publication
# @Date     : 2021.12.30
# @Author   : Ruozhou Lin
# @Email    : ruozhoulin@zju.edu.cn

    Useful parameters, settings and functions to create high
quality figures for publication
-------------------------------------------------
"""

import matplotlib.pyplot as plt
import matplotlib

# * ====================================================================
# * Set font's properties.
# ! You must use from `PLOT_academic import *` to enable font size setting
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

# controls default text sizes
font = {'family': 'Times New Roman',
        'weight': 'normal',  # bold
        'size': SMALL_SIZE}
matplotlib.rc('font', **font)
# fontsize of the axes title, namely title of subplot
plt.rc('axes', titlesize=MEDIUM_SIZE)
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
# * =====================================================================


class Page():
    """This class define the size of the page/slide that you want to insert your figure.
    Please set the `height`, `width`, and `margin` of the page/slide in inch.

    If you are not familiar with these term, please refer to Word -> Layout -> Page Setup
    section for more information.
    """

    def __init__(self, height, width, margin=(0, 0, 0, 0)) -> None:
        # Define size of the paper in inch
        self.__height = height  # inch
        self.__width = width  # inch
        self.__margin = margin  # (top, bottum, left, right)
        self.validate()  # Check if the above parameters are reasonable.

    def validate(self):
        """Check if page parameters are reasonable, i.e., the margin should be 
        positive and should not be larger than the page.
        """
        assert self.__height > 0 and self.__width > 0
        for value in self.margin:
            assert value >= 0
        assert self.margin[0] + self.margin[1] < self.__height
        assert self.margin[2] + self.margin[3] < self.__width

    @property
    def page_size(self):
        return self.__height, self.__width

    @page_size.setter
    def page_size(self, height, width):
        self.__height = height
        self.__width = width
        self.validate()

    @property
    def body_size(self):
        height = self.__height-self.__margin[0]-self.__margin[1]
        width = self.__width-self.__margin[2]-self.__margin[3]
        return height, width

    @property
    def margin(self):
        return self.__margin

    @margin.setter
    def margin(self, values):
        self.__margin = values
        self.validate()  # Check if the above parameters are reasonable.

    def print_page_setting(self):
        print('The size of the page is %.2f * %.2f.' %
              (self.__height, self.__width))
        print("""The margin is:
    Top:    %.2f
    Bottom: %.2f
    Left:   %.2f
    Right:  %.2f""" % self.__margin)

    # set space between subplot
    def set_width_space(self, v=0.25):
        plt.rcParams['figure.subplot.wspace'] = v

    def set_height_space(self, v=0.3):
        plt.rcParams['figure.subplot.hspace'] = v


class PageA4(Page):
    """Create a subclass of `Page` that has a size of A4 and use default margin setting in Word.
    """

    def __init__(self, height=11.69, width=8.27, margin=(1, 1, 1.25, 1.25)) -> None:
        super().__init__(height, width, margin)

    def print_page_setting(self):
        print('Page A4:')
        super().print_page_setting()


class PageLetter(Page):
    """Create a subclass of `Page` that has a size of Letter and use default margin setting in Word.
    """

    def __init__(self, height=11, width=8.5, margin=(1, 1, 1.25, 1.25)) -> None:
        super().__init__(height, width, margin)

    def print_page_setting(self):
        print('Page Letter:')
        super().print_page_setting()


class PageSlide(Page):
    """Create a subclass of `Page` that has a size of slide and use default setting in PowerPoint.
    """

    def __init__(self, height=0, width=0, aspectRatio='4:3', margin=(0, 0, 0, 0)) -> None:
        if aspectRatio == '4:3':
            height, width = 7.5, 10
        elif aspectRatio == '16:9':
            height, width = 7.5, 13.33
        else:
            pass
        super().__init__(height, width, margin)

    def print_page_setting(self):
        print('Page for slides:')
        super().print_page_setting()


class FigurePublication():
    def __init__(self, nrows, ncols, page=PageA4(), xrate=None, yrate=None, tightLayout=True) -> None:
        self.__bbox_inches = 'tight'
        # 300 is usually minimum requirement for high resolution images, 600 is better
        self.__dpi = 300
        self.page: Page = page
        self.__nrows = nrows
        self.__ncols = ncols
        self.fig, self.ax = plt.subplots(nrows, ncols)
        self.tightLayout = tightLayout
        self.arrange(xrate, yrate)

    def update(self, tightLayout=True):
        if tightLayout:  # auto adjust layout
            self.fig.tight_layout()

    def arrange(self, xrate=None, yrate=None):
        """Automatically set size of the figure according to the page size and figure content.
        You can also do this manually by setting `xrate` and `yrate`.
        """
        # this rate is for sub-figure with full x-y labels
        xy = (((0.6, 0.30),  (1.0, 0.28), (1.0, 0.25), (1.0, 0.25)),
              ((1.0, 0.55),  (1.0, 0.55), (1.0, 0.55), (1.0, 0.55)),
              ((1.0, 0.80),  (1.0, 0.80), (1.0, 0.80), (1.0, 0.80)),
              ((1.0, 1.00),  (1.0, 1.00), (1.0, 1.00), (1.0, 1.00)))

        xrate1, yrate1 = xy[self.__nrows-1][self.__ncols-1]
        # Check these parameters are set manully.
        if xrate is not None:
            xrate1 = xrate
        if yrate is not None:
            yrate1 = yrate
        # set figure size
        height, width = self.page.body_size
        width1 = width * xrate1
        height1 = height * yrate1
        self.fig.set_size_inches(width1, height1)
        # auto adjust layout
        self.update()

    def save(self, savename: str, bbox_inches=None, dpi=None):
        """Save the figure in .svg format.
        """
        # format of save name should be "directory/figure.svg"
        assert savename.split('.')[-1] == 'svg'
        # if dpi is not assigned external, use dpi store in this class
        if dpi is None:
            dpi = self.__dpi
        # same for bbox_inces
        if bbox_inches is None:
            bbox_inches = self.__bbox_inches
        self.update()
        self.fig.savefig(savename, format='svg',
                         bbox_inches=bbox_inches,
                         dpi=dpi)

    def change_page(self, newpage=PageSlide()):
        # modify paper size, such as from A4 to a slide in 16:9
        self.page = newpage
        self.arrange()


def get_default_color(type='rgb') -> list:
    # [u'#1f77b4', u'#ff7f0e', u'#2ca02c', u'#d62728', u'#9467bd',
    # u'#8c564b', u'#e377c2', u'#7f7f7f', u'#bcbd22', u'#17becf']
    lst = matplotlib.rcParams['axes.prop_cycle'].by_key()['color']  # hex
    if type == 'rgb':
        # convert hex to rgb that ranges from 0 to 1
        lst = [list(int(h.lstrip('#')[i:i+2], 16)/256
                    for i in (0, 2, 4)) for h in lst]
    return lst


def legend(ax):
    ax.legend(frameon=False)  # remove legend background


# * check whether font exist
if __name__ == "__main__":
    fontPath = matplotlib.font_manager.findfont('Times New Roman')
    print(fontPath)
