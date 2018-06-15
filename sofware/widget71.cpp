#include "widget71.h"
#include "ui_widget71.h"
#include "Python.h"

widget71::widget71(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::widget71)
{
    ui->setupUi(this);
}

widget71::~widget71()
{
    delete ui;
}
