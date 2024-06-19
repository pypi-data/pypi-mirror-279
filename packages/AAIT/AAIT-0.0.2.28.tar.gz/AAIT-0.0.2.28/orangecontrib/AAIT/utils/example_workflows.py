import gc
import Orange

from orangecanvas import config
from orangecanvas.application import examples
from orangecanvas.preview import previewmodel, previewdialog
from AnyQt.QtWidgets import QDialog
import os
import ctypes

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\", "/"):
    from Orange.widgets.orangecontrib.AAIT.utils import shared_variables,MetManagement
else:
    from orangecontrib.AAIT.utils import shared_variables,MetManagement

def show_example_worklow(argself,windows_title="The Title"):
    """
    code extracted from orangecans.py of Orange data mining software
    """

    ows_files = []
    for dirpath, dirnames, filenames in os.walk(MetManagement.get_local_store_path()):
        for filename in filenames:
            if filename.endswith('.ows'):
                ows_files.append(os.path.join(dirpath, filename))
    print(ows_files)
    items = [previewmodel.PreviewItem(path=t) for t in ows_files]
    dialog = previewdialog.PreviewDialog(argself)
    model = previewmodel.PreviewModel(dialog, items=items)
    title = argself.tr(windows_title)
    dialog.setWindowTitle(title)
    template = ('<h3 style="font-size: 26px">\n'
                '{0}\n'
                '</h3>')

    dialog.setHeading(template.format(title))
    dialog.setModel(model)

    model.delayedScanUpdate()
    status = dialog.exec()
    index = dialog.currentIndex()

    dialog.deleteLater()

    if status == QDialog.Accepted:
        selected = model.item(index)

        # open_example_schem
    obj_id=-666
    for obj in gc.get_objects():
        # Stop whenever a MainWindow is found (OWS)
        # it can be another main windows but the example scheme will still open
        if isinstance(obj, Orange.canvas.mainwindow.MainWindow):
            obj_id=id(obj)
            break

    if obj_id!=-666:
        #open_scheme_file #open_example_scheme
        ctypes.cast(obj_id, ctypes.py_object).value.open_scheme_file(selected.path())

    return status