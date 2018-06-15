#include "widget1.h"
#include "ui_widget1.h"
#include "control.h"
#include "QFileDialog"
#include "qmessagebox.h"
#include "qaxobject.h"
#include "qlabel.h"
#include "qdebug.h"
#include "Python.h"

widget1::widget1(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::widget1)
{
    ui->setupUi(this);
}

widget1::~widget1()
{
    delete ui;
}

void widget1::on_pushButton_3_clicked()
{
    this->hide();
    Control::get()->w->show();
}

void widget1::on_pushButton_clicked()
{

    this->ui->textEdit->clear();
    xlsFile = QFileDialog::getOpenFileName(this,QString(),QString(),"excel(*.xls *.xlsx)");

    qDebug()<<"xlsFile is       "<<xlsFile;
    // step1 链接控件
    QAxObject* excel = new QAxObject(this);
    excel->setControl("Excel.Application");  // 连接Excel控件
    excel->dynamicCall("SetVisible (bool Visible)", "false"); // 不显示窗体
    excel->setProperty("DisplayAlerts", false);  // 不显示任何警告信息。如果为true, 那么关闭时会出现类似"文件已修改，是否保存"的提示

    // step2: 打开工作簿
    QAxObject* workbooks = excel->querySubObject("WorkBooks"); // 获取工作簿集合
    QAxObject* workbook = workbooks->querySubObject("Open(const QString&)", xlsFile);

    // step3: 打开sheet
    QAxObject* worksheet = workbook->querySubObject("WorkSheets(int)", 1); // 获取工作表集合的工作表1， 即sheet1

    // step4: 获取行数，列数
        QAxObject* usedrange = worksheet->querySubObject("UsedRange"); // sheet范围
        int intRowStart = usedrange->property("Row").toInt(); // 起始行数
        int intColStart = usedrange->property("Column").toInt();  // 起始列数

        QAxObject *rows, *columns;
        rows = usedrange->querySubObject("Rows");  // 行
        columns = usedrange->querySubObject("Columns");  // 列

        int intRow = rows->property("Count").toInt(); // 行数
        int intCol = columns->property("Count").toInt();  // 列数

     //读
        for(int i=1; i <= intRow; i++ ){
            for(int j=1; j<=3;j++){
                    QAxObject* cell = worksheet->querySubObject("Cells(int, int)", i, j);  //获单元格值
                  //  qDebug() <<1<<"   "<< 1<<"   "<< cell->dynamicCall("Value2()").toString();
                    QString str=cell->dynamicCall("Value2()").toString();
                    this->ui->textEdit->insertPlainText(str);
                    this->ui->textEdit->insertPlainText("   ");
            }
            this->ui->textEdit->insertPlainText("\n");
        }

}

void widget1::on_pushButton_2_clicked()
{

    Control::get()->w1_2->show();

}

void widget1::doit(){
    this->hide();
    Control::get()->w1_1->doit();
    Control::get()->w1_1->show();
}


