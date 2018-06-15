#ifndef DIALOG1_1_H
#define DIALOG1_1_H

#include <QDialog>

namespace Ui {
class dialog1_1;
}

class dialog1_1 : public QDialog
{
    Q_OBJECT

public:
    explicit dialog1_1(QWidget *parent = 0);
    ~dialog1_1();

private slots:
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

    void on_pushButton_3_clicked();

    void on_pushButton_4_clicked();

    void on_pushButton_7_clicked();

    void on_pushButton_5_clicked();

private:
    Ui::dialog1_1 *ui;
};

#endif // DIALOG1_1_H
