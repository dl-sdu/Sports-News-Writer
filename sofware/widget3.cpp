#include "widget3.h"
#include "ui_widget3.h"
#include "control.h"
#include "qdebug.h"
#include "QFileDialog"
#include "qfile.h"

widget3::widget3(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::widget3)
{
    ui->setupUi(this);
}

widget3::~widget3()
{
    delete ui;
}

void widget3::on_pushButton_2_clicked()
{
    this->hide();
    Control::get()->w->show();
}

void widget3::on_pushButton_clicked()
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
