#ifndef CONTROL_H
#define CONTROL_H
#include "mainwindow.h"
#include "widget11.h"
#include "widget21.h"
#include "widget31.h"
#include "widget41.h"
#include "widget51.h"
#include "dialog1.h"
#include "dialog1_1.h"
#include  "dialog4_1.h"
#include "dialog4_2.h"
#include "dialog4_3.h"
#include "dialog4_4.h"
#include "wideget61.h"
#include "widget71.h"

class Control
{

private:
    Control();
    static Control* control;

public:
    static Control* get();
    MainWindow* w;
    widget11* w1;
    Dialog1* w1_1;
    dialog1_1* w1_2;

    widget21* w2;

    widget31* w3;

    widget41* w4;
    dialog4_1* w4_1;
    dialog4_2* w4_2;
    dialog4_3* w4_3;
    dialog4_4* w4_4;

    widget51* w5;

    wideget61* w6;

    widget71* w7;
};

#endif // CONTROL_H
