import wx

class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='wx.Notebook')
        # create a wx.Notebook
        book = wx.Notebook(self)
        # create a new page; wx.Notebook owns the page
        # therefore the notebook must be the parent window
        page = MyPage(parent=book)
        # add the page to the notebook:
        book.AddPage(page, 'Page 1')
        book.AddPage(MyPage(book),'Page 2')
        book.AddPage(MyPage(book),'Page 3')

class MyPage(wx.Panel):
    "a page for wx.Notebook"
    def __init__(self, parent):
        # NOTE: wxPython 2.9.4/winXP may create graphic 
        # artifacts when more than one page is added. This can
        # be avoided by creating the page with a size of (0,0).
        # the reason for this is: the page (here a panel) is
        # created with the default size and position (upper
        # left corner). Once the layout is applied, the page
        # is moved to the proper coordinates. However, the
        # wx.Notebook is not redrawn so it will leave a black
        # spot where the page was moved away from. Alternatively,
        # the frame or notebook can be Refresh()ed after the
        # frame is shown.
        wx.Panel.__init__(self, parent, size=(0,0))
        # create sizer to add a border
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        # create a grid sizer for the content
        self.grid = wx.GridSizer(0, 4, 5, 5)
        # add the grid sizer to the page sizer:
        # to allow the grid to fill the entire page,
        # set proportion>0 and add the wx.EXPAND flag.
        # the border of 10 is the spacing between the
        # page and the cells of the grid
        pageSizer.Add(self.grid, 1, wx.EXPAND|wx.ALL, 10)
        # set the main sizer:
        self.SetSizer(pageSizer)
        # add content to the grid
        self.GenerateContent()
        # DEMO: click any white space on the page to 
        # generate new content
        self.Bind(wx.EVT_LEFT_DOWN, self.GenerateContent)

    def GenerateContent(self, event=None):
        "dynamically create page content"
        # remove all items from the grid and destroy them
        # NOTE: if you don't actually create new controls here,
        # but use a list of controls created elsewhere (like in
        # in your code), do not delete the items! Use:
        # deleteWindows=False instead.
        self.grid.Clear(deleteWindows=True)
        # generate new grid content
        for i in range(10):
            # the contents are owned by the page,
            # therefore the page must be the parent window:
            # NOTE: size=(0,0) here is not required but
            # eliminates a briefly shown graphic artifact
            cell = wx.Panel(self, size=(0,0))
            cell.SetBackgroundColour(self.NewColor())
            # add the content (cells) to the grid:
            # specify the wx.EXPAND flag to fit the
            # content to the grid cell
            self.grid.Add(cell, flag=wx.EXPAND)
        # DEMO: hint text
        self.grid.Add(wx.StaticText(self, label=
            'Click empty cell to update content ->'),
                      flag=wx.EXPAND)
        # recalculate the layout to move the new contents
        # of the grid sizer into place
        self.Layout()

    col = 0 # DEMO: coloring
    def NewColor(self):
        self.col = (self.col + 3) % 241
        return wx.Colour(0, self.col * 10 % 255, self.col % 255)

app = wx.App(False)
MyFrame().Show()
app.MainLoop()