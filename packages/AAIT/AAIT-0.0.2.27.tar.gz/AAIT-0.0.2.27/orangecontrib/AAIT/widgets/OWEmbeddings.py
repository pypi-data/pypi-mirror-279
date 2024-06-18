import os
import sys

import Orange.data
from Orange.widgets import widget
from Orange.widgets.utils.signals import Input, Output

from PyQt5 import uic
from AnyQt.QtWidgets import QApplication, QLabel

if "site-packages/Orange/widgets" in os.path.dirname(os.path.abspath(__file__)).replace("\\","/"):
    from Orange.widgets.orangecontrib.AAIT.utils import shared_functions
    from Orange.widgets.orangecontrib.AAIT.llm import embeddings
    from Orange.widgets.orangecontrib.AAIT.utils.MetManagement import get_local_store_path
else:
    from orangecontrib.AAIT.utils import shared_functions
    from orangecontrib.AAIT.llm import embeddings
    from orangecontrib.AAIT.utils.MetManagement import get_local_store_path


class OWCreateEmbeddings(widget.OWWidget):
    name = "Create Embeddings"
    description = "Create embeddings on the column 'content' of a Table"
    icon = "icons/owembeddings.svg"
    gui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "designer/owembeddings.ui")
    want_control_area = False

    class Inputs:
        data = Input("Data", Orange.data.Table)

    class Outputs:
        data = Output("Data", Orange.data.Table)

    @Inputs.data
    def set_data(self, in_data):
        self.data = in_data
        self.run()

    def __init__(self):
        super().__init__()
        # Path management
        self.current_ows = ""
        local_store_path = get_local_store_path()
        model_name = "all-mpnet-base-v2"
        self.model_path = os.path.join(local_store_path, "Models", "NLP", model_name)

        # Qt Management
        self.setFixedWidth(470)
        self.setFixedHeight(300)
        uic.loadUi(self.gui, self)
        self.label_description = self.findChild(QLabel, 'Description')
        self.label_description.setText("This widget generates an answer on the column 'prompt' of your input data.")

        # Data Management
        self.data = None

    def run(self):
        try:
            table = embeddings.create_embeddings(self.data, self.model_path)
            self.Outputs.data.send(table)
        except Exception as e:
            print("An error occurred when generating embeddings:", e)
            self.Outputs.data.send(None)
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = OWCreateEmbeddings()
    my_widget.show()
    app.exec_()
