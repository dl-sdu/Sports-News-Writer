#ifndef WIDGET31_H
#define WIDGET31_H

#include <QMainWindow>

namespace Ui {
class widget31;
}

class widget31 : public QMainWindow
{
    Q_OBJECT

public:
    explicit widget31(QWidget *parent = 0);
    ~widget31();

private slots:
    void on_pushButton_2_clicked();

    void on_pushButton_clicked();

private:
    Ui::widget31 *ui;
    QString str;
};

#endif // WIDGET31_H
