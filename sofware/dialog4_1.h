#ifndef DIALOG4_1_H
#define DIALOG4_1_H

#include <QDialog>

namespace Ui {
class dialog4_1;
}

class dialog4_1 : public QDialog
{
    Q_OBJECT

public:
    explicit dialog4_1(QWidget *parent = 0);
    void doit();
    ~dialog4_1();

private slots:
    void on_pushButton_clicked();

private:
    Ui::dialog4_1 *ui;
};

#endif // DIALOG4_1_H
