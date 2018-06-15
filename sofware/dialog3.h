#ifndef DIALOG3_H
#define DIALOG3_H

#include <QDialog>

namespace Ui {
class dialog3;
}

class dialog3 : public QDialog
{
    Q_OBJECT

public:
    explicit dialog3(QWidget *parent = 0);
    ~dialog3();

private:
    Ui::dialog3 *ui;
};

#endif // DIALOG3_H
