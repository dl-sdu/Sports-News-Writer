#ifndef WIDGET1_H
#define WIDGET1_H

#include <QWidget>

namespace Ui {
class widget1;
}

class widget1 : public QWidget
{
    Q_OBJECT

public:
    explicit widget1(QWidget *parent = 0);
    void doit();
    ~widget1();

private slots:
    void on_pushButton_3_clicked();

    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

private:
    Ui::widget1 *ui;
    QString xlsFile;
};

#endif // WIDGET1_H
