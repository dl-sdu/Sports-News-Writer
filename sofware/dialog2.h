#ifndef DIALOG2_H
#define DIALOG2_H

#include <QDialog>

namespace Ui {
class dialog2;
}

class dialog2 : public QDialog
{
    Q_OBJECT

public:
    explicit dialog2(QWidget *parent = 0);
    ~dialog2();

private:
    Ui::dialog2 *ui;
};

#endif // DIALOG2_H
