#include "dialog4_2.h"
#include "ui_dialog4_2.h"
#include "control.h"
#include "dialog4_3.h"
#include "qfile.h"
#include "qdebug.h"
#include "Python.h"

dialog4_2::dialog4_2(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::dialog4_2)
{
    ui->setupUi(this);
}

dialog4_2::~dialog4_2()
{
    delete ui;
}

void dialog4_2::on_pushButton_clicked()
{
    this->ui->textEdit->clear();
    this->hide();
    Control::get()->w4_3->doit();
    Control::get()->w4_3->show();
}

void dialog4_2::doit(){
    this->ui->textEdit->clear();
    //this->ui->textEdit->setText(QString("ASADSDS"));
    QString str = QString("D:/tuijian/tuijian2.txt");

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
