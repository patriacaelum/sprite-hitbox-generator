import os
import wx

from canvas import Canvas
from enums import State
from inspector import Inspector


IMAGE_WILDCARD = "JPG files (*.jpg)|*.jpg|PNG files (*.png)|*.png"
JSON_WILDCARD = "JSON files (*.json)|*.json"


class SpriteHitboxGenerator(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(
            parent=parent,
            id=wx.ID_ANY,
            title="sprite-hitbox-generator",
            pos=wx.DefaultPosition,
            size=wx.Size(640, 480),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        # Main panel
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)

        self.canvas = Canvas(parent=self)
        main_sizer.Add(
            window=self.canvas,
            proportion=1,
            flag=wx.ALL | wx.EXPAND,
            border=5,
        )

        self.inspector = Inspector(parent=self)
        main_sizer.Add(
            window=self.inspector,
            proportion=1,
            flag=wx.ALL | wx.EXPAND,
            border=5,
        )

        self.SetSizer(main_sizer)
        self.Layout()

        self.InitMenuBar()
        self.InitToolBar()

        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_MENU, self.onFileMenuNew, id=self.file_menu_new.GetId())
        self.Bind(wx.EVT_MENU, self.onFileMenuOpen, id=self.file_menu_open.GetId())
        self.Bind(wx.EVT_MENU, self.onFileMenuSave, id=self.file_menu_save.GetId())
        self.Bind(wx.EVT_MENU, self.onFileMenuExit, id=self.file_menu_exit.GetId())

        self.Bind(wx.EVT_TOOL, self.onToolMove, id=self.tool_move.GetId())
        self.Bind(wx.EVT_TOOL, self.onToolDraw, id=self.tool_draw.GetId())
        self.Bind(wx.EVT_TOOL, self.onToolColourPicker, id=self.tool_colour_picker.GetId())

    def InitFileMenu(self):
        self.file_menu = wx.Menu()

        self.file_menu_new = wx.MenuItem(
            parentMenu=self.file_menu,
            id=wx.ID_ANY,
            text="New\tCTRL+N",
            helpString=wx.EmptyString,
            kind=wx.ITEM_NORMAL,
        )
        self.file_menu.Append(self.file_menu_new)

        self.file_menu.AppendSeparator()

        self.file_menu_open = wx.MenuItem(
            parentMenu=self.file_menu,
            id=wx.ID_ANY,
            text="Open\tCTRL+O",
            helpString=wx.EmptyString,
            kind=wx.ITEM_NORMAL,
        )
        self.file_menu.Append(self.file_menu_open)

        self.file_menu.AppendSeparator()

        self.file_menu_close = wx.MenuItem(
            parentMenu=self.file_menu,
            id=wx.ID_ANY,
            text="Close\tCTRL+W",
            helpString=wx.EmptyString,
            kind=wx.ITEM_NORMAL,
        )
        self.file_menu.Append(self.file_menu_close)
        
        self.file_menu.AppendSeparator()

        self.file_menu_save = wx.MenuItem(
            parentMenu=self.file_menu,
            id=wx.ID_ANY,
            text="Save\tCTRL+S",
            helpString=wx.EmptyString,
            kind=wx.ITEM_NORMAL,
        )
        self.file_menu.Append(self.file_menu_save)

        self.file_menu.AppendSeparator()

        self.file_menu_exit = wx.MenuItem(
            parentMenu=self.file_menu,
            id=wx.ID_ANY,
            text="Exit\tCTRL+Q",
            helpString=wx.EmptyString,
            kind=wx.ITEM_NORMAL,
        )
        self.file_menu.Append(self.file_menu_exit)

    def InitMenuBar(self):
        self.menu_bar = wx.MenuBar(0)

        self.InitFileMenu()
        self.menu_bar.Append(self.file_menu, "File")

        self.SetMenuBar(self.menu_bar)

    def InitToolBar(self):
        self.tool_bar = self.CreateToolBar(
            style=wx.TB_VERTICAL,
            id=wx.ID_ANY,
        )

        self.tool_move = self.tool_bar.AddTool(
            toolId=wx.ID_ANY,
            label="Move",
            bitmap=wx.Bitmap(name="assets/tool_move.png"),
            bmpDisabled=wx.NullBitmap,
            kind=wx.ITEM_CHECK,
            shortHelp=wx.EmptyString,
            longHelp=wx.EmptyString,
            clientData=None,
        )

        self.tool_bar.AddSeparator()

        self.tool_draw = self.tool_bar.AddTool(
            toolId=wx.ID_ANY,
            label="Draw",
            bitmap=wx.Bitmap(name="assets/tool_draw.png"),
            bmpDisabled=wx.NullBitmap,
            kind=wx.ITEM_CHECK,
            shortHelp=wx.EmptyString,
            longHelp=wx.EmptyString,
            clientData=None,
        )

        self.tool_bar.AddSeparator()

        self.tool_colour_picker = self.tool_bar.AddTool(
            toolId=wx.ID_ANY,
            label="Colour Picker",
            bitmap=wx.Bitmap(name="assets/tool_colour_picker.png"),
            bmpDisabled=wx.NullBitmap,
            kind=wx.ITEM_NORMAL,
            shortHelp=wx.EmptyString,
            longHelp=wx.EmptyString,
            clientData=None,
        )

        self.tool_bar.Realize()

        self.tool_bar.ToggleTool(self.tool_move.GetId(), True)

    def Open(self):
        """Create and show the `wx.FileDialog` to open an image."""
        with wx.FileDialog(
                    parent=self,
                    message="Select a file to open",
                    defaultDir=os.getcwd(),
                    defaultFile="",
                    wildcard=IMAGE_WILDCARD,
                    style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
                ) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return

            self.canvas.LoadImage(dialog.GetPath())

        self.Refresh()

    def Save(self):
        """Create and show the `wx.FileDialog` to save the current canvas."""
        with wx.FileDialog(
                    parent=self,
                    message="Save hitbox data",
                    wildcard=JSON_WILDCARD,
                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
                ) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return

            self.canvas.Save(dialog.GetPath())

        self.canvas.saved = True

    def onFileMenuExit(self, event):
        """Asks to save the current canvas and exits the program."""
        self.Save()
        self.Close()

    def onFileMenuNew(self, event):
        self.Open()

    def onFileMenuOpen(self, event):
        """Create and show the `wx.FileDialog` to open a file."""
        if not self.canvas.saved:
            confirm_continue = wx.MessageBox(
                message="Current file has not been saved. Continue?",
                caption="Current canvas not saved",
                style=wx.ICON_QUESTION | wx.YES_NO,
                parent=self
            )

            if confirm_continue == wx.NO:
                return

        self.Open()

    def onFileMenuSave(self, event):
        """Create and show the `wx.FileDialog` to save the current canvas."""
        self.Save()

    def onToolColourPicker(self, event):
        """Opens the colour dialog and sets the draw colour."""
        with wx.ColourDialog(parent=self) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return

            colour = dialog.GetColourData().GetColour()

            self.canvas.hitbox_colour.Set(
                red=colour.red,
                green=colour.green,
                blue=colour.blue,
            )

        self.Refresh()

    def onToolDraw(self, event):
        """Toggles the draw tool on."""
        self.canvas.state = State.DRAW
        self.canvas.hitbox_select = None

        self.tool_bar.ToggleTool(self.tool_draw.GetId(), True)
        self.tool_bar.ToggleTool(self.tool_move.GetId(), False)

        self.Refresh()

    def onToolMove(self, event):
        """Toggles the move tool on."""
        self.canvas.state = State.MOVE

        self.tool_bar.ToggleTool(self.tool_draw.GetId(), False)
        self.tool_bar.ToggleTool(self.tool_move.GetId(), True)

        self.Refresh()
