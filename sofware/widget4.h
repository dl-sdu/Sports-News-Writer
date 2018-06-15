#ifndef WIDGET4_H
#define WIDGET4_H

#include <QWidget>

namespace Ui {
class widget4;
}

class widget4 : public QWidget
{
    Q_OBJECT

public:
    explicit widget4(QWidget *parent = 0);
    ~widget4();

private slots:
    void on_pushButton_2_clicked();

    void on_pushButton_3_clicked();

    void on_pushButton_clicked();

private:
    Ui::widget4 *ui;
    QString str;
};

#endif // WIDGET4_H
