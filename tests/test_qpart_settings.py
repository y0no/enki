#!/usr/bin/env python

import unittest

import base

from PyQt4.QtCore import Qt
from PyQt4.QtTest import QTest
from PyQt4.QtGui import QColor, QFont, QPlainTextEdit, QTextOption

from enki.core.core import core


class Font(base.TestCase):
    def test_1(self):
        font = QFont("Arial", 88)
        
        def continueFunc(dialog):
            page = dialog._pageForItem["Editor/Font"]
            
            page.lFont.setFont(font)
            
            QTest.keyClick(dialog, Qt.Key_Enter)
        
        self.openSettings(continueFunc)
        
        self.assertEqual(core.config()['Qutepart']['Font']['Family'], font.family())
        self.assertEqual(core.config()['Qutepart']['Font']['Size'], font.pointSize())
        
        self.assertEqual(core.workspace().currentDocument().qutepart.font(), font)


class Indent(base.TestCase):
    def _do_test(self, useTabs, width, autoDetect):
        def continueFunc(dialog):
            page = dialog._pageForItem["Editor/Indentation"]
            
            if useTabs:
                page.rbIndentationTabs.setChecked(True)
            else:
                page.rbIndentationSpaces.setChecked(True)
            
            page.sIndentationWidth.setValue(width)
            page.cbAutodetectIndent.setChecked(autoDetect)
            
            QTest.keyClick(dialog, Qt.Key_Enter)
        
        self.openSettings(continueFunc)
        
        self.assertEqual(core.config()['Qutepart']['Indentation']['UseTabs'], useTabs)
        self.assertEqual(core.config()['Qutepart']['Indentation']['Width'], width)
        self.assertEqual(core.config()['Qutepart']['Indentation']['AutoDetect'], autoDetect)
        
        self.assertEqual(core.workspace().currentDocument().qutepart.indentUseTabs, useTabs)
        self.assertEqual(core.workspace().currentDocument().qutepart.indentWidth, width)
    
    def test_1(self):
        self._do_test(True, 4, False)
    
    def test_2(self):
        self._do_test(False, 8, True)


class AutoCompletion(base.TestCase):
    def _do_test(self, enabled, threshold):
        def continueFunc(dialog):
            page = dialog._pageForItem["Editor/Autocompletion"]
            
            page.gbAutoCompletion.setChecked(enabled)
            page.sThreshold.setValue(threshold)
            
            self.assertTrue(page.lcdNumber.value(), threshold)
            
            QTest.keyClick(dialog, Qt.Key_Enter)
        
        self.openSettings(continueFunc)
        
        self.assertEqual(core.config()['Qutepart']['AutoCompletion']['Enabled'], enabled)
        self.assertEqual(core.config()['Qutepart']['AutoCompletion']['Threshold'], threshold)
        
        self.assertEqual(core.workspace().currentDocument().qutepart.completionEnabled, enabled)
        self.assertEqual(core.workspace().currentDocument().qutepart.completionThreshold, threshold)
    
    def test_1(self):
        self._do_test(False, 2)
    
    def test_2(self):
        self._do_test(True, 6)


class Edge(base.TestCase):
    def _do_test(self, enabled, width, colorName):
        def continueFunc(dialog):
            page = dialog._pageForItem["Editor/Edge"]
            
            page.gbEdgeEnabled.setChecked(enabled)
            page.sEdgeColumnNumber.setValue(width)
            page.tbEdgeColor.setColor(QColor(colorName))
            
            dialog.accept()

        self.openSettings(continueFunc)

        self.assertEqual(core.config()['Qutepart']['Edge']['Enabled'], enabled)
        self.assertEqual(core.config()['Qutepart']['Edge']['Column'], width)
        self.assertEqual(core.config()['Qutepart']['Edge']['Color'], colorName)
        
        self.assertEqual(core.workspace().currentDocument().qutepart.lineLengthEdge,
                         width if enabled else None)
        self.assertEqual(core.workspace().currentDocument().qutepart.lineLengthEdgeColor.name(), colorName)
    
    def test_1(self):
        self._do_test(True, 80, '#ff0000')
    
    def test_2(self):
        self._do_test(False, 80, '#ff0000')
    
    def test_3(self):
        self._do_test(True, 120, '#ff0000')
    
    def test_4(self):
        self._do_test(True, 120, '#00ff00')


class Eol(base.TestCase):
    def _do_test(self, mode, autoDetect):
        def continueFunc(dialog):
            page = dialog._pageForItem["Editor/EOL"]
            
            if mode == r'\n':
                page.rbEolUnix.setChecked(True)
            elif mode == r'\r\n':
                page.rbEolWindows.setChecked(True)
            elif mode == r'\r':
                page.rbEolMac.setChecked(True)
            else:
                assert 0
            
            if page.cbAutoDetectEol.isChecked() != autoDetect:
                QTest.mouseClick(page.cbAutoDetectEol, Qt.LeftButton)
            
            self.assertEqual(not page.lReloadToReapply.isHidden(), autoDetect)
            
            QTest.keyClick(dialog, Qt.Key_Enter)
        
        self.openSettings(continueFunc)

        self.assertEqual(core.config()['Qutepart']['EOL']['Mode'], mode)
        self.assertEqual(core.config()['Qutepart']['EOL']['AutoDetect'], autoDetect)
        
        conv = {r'\n': '\n',
                r'\r\n': '\r\n',
                r'\r': '\r'}
        
        if not autoDetect:  # if autodetection is active - not applied
            self.assertEqual(core.workspace().currentDocument().qutepart.eol, conv[mode])

    def test_1(self):
        self._do_test(r'\n', False)
    
    def test_2(self):
        self._do_test(r'\r\n', False)
    
    def test_3(self):
        self._do_test(r'\r', False)
    
    def test_4(self):        
        self._do_test(r'\n', True)


class Wrap(base.TestCase):
    def _do_test(self, enabled, atWord, lineWrapMode, wordWrapMode, wordWrapText):
        def continueFunc(dialog):
            page = dialog._pageForItem["Editor/Wrap"]
            
            page.gbWrapEnabled.setChecked(enabled)
            if atWord:
                page.rbWrapAtWord.setChecked(True)
            else:
                page.rbWrapAnywhere.setChecked(True)
            
            QTest.keyClick(dialog, Qt.Key_Enter)
            
        self.openSettings(continueFunc)
        
        self.assertEqual(core.config()['Qutepart']['Wrap']['Enabled'], enabled)
        self.assertEqual(core.config()['Qutepart']['Wrap']['Mode'], wordWrapText)
        
        self.assertEqual(core.workspace().currentDocument().qutepart.lineWrapMode(),
                         lineWrapMode)
        self.assertEqual(core.workspace().currentDocument().qutepart.wordWrapMode(),
                         wordWrapMode)


    def test_1(self):
        self._do_test(True, True, QPlainTextEdit.WidgetWidth, QTextOption.WrapAtWordBoundaryOrAnywhere, "WrapAtWord")
    
    def test_2(self):
        self._do_test(True, False, QPlainTextEdit.WidgetWidth, QTextOption.WrapAnywhere, "WrapAnywhere")
    
    def test_3(self):
        self._do_test(False, False, QPlainTextEdit.NoWrap, QTextOption.WrapAnywhere, "WrapAnywhere")


if __name__ == '__main__':
    unittest.main()
