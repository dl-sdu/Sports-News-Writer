#include "wideget61.h"
#include "ui_wideget61.h"
#include "control.h"
#include "qfile.h"
#include "qfiledialog.h"
#include "qmessagebox.h"
#include "qdebug.h"
#include "Python.h"

wideget61::wideget61(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::wideget61)
{
    ui->setupUi(this);
}

wideget61::~wideget61()
{
    delete ui;
}

void wideget61::on_pushButton_2_clicked()
{
    this->hide();
    Control::get()->w->show();
}

void wideget61::on_pushButton_3_clicked()
{
    this->ui->textEdit_3->clear();
    //this->ui->textEdit->setText(QString("ASADSDS"));
    str = QFileDialog::getOpenFileName(this, tr("打开文件"), tr("*.txt") );
    QFile file(str);
    if(file.isOpen())
        qDebug()<<"open";

                    if(file.open(QIODevice::ReadOnly))

                    {

                        QTextStream read(&file);

                        while(!read.atEnd() )

                        {

                           ui->textEdit_3->insertPlainText(read.readLine());
                           ui->textEdit_3->insertPlainText(QString("\n"));

                        }
                    }

}

void wideget61::on_pushButton_clicked()
{
    //this->ui->textEdit_2->setText(QString("体育"));
    this->ui->textEdit->clear();
    this->ui->textEdit_3->clear();
    QString x=QString("D:/fenlei/fenlei.txt");
    QFile file(x);
    if(file.isOpen())
        qDebug()<<"open";

                    if(file.open(QIODevice::ReadOnly))

                    {

                        QTextStream read(&file);

                        while(!read.atEnd() )

                        {

                           ui->textEdit->insertPlainText(read.readLine());
                           ui->textEdit->insertPlainText(QString("    "));
                           ui->textEdit->insertPlainText(read.readLine());
                           ui->textEdit->insertPlainText(QString("\n"));
                        }
                    }

}


