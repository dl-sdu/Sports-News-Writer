#include "widget41.h"
#include "ui_widget41.h"
#include "control.h"
#include "dialog4_1.h"
#include "qfile.h"
#include "qfiledialog.h"
#include "qdebug.h"
#include "QMessageBox"
#include "Python.h"

widget41::widget41(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::widget41)
{
    ui->setupUi(this);
}

widget41::~widget41()
{
    delete ui;
}

void widget41::on_pushButton_2_clicked()
{
    this->hide();
    Control::get()->w->show();
    this->ui->textEdit->clear();
}

void widget41::on_pushButton_3_clicked()
{

    QString fileName = QString("D:/tuijian/tuijian.txt");

    QFile file(fileName);//文件命名
        if (!file.open(QFile::WriteOnly | QFile::Text))     //检测文件是否打开
        {
            QMessageBox::information(this, "Error Message", "Please Select a Text File!");
            return;
        }
        QTextStream out(&file);                 //分行写入文件
        out << ui->textEdit->toPlainText();
        QMessageBox::information(this,"消息"," 操作成功 ");


        //启动W4
        Control::get()->w4_1->doit();
        Control::get()->w4_1->show();


}

void widget41::on_pushButton_clicked()
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
