# Copyright (c) DataLab Platform Developers, BSD 3-Clause license, see LICENSE file.

"""
DataLab Remote client connection dialog example
"""

# guitest: show

from guidata.qthelpers import qt_app_context
from qtpy import QtWidgets as QW

from cdlclient import SimpleRemoteProxy
from cdlclient.widgets import ConnectionDialog


def test_dialog():
    """Test connection dialog"""
    proxy = SimpleRemoteProxy(autoconnect=False)
    with qt_app_context():
        dlg = ConnectionDialog(proxy.connect)
        if dlg.exec():
            QW.QMessageBox.information(None, "Connection", "Successfully connected")
        else:
            QW.QMessageBox.critical(None, "Connection", "Connection failed")


if __name__ == "__main__":
    test_dialog()
