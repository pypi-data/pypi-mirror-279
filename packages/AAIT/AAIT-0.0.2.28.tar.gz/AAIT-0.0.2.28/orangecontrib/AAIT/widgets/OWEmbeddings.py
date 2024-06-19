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
    from Orange.widgets.orangecontrib.AAIT.utils import threading
    from Orange.widgets.orangecontrib.AAIT.utils.MetManagement import get_local_store_path
else:
    from orangecontrib.AAIT.utils import shared_functions
    from orangecontrib.AAIT.llm import embeddings
    from orangecontrib.AAIT.utils import threading
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

        # Data Management
        self.data = None
        self.thread = None

    def run(self):
        # Start progress bar
        self.progressBarInit()

        # Connect and start thread : main function, progress, result and finish
        # --> progress is used in the main function to track progress (with a callback)
        # --> result is used to collect the result from main function
        # --> finish is just an empty signal to indicate that the thread is finished
        self.thread = threading.Thread(embeddings.create_embeddings, self.data, self.model_path)
        self.thread.progress.connect(self.handle_progress)
        self.thread.result.connect(self.handle_result)
        self.thread.finish.connect(self.handle_finish)
        self.thread.start()

    def handle_progress(self, value):
        self.progressBarSet(value)

    def handle_result(self, result):
        try:
            self.Outputs.data.send(result)
        except Exception as e:
            print("An error occurred when sending out_data:", e)
            self.Outputs.data.send(None)
            return

    def handle_finish(self):
        print("Embeddings finished")
        self.progressBarFinished()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_widget = OWCreateEmbeddings()
    my_widget.show()
    app.exec_()
