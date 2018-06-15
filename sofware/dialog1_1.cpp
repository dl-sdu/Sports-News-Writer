#include "dialog1_1.h"
#include "ui_dialog1_1.h"
#include "control.h"
//#include <Python.h>
#include "qdebug.h"
#include "Python.h"
//#include "dialog1_1.ui"

dialog1_1::dialog1_1(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::dialog1_1)
{
    ui->setupUi(this);
}

dialog1_1::~dialog1_1()
{
    delete ui;
}

void dialog1_1::on_pushButton_clicked()
{
     //Control::get()->w1_1->ui->
     Control::get()->w1_1->str=QString("D:/s/1.txt");
     Control::get()->w1->doit();

     this->hide();
}

void dialog1_1::on_pushButton_2_clicked()
{
    Control::get()->w1_1->str=QString("D:/s/2.txt");
     Control::get()->w1->doit();

     this->hide();

}

void dialog1_1::on_pushButton_3_clicked()
{
     Control::get()->w1_1->str=QString("D:/s/3.txt");
     Control::get()->w1->doit();

     this->hide();
}

void dialog1_1::on_pushButton_4_clicked()
{
    Control::get()->w1_1->str=QString("D:/s/4.txt");
    Control::get()->w1->doit();

    this->hide();
}

void dialog1_1::on_pushButton_7_clicked()
{

    Control::get()->w1_1->str=QString("D:/s/5.txt");
    Control::get()->w1->doit();

    this->hide();
}

void dialog1_1::on_pushButton_5_clicked()
{
    Control::get()->w1_1->str=QString("D:/s/6.txt");
    Control::get()->w1->doit();

    this->hide();
}
