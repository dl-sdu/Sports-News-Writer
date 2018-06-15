#ifndef DIALOG4_4_H
#define DIALOG4_4_H

#include <QDialog>

namespace Ui {
class dialog4_4;
}

class dialog4_4 : public QDialog
{
    Q_OBJECT

public:
    explicit dialog4_4(QWidget *parent = 0);
    void doit();
    ~dialog4_4();

private slots:
    void on_pushButton_clicked();

private:
    Ui::dialog4_4 *ui;
};

#endif // DIALOG4_4_H
