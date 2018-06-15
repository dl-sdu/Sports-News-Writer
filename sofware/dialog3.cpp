#include "dialog3.h"
#include "ui_dialog3.h"

dialog3::dialog3(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::dialog3)
{
    ui->setupUi(this);
}

dialog3::~dialog3()
{
    delete ui;
}
