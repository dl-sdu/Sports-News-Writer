#ifndef DIALOG4_3_H
#define DIALOG4_3_H

#include <QDialog>

namespace Ui {
class dialog4_3;
}

class dialog4_3 : public QDialog
{
    Q_OBJECT

public:
    explicit dialog4_3(QWidget *parent = 0);
    void doit();
    ~dialog4_3();

private slots:
    void on_pushButton_clicked();

private:
    Ui::dialog4_3 *ui;
};

#endif // DIALOG4_3_H
