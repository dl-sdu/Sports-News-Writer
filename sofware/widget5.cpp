#include "widget5.h"
#include "ui_widget5.h"
#include "control.h"

widget5::widget5(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::widget5)
{
    ui->setupUi(this);
}

widget5::~widget5()
{
    delete ui;
}

void widget5::on_pushButton_clicked()
{
    this->hide();
    Control::get()->w->show();
}
