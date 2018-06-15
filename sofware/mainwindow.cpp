#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "qstylefactory.h"
#include "QDebug"
#include "control.h"
#include "Python.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked()
{
    this->hide();
    Control::get()->w1->show();
}

void MainWindow::on_pushButton_2_clicked()
{
    this->hide();
    Control::get()->w2->show();
}

void MainWindow::on_pushButton_3_clicked()
{
    this->hide();
    Control::get()->w3->show();
}

void MainWindow::on_pushButton_4_clicked()
{
    this->hide();
    Control::get()->w4->show();
}

void MainWindow::on_pushButton_5_clicked()
{
    //this->hide();
    Control::get()->w5->show();
}

void MainWindow::on_pushButton_6_clicked()
{

}

void MainWindow::on_pushButton_9_clicked()
{
    this->hide();
    Control::get()->w6->show();
}

void MainWindow::on_pushButton_10_clicked()
{
    Control::get()->w7->show();
}
