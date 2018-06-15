#ifndef WIDGET11_H
#define WIDGET11_H

#include <QMainWindow>

namespace Ui {
class widget11;
}

class widget11 : public QMainWindow
{
    Q_OBJECT

public:
    explicit widget11(QWidget *parent = 0);
    void doit();
    ~widget11();
    QString xlsFile;

private slots:
    void on_pushButton_3_clicked();

    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

private:
    Ui::widget11 *ui;

};

#endif // WIDGET11_H
