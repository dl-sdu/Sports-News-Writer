#ifndef WIDGET3_H
#define WIDGET3_H

#include <QWidget>

namespace Ui {
class widget3;
}

class widget3 : public QWidget
{
    Q_OBJECT

public:
    explicit widget3(QWidget *parent = 0);
    ~widget3();

private slots:
    void on_pushButton_2_clicked();

    void on_pushButton_clicked();

private:
    Ui::widget3 *ui;
    QString str;
};

#endif // WIDGET3_H
