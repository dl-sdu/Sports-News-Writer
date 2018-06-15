#include "dialog2.h"
#include "ui_dialog2.h"

dialog2::dialog2(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::dialog2)
{
    ui->setupUi(this);
}

dialog2::~dialog2()
{
    delete ui;
}
