#include "dialog4_1.h"
#include "ui_dialog4_1.h"
#include "control.h"
#include "dialog4_2.h"
#include "qfile.h"
#include "qdebug.h"
#include "Python.h"

dialog4_1::dialog4_1(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::dialog4_1)
{
    ui->setupUi(this);
}

dialog4_1::~dialog4_1()
{
    delete ui;
}

void dialog4_1::on_pushButton_clicked()
{
    this->ui->textEdit->clear();
    this->hide();
    Control::get()->w4_2->doit();
    Control::get()->w4_2->show();
}

void dialog4_1::doit(){
    this->ui->textEdit->clear();
    //this->ui->textEdit->setText(QString("ASADSDS"));
    QString str = QString("D:/tuijian/tuijian1.txt");

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






