# -*- coding: utf-8 -*-
"""
/***************************************************************************
 stylecolor
                                 A QGIS plugin
 This plugin to make style color
                              -------------------
        begin                : 2017-07-31
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Hoa Le - GFD
        email                : hoa.lq@gfd.com.vn
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.utils import *

from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon, QColor, QFileDialog
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from style_color_dialog import stylecolorDialog
import os.path
from qgis.core import QgsMapLayerRegistry, QgsSymbolV2, QgsRendererCategoryV2, QgsCategorizedSymbolRendererV2

# from qgis.utils import iface
# from qgis.core import *
# from qgis.utils import *
# from qgis.gui import *

class stylecolor:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):

        self.iface = iface

        pluginName = 'Style color VN'
        userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/" + pluginName
        systemPluginPath = QgsApplication.prefixPath() + "/python/plugins/" + pluginName
        overrideLocale = bool(QSettings().value("locale/overrideFlag", False))

        # print 'userPluginPath: '+ userPluginPath
        if not overrideLocale:
            localeFullName = QLocale.system().name()
        else:
            localeFullName = QSettings().value("locale/userLocale", "")

        if QFileInfo(userPluginPath).exists():
            translationPath = userPluginPath + "/i18n/" + pluginName + "_" + localeFullName + ".qm"
        else:
            translationPath = systemPluginPath + "/i18n/" + pluginName + "_" + localeFullName + ".qm"
        # print translationPath
        self.localePath = translationPath

        if QFileInfo(self.localePath).exists():
            self.translator = QTranslator()
            self.translator.load(self.localePath)
            QCoreApplication.installTranslator(self.translator)
            # print('localepath exists')
            # print('translation debug info :' + ' overrideLocale=' + str(overrideLocale) + '; localeFullName=' +localeFullName + '; translationPath=' + translationPath )


        # Create the dialog (after translation) and keep reference
        self.dlgtool = stylecolorDialog()


    # noinspection PyMethodMayBeStatic
    def tr(self, message):

        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('stylecolor', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):

        # Create the dialog (after translation) and keep reference
        self.dlgtool = stylecolorDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        # Create actions triggered by the plugin
        self.actionRungkk = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon.png")),
                                   QtGui.QApplication.translate("Tô màu lớp bản đồ",
                                                                "1- Rừng kiểm kê", None,
                                                                QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())

        self.actionGthong = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon_gth.png")),
                                   QtGui.QApplication.translate("Tô màu lớp bản đồ",
                                                                "2- Giao thông", None,
                                                                QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())

        self.actionTv1 = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon_tv1.png")),
                                   QtGui.QApplication.translate("Tô màu lớp bản đồ",
                                                                "3- Thủy văn 1", None,
                                                                QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())

        self.actionTv2 = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon_tv2.png")),
                                   QtGui.QApplication.translate("Tô màu lớp bản đồ",
                                                                "4- Thủy văn 2 (polygon)", None,
                                                                QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())

        self.actionTk = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon_tk.png")),
                                   QtGui.QApplication.translate("Tô màu lớp bản đồ",
                                                                "5- RG tiểu khu", None,
                                                                QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())

        self.actionKh = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon_kh.png")),
                                QtGui.QApplication.translate("Tô màu lớp bản đồ",
                                                             "6- RG khoảnh", None,
                                                             QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())

        self.actionDh1 = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon_dh1.png")),
                                   QtGui.QApplication.translate("Tô màu lớp bản đồ",
                                                                "7- Địa hình 1 (_dh1)", None,
                                                                QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())

        self.actionDh2 = QAction(QIcon(os.path.join(os.path.dirname(__file__), "icon_dh2.png")),
                                QtGui.QApplication.translate("Tô màu lớp bản đồ",
                                                             "8- Địa hình 2 (_dh2)", None,
                                                             QtGui.QApplication.UnicodeUTF8), self.iface.mainWindow())

        # connect the action to the run method
        # self.iface.addToolBarIcon(self.actionRungkk)
        # self.iface.addToolBarIcon(self.actionGthong)
        # self.iface.addToolBarIcon(self.actionTv1)

        self.actionRungkk.triggered.connect(self.style_rungkk)
        self.actionGthong.triggered.connect(self.style_gthong)
        self.actionTv1.triggered.connect(self.style_tv1)
        self.actionTv2.triggered.connect(self.style_tv2)
        self.actionTk.triggered.connect(self.style_tk)
        self.actionKh.triggered.connect(self.style_kh)
        self.actionDh1.triggered.connect(self.style_dh1)
        self.actionDh2.triggered.connect(self.style_dh2)
        # adds buttons to labeling toolbar if exists

        self.toolBar = self.iface.pluginToolBar()
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None, QtGui.QApplication.UnicodeUTF8), self.actionRungkk)
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None, QtGui.QApplication.UnicodeUTF8), self.actionGthong)
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None, QtGui.QApplication.UnicodeUTF8), self.actionTv1)
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None, QtGui.QApplication.UnicodeUTF8), self.actionTv2)
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None, QtGui.QApplication.UnicodeUTF8), self.actionTk)
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None, QtGui.QApplication.UnicodeUTF8), self.actionKh)
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None, QtGui.QApplication.UnicodeUTF8), self.actionDh1)
        self.iface.addPluginToMenu( "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None, QtGui.QApplication.UnicodeUTF8), self.actionDh2)
    def unload(self):
        # Remove the plugin menu item and icon
        self.toolBar.removeAction(self.actionRungkk)
        self.toolBar.removeAction(self.actionGthong)
        self.toolBar.removeAction(self.actionTv1)
        self.toolBar.removeAction(self.actionTv2)
        self.toolBar.removeAction(self.actionTk)
        self.toolBar.removeAction(self.actionKh)
        self.toolBar.removeAction(self.actionDh1)
        self.toolBar.removeAction(self.actionDh2)
        self.toolBar.removeAction(self.actionKh)

        self.iface.removePluginMenu(
            "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None,
                                               QtGui.QApplication.UnicodeUTF8), self.actionRungkk)
        self.iface.removePluginMenu(
            "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None,
                                               QtGui.QApplication.UnicodeUTF8), self.actionGthong)
        self.iface.removePluginMenu(
            "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None,
                                               QtGui.QApplication.UnicodeUTF8), self.actionTv1)

        self.iface.removePluginMenu(
            "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None,
                                               QtGui.QApplication.UnicodeUTF8), self.actionTv2)

        self.iface.removePluginMenu(
            "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None,
                                               QtGui.QApplication.UnicodeUTF8), self.actionTk)

        self.iface.removePluginMenu(
            "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None,
                                               QtGui.QApplication.UnicodeUTF8), self.actionKh)

        self.iface.removePluginMenu(
            "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None,
                                               QtGui.QApplication.UnicodeUTF8), self.actionDh1)

        self.iface.removePluginMenu(
            "&" + QtGui.QApplication.translate("style_color", "Tô màu lớp bản đồ", None,
                                               QtGui.QApplication.UnicodeUTF8), self.actionDh2)




    def style_rungkk(self):
        #Select the layers open in TOC
        layers = self.iface.legendInterface().layers()
        layer_list =[]
        # Get only vector layer
        for layer in layers:
            if layer.type()==0:
                layer_list.append(layer.name())
            else:
                pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool.input_layer.clear()
        self.dlgtool.input_layer.addItems(layer_list)

        # show the dialog
        self.dlgtool.show()
        # Run the dialog event loop
        result = self.dlgtool.exec_()

        current_layer = self.dlgtool.input_layer.currentText()
        layer = QgsMapLayerRegistry.instance().mapLayersByName(str(current_layer))[0]

        ldlr_field = {
            'TXG1': ('#00D000', u'Rừng gỗ tự nhiên núi đất LRTX giàu nguyên sinh'),
            'TXB1': ('#00FF00', u'Rừng gỗ tự nhiên núi đất LRTX TB nguyên sinh'),
            'RLG1': ('#A0A000', u'Rừng gỗ tự nhiên núi đất LRRL giàu nguyên sinh'),
            'RLB1': ('#C0C000', u'Rừng gỗ tự nhiên núi đất LRRL TB nguyên sinh'),
            'LKG1': ('#FF505A', u'Rừng gỗ tự nhiên núi đất LK giàu nguyên sinh'),
            'LKB1': ('#FF6982', u'Rừng gỗ tự nhiên núi đất LK TB nguyên sinh'),
            'RKG1': ('#FFA0D0', u'Rừng gỗ tự nhiên núi đất LRLK giàu nguyên sinh'),
            'RKB1': ('#FFA0D0', u'Rừng gỗ tự nhiên núi đất LRLK TB nguyên sinh'),
            'TXDG1': ('#00D068', u'Rừng gỗ tự nhiên núi đá LRTX giàu nguyên sinh'),
            'TXDB1': ('#00FF80', u'Rừng gỗ tự nhiên núi đá LRTX TB nguyên sinh'),
            'RNM1': ('#7070FF', u'Rừng gỗ tự nhiên ngập mặn nguyên sinh'),
            'RNP1': ('#A850FF', u'Rừng gỗ tự nhiên ngập phèn nguyên sinh'),
            'RNN1': ('#E8D0FF', u'Rừng gỗ tự nhiên ngập ngọt nguyên sinh'),
            'TXG': ('#00D000', u'Rừng gỗ tự nhiên núi đất LRTX giàu'),
            'TXB': ('#00FF00', u'Rừng gỗ tự nhiên núi đất LRTX TB'),
            'TXN': ('#90FF90', u'Rừng gỗ tự nhiên núi đất LRTX nghèo'),
            'TXK': ('#B0FFB0', u'Rừng gỗ tự nhiên núi đất LRTX nghèo kiệt'),
            'TXP': ('#B3FF40', u'Rừng gỗ tự nhiên núi đất LRTX phục hồi'),
            'RLG': ('#A0A000', u'Rừng gỗ tự nhiên núi đất LRRL giàu'),
            'RLB': ('#C0C000', u'Rừng gỗ tự nhiên núi đất LRRL TB'),
            'RLN': ('#E0E000', u'Rừng gỗ tự nhiên núi đất LRRL nghèo'),
            'RLK': ('#F0F000', u'Rừng gỗ tự nhiên núi đất LRRL nghèo kiệt'),
            'RLP': ('#EBFF00', u'Rừng gỗ tự nhiên núi đất LRRL phục hồi'),
            'LKG': ('#FF505A', u'Rừng gỗ tự nhiên núi đất LK giàu'),
            'LKB': ('#FF6982', u'Rừng gỗ tự nhiên núi đất LK TB'),
            'LKN': ('#FF8690', u'Rừng gỗ tự nhiên núi đất LK nghèo'),
            'LKK': ('#FF9A90', u'Rừng gỗ tự nhiên núi đất LK nghèo kiệt'),
            'LKP': ('#FFB0B0', u'Rừng gỗ tự nhiên núi đất LK phục hồi'),
            'RKG': ('#FFA0D0', u'Rừng gỗ tự nhiên núi đất LRLK giàu'),
            'RKB': ('#FFA0D0', u'Rừng gỗ tự nhiên núi đất LRLK TB'),
            'RKN': ('#FFA0D0', u'Rừng gỗ tự nhiên núi đất LRLK nghèo'),
            'RKK': ('#FFA0D0', u'Rừng gỗ tự nhiên núi đất LRLK nghèo kiệt'),
            'RKP': ('#FFA0D0', u'Rừng gỗ tự nhiên núi đất LRLK phục hồi'),
            'TXDG': ('#00D068', u'Rừng gỗ tự nhiên núi đá LRTX giàu'),
            'TXDB': ('#00FF80', u'Rừng gỗ tự nhiên núi đá LRTX TB'),
            'TXDN': ('#60FFB0', u'Rừng gỗ tự nhiên núi đá LRTX nghèo'),
            'TXDK': ('#A0FFD0', u'Rừng gỗ tự nhiên núi đá LRTX nghèo kiệt'),
            'TXDP': ('#D0FFE8', u'Rừng gỗ tự nhiên núi đá LRTX phục hồi'),
            'RNMG': ('#7070FF', u'Rừng gỗ tự nhiên ngập mặn giàu'),
            'RNMB': ('#9090FF', u'Rừng gỗ tự nhiên ngập mặn trung bình'),
            'RNMN': ('#C0C0FF', u'Rừng gỗ tự nhiên ngập mặn nghèo'),
            'RNMP': ('#D0D0FF', u'Rừng gỗ tự nhiên ngập mặn phục hồi'),
            'RNPG': ('#A850FF', u'Rừng gỗ tự nhiên ngập phèn giàu'),
            'RNPB': ('#C080FF', u'Rừng gỗ tự nhiên ngập phèn trung bình'),
            'RNPN': ('#D0A0FF', u'Rừng gỗ tự nhiên ngập phèn nghèo'),
            'RNPP': ('#D8B0FF', u'Rừng gỗ tự nhiên ngập phèn phục hồi'),
            'RNN': ('#E8D0FF', u'Rừng gỗ tự nhiên ngập ngọt'),
            'TLU': ('#D0E0FF', u'Rừng tre/luồng tự nhiên núi đất'),
            'NUA': ('#D0E0FF', u'Rừng nứa tự nhiên núi đất'),
            'VAU': ('#D0E0FF', u'Rừng vầu tự nhiên núi đất'),
            'LOO': ('#D0E0FF', u'Rừng lồ ô tự nhiên núi đất'),
            'TNK': ('#D0E0FF', u'Rừng tre nứa khác tự nhiên núi đất'),
            'TND': ('#D0E0FF', u'Rừng tre nứa tự nhiên núi đá'),
            'HG1': ('#FFD0FF', u'Rừng hỗn giao G-TN tự nhiên núi đất '),
            'HG2': ('#FFD0FF', u'Rừng hỗn giao TN-G tự nhiên núi đất '),
            'HGD': ('#FFD0FF', u'Rừng hỗn giao tự nhiên núi đá'),
            'CD': ('#C0C0FF', u'Rừng cau dừa tự nhiên núi đất'),
            'CDD': ('#C0C0FF', u'Rừng cau dừa tự nhiên núi đá'),
            'CDN': ('#C0C0FF', u'Rừng cau dừa tự nhiên ngập nước ngọt'),
            'RTG': ('#FFD8B0', u'Rừng gỗ trồng núi đất'),
            'RTGD': ('#FFC080', u'Rừng gỗ trồng núi đá'),
            'RTM': ('#FFC080', u'Rừng gỗ trồng ngập mặn'),
            'RTP': ('#FFC080', u'Rừng gỗ trồng ngập phèn'),
            'RTC': ('#FFC080', u'Rừng gỗ trồng đất cát'),
            'RTTN': ('#FFC080', u'Rừng tre nứa trồng núi đất'),
            'RTTND': ('#FFC080', u'Rừng tre nứa trồng núi đá'),
            'RTCD': ('#FFC080', u'Rừng cau dừa trồng cạn'),
            'RTCDN': ('#FFD8B0', u'Rừng cau dừa trồng ngập nước'),
            'RTCDC': ('#FFC080', u'Rừng cau dừa trồng đất cát'),
            'RTK': ('#FFC080', u'Rừng trồng khác núi đất'),
            'RTKD': ('#FFE490', u'Rừng trồng khác núi đá'),
            'DTR': ('#FFE8D0', u'Đất đã trồng trên núi đất'),
            'DTRD': ('#FFE8D0', u'Đất đã trồng trên núi đá'),
            'DTRM': ('#FFE8D0', u'Đất đã trồng trên đất ngập mặn'),
            'DTRP': ('#FFE8D0', u'Đất đã trồng trên đất ngập phèn'),
            'DTRN': ('#FFE8D0', u'Đất đã trồng trên đất ngập ngọt'),
            'DTRC': ('#FFE8D0', u'Đất đã trồng trên bãi cát'),
            'DT2': ('#006000', u'Đất có cây gỗ tái sinh núi đất'),
            'DT2D': ('#006000', u'Đất có cây gỗ tái sinh núi đá'),
            'DT2M': ('#006000', u'Đất có cây gỗ tái sinh ngập mặn'),
            'DT2P': ('#006000', u'Đất có cây tái sinh ngập nước phèn'),
            'DT1': ('#00FF00', u'Đất trống núi đất'),
            'DT1D': ('#E0E0E0', u'Đất trống núi đá'),
            'DT1M': ('#00FF00', u'Đất trống ngập mặn'),
            'DT1P': ('#00FF00', u'Đất trống ngập nước phèn'),
            'BC1': ('#808080', u'Bãi cát'),
            'BC2': ('#00FF00', u'Bãi cát có cây rải rác'),
            'NN': ('#FFFF90', u'Đất nông nghiệp núi đất'),
            'NND': ('#FFFF90', u'Đất nông nghiệp núi đá'),
            'NNM': ('#FFFF90', u'Đất nông nghiệp ngập mặn'),
            'NNP': ('#FFFF90', u'Đất nông nghiệp ngập nước ngọt'),
            'MN': ('#A0FFFF', u'Mặt nước '),
            'DKH': ('#808080', u'Đất khác'),
            # Ma bo sung mot so truong hop
            'NL': ('#FFFF90', u'Đất nông nghiệp núi đất'),
            'NLD': ('#FFFF90', u'Đất nông nghiệp núi đá'),
            'NLM': ('#FFFF90', u'Đất nông nghiệp ngập mặn'),
            'NLP': ('#FFFF90', u'Đất nông nghiệp ngập nước ngọt'),
            'DK': ('#808080', u'Đất khác')
        }

        # Define style parameters: value, colour, legend
        arr = {}


        for feature in layer.getFeatures():
            name = feature["ldlr"]
            arr[name] = ldlr_field[name]

            # Define a list for categories
            categories = []
            # Define symbology depending on layer type, set the relevant style parameters
            for classes, (color, label) in arr.items():
                symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
                symbol.setColor(QColor(color))
                category = QgsRendererCategoryV2(classes,symbol, label)
                categories.append(category)

                # Column/field name to be used to read values from
            column = 'ldlr'
            # Apply the style rendering
            renderer = QgsCategorizedSymbolRendererV2(column, categories)
            layer.setRendererV2(renderer)

            # Refresh the layer
            layer.triggerRepaint()


    def style_gthong(self):
        #Select the layers open in TOC
        layers = self.iface.legendInterface().layers()
        layer_list =[]
        # Get only vector layer
        for layer in layers:
            if layer.type()==0:
                layer_list.append(layer.name())
            else:
                pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool.input_layer.clear()
        self.dlgtool.input_layer.addItems(layer_list)

        # show the dialog
        self.dlgtool.show()
        # Run the dialog event loop
        result = self.dlgtool.exec_()
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

        symbol_gth = QgsLineSymbolV2.createSimple({'penstyle': 'solid',
                                                   'color': '#FF0000',
                                                   'width': '0.26'
                                                   })
        current_layer = self.dlgtool.input_layer.currentText()
        layer = QgsMapLayerRegistry.instance().mapLayersByName(str(current_layer))[0]

        renderer = layer.rendererV2()
        symbol_layer2 = symbol_gth.symbolLayer(0)
        renderer.setSymbol(symbol_gth)
        layer.triggerRepaint()
        iface.legendInterface().refreshLayerSymbology(layer)



    def style_tv1(self):
        #Select the layers open in TOC
        layers = self.iface.legendInterface().layers()
        layer_list =[]
        # Get only vector layer
        for layer in layers:
            if layer.type()==0:
                layer_list.append(layer.name())
            else:
                pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool.input_layer.clear()
        self.dlgtool.input_layer.addItems(layer_list)

        # show the dialog
        self.dlgtool.show()
        # Run the dialog event loop
        result = self.dlgtool.exec_()
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

        symbol_tv1 = QgsLineSymbolV2.createSimple({'penstyle': 'solid',
                                                   'color': '#70FFFF',
                                                   'width': '0.26'
                                                   })
        current_layertv1 = self.dlgtool.input_layer.currentText()
        layertv = QgsMapLayerRegistry.instance().mapLayersByName(str(current_layertv1))[0]

        renderertv1 = layertv.rendererV2()
        symbol_layer2 = symbol_tv1.symbolLayer(0)
        renderertv1.setSymbol(symbol_tv1)
        layertv.triggerRepaint()
        iface.legendInterface().refreshLayerSymbology(layertv)

    def style_tv2(self):
        # Select the layers open in TOC
        layers = self.iface.legendInterface().layers()
        layer_list = []
        # Get only vector layer
        for layer in layers:
            if layer.type() == 0:
                layer_list.append(layer.name())
            else:
                pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool.input_layer.clear()
        self.dlgtool.input_layer.addItems(layer_list)

        # show the dialog
        self.dlgtool.show()
        # Run the dialog event loop
        result = self.dlgtool.exec_()
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
        symbol_tv2 = QgsFillSymbolV2.createSimple({'color': '#70FFFF',
                                                   'color_border': '#00FFFF',
                                                   'width_border': '0.26'})

        current_layertv2 = self.dlgtool.input_layer.currentText()
        layertv = QgsMapLayerRegistry.instance().mapLayersByName(str(current_layertv2))[0]

        renderertv2 = layertv.rendererV2()
        symbol_layer2 = symbol_tv2.symbolLayer(0)
        renderertv2.setSymbol(symbol_tv2)
        layertv.triggerRepaint()
        iface.legendInterface().refreshLayerSymbology(layertv)

    def style_tk(self):
        #Select the layers open in TOC
        layers = self.iface.legendInterface().layers()
        layer_list =[]
        # Get only vector layer
        for layer in layers:
            if layer.type()==0:
                layer_list.append(layer.name())
            else:
                pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool.input_layer.clear()
        self.dlgtool.input_layer.addItems(layer_list)

        # show the dialog
        self.dlgtool.show()
        # Run the dialog event loop
        result = self.dlgtool.exec_()
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

        current_layertk = self.dlgtool.input_layer.currentText()
        layertk = QgsMapLayerRegistry.instance().mapLayersByName(str(current_layertk))[0]

        registry = QgsSymbolLayerV2Registry.instance()
        lineMeta = registry.symbolLayerMetadata("SimpleLine")
        markerMeta = registry.symbolLayerMetadata("MarkerLine")
        symbol = QgsSymbolV2.defaultSymbol(layertk.geometryType())

        # Line layer
        lineLayer = lineMeta.createSymbolLayer(
            {'width': '0.36', 'color': '#0000FF', 'penstyle': 'dashDotVector', 'use_custom_dash': '1',
             'joinstyle': 'bevel', 'capstyle': 'square'})
        # Marker layer
        markerLayer = markerMeta.createSymbolLayer(
            {'width': '0.26', 'color': '#0000FF', 'interval': '3', 'placement': 'interval'})
        subSymbol = markerLayer.subSymbol()

        # Replace the default layer with our own SimpleMarker
        subSymbol.deleteSymbolLayer(0)
        triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer(
            {'name': 'line', 'color': '#0000FF', 'color_border': '#0000FF', 'offset': '0,0', 'size': '1.2',
             'angle': '0'})
        subSymbol.appendSymbolLayer(triangle)

        # Replace the default layer with our two custom layers
        symbol.deleteSymbolLayer(0)
        symbol.appendSymbolLayer(lineLayer)
        symbol.appendSymbolLayer(markerLayer)


        # Replace the renderer of the current layer
        renderer = QgsSingleSymbolRendererV2(symbol)
        layertk.setRendererV2(renderer)

        layer.triggerRepaint()
        iface.legendInterface().refreshLayerSymbology(layer)

    def style_kh(self):
        #Select the layers open in TOC
        layers = self.iface.legendInterface().layers()
        layer_list =[]
        # Get only vector layer
        for layer in layers:
            if layer.type()==0:
                layer_list.append(layer.name())
            else:
                pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool.input_layer.clear()
        self.dlgtool.input_layer.addItems(layer_list)

        # show the dialog
        self.dlgtool.show()
        # Run the dialog event loop
        result = self.dlgtool.exec_()
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

        current_layertk = self.dlgtool.input_layer.currentText()
        layerkh = QgsMapLayerRegistry.instance().mapLayersByName(str(current_layertk))[0]

        registry = QgsSymbolLayerV2Registry.instance()
        lineMeta = registry.symbolLayerMetadata("SimpleLine")
        markerMeta = registry.symbolLayerMetadata("MarkerLine")
        symbol = QgsSymbolV2.defaultSymbol(layerkh.geometryType())

        # Line layer
        lineLayer = lineMeta.createSymbolLayer(
            {'width': '0.28', 'color': '#000000', 'penstyle': 'dashDotVector', 'use_custom_dash': '1',
             'joinstyle': 'bevel', 'capstyle': 'square'})
        # Marker layer
        markerLayer = markerMeta.createSymbolLayer(
            {'width': '0.26', 'color': '#000000', 'interval': '2', 'placement': 'interval'})
        subSymbol = markerLayer.subSymbol()

        # Replace the default layer with our own SimpleMarker
        subSymbol.deleteSymbolLayer(0)
        triangle = registry.symbolLayerMetadata("SimpleMarker").createSymbolLayer(
            {'name': 'line', 'color': '#000000', 'color_border': '#000000', 'offset': '0,0', 'size': '1.0',
             'angle': '0'})
        subSymbol.appendSymbolLayer(triangle)

        # Replace the default layer with our two custom layers
        symbol.deleteSymbolLayer(0)
        symbol.appendSymbolLayer(lineLayer)
        symbol.appendSymbolLayer(markerLayer)


        # Replace the renderer of the current layer
        renderer = QgsSingleSymbolRendererV2(symbol)
        layerkh.setRendererV2(renderer)

        layer.triggerRepaint()
        iface.legendInterface().refreshLayerSymbology(layer)


    def style_dh1(self):
        #Select the layers open in TOC
        layers = self.iface.legendInterface().layers()
        layer_list =[]
        # Get only vector layer
        for layer in layers:
            if layer.type()==0:
                layer_list.append(layer.name())
            else:
                pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool.input_layer.clear()
        self.dlgtool.input_layer.addItems(layer_list)

        # show the dialog
        self.dlgtool.show()
        # Run the dialog event loop
        result = self.dlgtool.exec_()
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

        symbol_dh1 = QgsLineSymbolV2.createSimple({'penstyle': 'solid',
                                                   'color': '#FF7C50',
                                                   'width': '0.3'
                                                   })
        current_layerdh1 = self.dlgtool.input_layer.currentText()
        layerdh1 = QgsMapLayerRegistry.instance().mapLayersByName(str(current_layerdh1))[0]

        rendererdh1 = layerdh1.rendererV2()
        symbol_layer2 = symbol_dh1.symbolLayer(0)
        rendererdh1.setSymbol(symbol_dh1)
        layerdh1.triggerRepaint()
        iface.legendInterface().refreshLayerSymbology(layerdh1)

    def style_dh2(self):
        #Select the layers open in TOC
        layers = self.iface.legendInterface().layers()
        layer_list =[]
        # Get only vector layer
        for layer in layers:
            if layer.type()==0:
                layer_list.append(layer.name())
            else:
                pass
        # Add layer_list array to listWidget, clear layer if removed to layer in tools
        self.dlgtool.input_layer.clear()
        self.dlgtool.input_layer.addItems(layer_list)

        # show the dialog
        self.dlgtool.show()
        # Run the dialog event loop
        result = self.dlgtool.exec_()
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

        symbol_dh2 = QgsLineSymbolV2.createSimple({'penstyle': 'solid',
                                                   'color': '#FF7C50',
                                                   'width': '0.15'
                                                   })
        current_layerdh2 = self.dlgtool.input_layer.currentText()
        layerdh2 = QgsMapLayerRegistry.instance().mapLayersByName(str(current_layerdh2))[0]

        rendererdh2 = layerdh2.rendererV2()
        symbol_layer2 = symbol_dh2.symbolLayer(0)
        rendererdh2.setSymbol(symbol_dh2)
        layerdh2.triggerRepaint()
        iface.legendInterface().refreshLayerSymbology(layerdh2)




