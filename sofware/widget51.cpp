#include "widget51.h"
#include "ui_widget51.h"
#include "control.h"
#include "Python.h"

widget51::widget51(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::widget51)
{
    ui->setupUi(this);
}

widget51::~widget51()
{
    delete ui;
}

void widget51::on_pushButton_clicked()
{
    this->hide();
    Control::get()->w->show();
}
