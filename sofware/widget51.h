#ifndef WIDGET51_H
#define WIDGET51_H

#include <QMainWindow>

namespace Ui {
class widget51;
}

class widget51 : public QMainWindow
{
    Q_OBJECT

public:
    explicit widget51(QWidget *parent = 0);
    ~widget51();

private slots:
    void on_pushButton_clicked();

private:
    Ui::widget51 *ui;
};

#endif // WIDGET51_H
