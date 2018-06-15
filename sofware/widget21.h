#ifndef WIDGET21_H
#define WIDGET21_H

#include <QMainWindow>

namespace Ui {
class widget21;
}

class widget21 : public QMainWindow
{
    Q_OBJECT

public:
    explicit widget21(QWidget *parent = 0);
    ~widget21();

private slots:
    void on_pushButton_3_clicked();

    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

private:
    Ui::widget21 *ui;
    QString str;
};

#endif // WIDGET21_H
