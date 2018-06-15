#ifndef WIDGET71_H
#define WIDGET71_H

#include <QMainWindow>

namespace Ui {
class widget71;
}

class widget71 : public QMainWindow
{
    Q_OBJECT

public:
    explicit widget71(QWidget *parent = 0);
    ~widget71();

private:
    Ui::widget71 *ui;
};

#endif // WIDGET71_H
