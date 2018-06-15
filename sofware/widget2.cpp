#include "widget2.h"
#include "ui_widget2.h"
#include "control.h"
#include "control.h"
#include "QFileDialog"
#include "QDebug"
#include "qmessagebox.h"

widget2::widget2(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::widget2)
{
    ui->setupUi(this);
}

widget2::~widget2()
{
    delete ui;
}

void widget2::on_pushButton_3_clicked()
{
    this->hide();
    Control::get()->w->show();
}

void widget2::on_pushButton_clicked()
{
    this->ui->textEdit->clear();
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

                           ui->textEdit->insertPlainText(read.readLine());
                           ui->textEdit->insertPlainText(QString("\n"));

                        }
                    }

}


void widget2::on_pushButton_2_clicked()
{
    QString fileName = QFileDialog::getSaveFileName(this, tr("保存文件") , tr("*.txt"));

    QFile file(fileName);//文件命名
        if (!file.open(QFile::WriteOnly | QFile::Text))     //检测文件是否打开
        {
            QMessageBox::information(this, "Error Message", "Please Select a Text File!");
            return;
        }
        QTextStream out(&file);                 //分行写入文件
        out << ui->textEdit->toPlainText();
        QMessageBox::information(this,"消息"," 保存成功 ");
        this->hide();
        Control::get()->w->show();
}
