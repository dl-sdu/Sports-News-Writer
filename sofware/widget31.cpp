#include "widget31.h"
#include "ui_widget31.h"
#include "control.h"
#include "qdebug.h"
#include "QFileDialog"
#include "qfile.h"
#include "Python.h"

widget31::widget31(QWidget *parent) :
   QMainWindow(parent),
    ui(new Ui::widget31)
{
    ui->setupUi(this);
}

widget31::~widget31()
{
    delete ui;
}

void widget31::on_pushButton_2_clicked()
{
    this->hide();
    Control::get()->w->show();
}

void widget31::on_pushButton_clicked()
{
    //this->ui->textEdit->clear();
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

                           ui->lineEdit_2->insert(read.readLine());

                        }
                    }
}
