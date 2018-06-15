#-------------------------------------------------
#
# Project created by QtCreator 2018-05-30T16:21:08
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = Pro
TEMPLATE = app

# The following define makes your compiler emit warnings if you use
# any feature of Qt which has been marked as deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

# You can also make your code fail to compile if you use deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0


SOURCES += \
        main.cpp \
        mainwindow.cpp \
    control.cpp \
    widget1.cpp \
    dialog1.cpp \
    dialog1_1.cpp \
    dialog4_1.cpp \
    dialog4_2.cpp \
    dialog4_3.cpp \
    dialog4_4.cpp \
    widget11.cpp \
    widget21.cpp \
    widget31.cpp \
    widget41.cpp \
    widget51.cpp \
    wideget61.cpp \
    widget71.cpp

HEADERS += \
        mainwindow.h \
    control.h \
    widget1.h \
    dialog1.h \
    dialog1_1.h \
    dialog4_1.h \
    dialog4_2.h \
    dialog4_3.h \
    dialog4_4.h \
    widget11.h \
    widget21.h \
    widget31.h \
    widget41.h \
    widget51.h \
    wideget61.h \
    widget71.h

FORMS += \
        mainwindow.ui \
    widget1.ui \
    dialog1.ui \
    dialog1_1.ui \
    dialog4_1.ui \
    dialog4_2.ui \
    dialog4_3.ui \
    dialog4_4.ui \
    widget11.ui \
    widget21.ui \
    widget31.ui \
    widget41.ui \
    widget51.ui \
    wideget61.ui \
    widget71.ui

QT       += axcontainer

QT       += core gui axcontainer

RESOURCES += \
    zxc.qrc \
    asdf.qrc

DISTFILES +=

win32: LIBS += -LC:/Python3/libs/ -lpython36

INCLUDEPATH += C:/Python3/include
DEPENDPATH += C:/Python3/include

win32:!win32-g++: PRE_TARGETDEPS += C:/Python3/libs/python36.lib
else:win32-g++: PRE_TARGETDEPS += C:/Python3/libs/libpython36.a
