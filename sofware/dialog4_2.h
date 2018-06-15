#ifndef DIALOG4_2_H
#define DIALOG4_2_H

#include <QDialog>

namespace Ui {
class dialog4_2;
}

class dialog4_2 : public QDialog
{
    Q_OBJECT

public:
    explicit dialog4_2(QWidget *parent = 0);
    void doit();
    ~dialog4_2();

private slots:
    void on_pushButton_clicked();

private:
    Ui::dialog4_2 *ui;
};

#endif // DIALOG4_2_H
