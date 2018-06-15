#ifndef WIDEGET61_H
#define WIDEGET61_H

#include <QMainWindow>

namespace Ui {
class wideget61;
}

class wideget61 : public QMainWindow
{
    Q_OBJECT

public:
    explicit wideget61(QWidget *parent = 0);
    ~wideget61();

private slots:
    void on_pushButton_2_clicked();

    void on_pushButton_3_clicked();

    void on_pushButton_clicked();

private:
    Ui::wideget61 *ui;
    QString str="";
};

#endif // WIDEGET61_H
