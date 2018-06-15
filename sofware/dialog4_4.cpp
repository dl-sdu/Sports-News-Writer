#include "dialog4_4.h"
#include "ui_dialog4_4.h"
#include "qfile.h"
#include "qdebug.h"
#include "control.h"
#include "Python.h"

dialog4_4::dialog4_4(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::dialog4_4)
{
    ui->setupUi(this);
}

dialog4_4::~dialog4_4()
{
    delete ui;
}

void dialog4_4::on_pushButton_clicked()
{
    this->ui->textEdit->clear();
    this->hide();
}

void dialog4_4::doit(){
    this->ui->textEdit->clear();
    //this->ui->textEdit->setText(QString("ASADSDS"));
    QString str = QString("D:/tuijian/tuijian4.txt");

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
