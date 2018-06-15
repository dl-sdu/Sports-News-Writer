#include "dialog1.h"
#include "ui_dialog1.h"
#include "qdebug.h"
#include "QTextStream"
#include "qfile.h"
#include "QMessageBox"
#include "control.h"
#include "QFileDialog"
#include "qdebug.h"
#include "Python.h"

Dialog1::Dialog1(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Dialog1)
{
    ui->setupUi(this);
}

Dialog1::~Dialog1()
{
    delete ui;
}

void Dialog1::doit(){

      this->ui->textEdit->clear();
    //qDebug()<<str<<"   is str now";
    QFile file(str);
    // qDebug()<<str<<"      kkkkkkkkkkk";
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

void Dialog1::on_pushButton_clicked()
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
