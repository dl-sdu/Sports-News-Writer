#ifndef WIDGET41_H
#define WIDGET41_H

#include <QMainWindow>

namespace Ui {
class widget41;
}

class widget41 : public QMainWindow
{
    Q_OBJECT

public:
    explicit widget41(QWidget *parent = 0);
    ~widget41();

private slots:
    void on_pushButton_2_clicked();

    void on_pushButton_3_clicked();

    void on_pushButton_clicked();

private:
    Ui::widget41 *ui;
    QString str;
};

#endif // WIDGET41_H
