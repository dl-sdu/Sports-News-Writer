#ifndef WIDGET5_H
#define WIDGET5_H

#include <QWidget>

namespace Ui {
class widget5;
}

class widget5 : public QWidget
{
    Q_OBJECT

public:
    explicit widget5(QWidget *parent = 0);
    ~widget5();

private slots:
    void on_pushButton_clicked();

private:
    Ui::widget5 *ui;
};

#endif // WIDGET5_H
