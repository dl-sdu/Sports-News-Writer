#include "control.h"
#include "mainwindow.h"
#include "widget11.h"
#include "widget21.h"
#include "widget31.h"
#include "widget41.h"
#include "widget51.h"
#include "dialog4_1.h"
#include "dialog4_2.h"
#include "dialog4_3.h"
#include "dialog4_4.h"
#include "widget71.h"
#include "Python.h"

Control* Control::control=NULL;

Control::Control()
{
    w = new MainWindow();
    w1 = new widget11();
    w1_1 = new Dialog1();
    w1_2 = new dialog1_1;
    w2 = new widget21();
    w3 = new widget31();
    w4 = new widget41();
    w5 = new widget51();
    w6 = new wideget61();
    w4_1 =new dialog4_1();
    w4_2 =new dialog4_2();
    w4_3 =new dialog4_3();
    w4_4 =new dialog4_4();
    w7 = new widget71();

    w->show();
}
Control* Control::get()
{
        if(control == NULL)
                    control = new Control();
                return control;
}

