# Copyright (C) 2006-2007 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from sugar.graphics.icon import CanvasIcon
from sugar.graphics import style

from jarabe.view.buddymenu import BuddyMenu

class BuddyIcon(CanvasIcon):
    def __init__(self, buddy, size=style.STANDARD_ICON_SIZE):
        CanvasIcon.__init__(self, icon_name='computer-xo', size=size)

        self._greyed_out = False
        self._buddy = buddy
        self._buddy.connect('notify::present', self.__buddy_notify_present_cb)
        self._buddy.connect('notify::color', self.__buddy_notify_color_cb)

        palette = BuddyMenu(buddy)
        self.set_palette(palette)

        self._update_color()

    def __buddy_notify_present_cb(self, buddy, pspec):
        # Update the icon's color when the buddy comes and goes
        self._update_color()

    def __buddy_notify_color_cb(self, buddy, pspec):
        self._update_color()

    def _update_color(self):

        # keep the icon in the palette in sync with the view
        palette = self.get_palette()
        palette_icon = palette.props.icon

        if self._greyed_out:
            self.props.stroke_color = '#D5D5D5'
            self.props.fill_color = style.COLOR_TRANSPARENT.get_svg()
            palette_icon.props.stroke_color = '#D5D5D5'
            palette_icon.props.fill_color = style.COLOR_TRANSPARENT.get_svg()
        else:
            self.props.xo_color = self._buddy.get_color()
            palette_icon.props.xo_color = self._buddy.get_color()

    def set_filter(self, query):
        self._greyed_out = (self._buddy.get_nick().lower().find(query) == -1) \
                and not self._buddy.is_owner()
        self._update_color()

