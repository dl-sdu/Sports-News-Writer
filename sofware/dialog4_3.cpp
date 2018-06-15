#include "dialog4_3.h"
#include "ui_dialog4_3.h"
#include "control.h"
#include "dialog4_4.h"
#include "qfile.h"
#include "qdebug.h"
#include "Python.h"

dialog4_3::dialog4_3(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::dialog4_3)
{
    ui->setupUi(this);
}

dialog4_3::~dialog4_3()
{
    delete ui;
}

void dialog4_3::on_pushButton_clicked()
{
    this->ui->textEdit->clear();
    this->hide();
    Control::get()->w4_4->doit();
    Control::get()->w4_4->show();
}

void dialog4_3::doit(){
    this->ui->textEdit->clear();
    //this->ui->textEdit->setText(QString("ASADSDS"));
    QString str = QString("D:/tuijian/tuijian3.txt");

    QFile file(str);
    if(file.isOpen())
        qDebug()<<"open";

                    if(file.open(QIODevice::ReadOnly))

                    {

                        QTextStream read(&file);

                        while(!read.atEnd() )

                        {

                           ui->textEdit->insertPlainText(read.readLine());
                           ui->textEdit->insertPlainText(QString("\n"));

                        }
                    }

}
