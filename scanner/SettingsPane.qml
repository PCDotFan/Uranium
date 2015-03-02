import QtQuick 2.1
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import QtQuick.Window 2.
import QtQuick.Controls.Styles 1.1

import UM 1.0 as UM

import ".."

UM.Panel 
{
    id: settingsPanel
    color:"white"
    border.width:1
    signal settingConfigurationRequested;

    contents: ColumnLayout
    {
        Layout.preferredWidth: 250
        Layout.preferredHeight: 500
        UM.SettingsView 
        {
            anchors.fill:parent
        }
    }
}
