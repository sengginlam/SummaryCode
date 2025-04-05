from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Button, Header, RichLog, Input, TextArea, Label
from textual.worker import Worker, WorkerState
from rich.text import Text
from tkinter.filedialog import askopenfilename
from os import path, getenv
from platform import system as systemType
from sys import argv
from re import findall
from _summaryCode import _summaryCode
from terminalFontSizeManager import TerminalFontSizeManager


INIT_TEXT_0 = \
'''
The api used should compatible with OpenAI
**NEEDED: model. default: 'qwen-long'**
**NEEDED: api key. auto load from env var `SUMMARYCODE_API_KEY`**
**NEEDED: api address. auto load from env var `SUMMARYCODE_API_ADDRESS`**
**NEEDED: code type. default: 'python'**
**OPTIONAL: code description. Writing in Chinese and fllowing the best practice is recommended. \ndescription best practice:\n \tBegin with “这段代码描述了......”**
'''
INIT_TEXT_1 = \
'''
default model: {}
default api key: {}
default api address: {}
default code type: {}
'''

class Tui(App[int]):
    TITLE = "summary code"
    CSS_PATH = "summaryCode.tcss"

    _WORKER_STATE = (WorkerState.CANCELLED, WorkerState.ERROR, WorkerState.SUCCESS)

    def compose(self) -> ComposeResult:
        '''
            chooseFile->left-top    filePath->middle-top:path   summary->right-top:summary
                                                                apiKey->right-bottom:api-key
                        view->left-buttom:view                  baseUrl->right-bottom:base-url
                                                                description->right-bottom:description
                                                                
        '''
        yield Header(show_clock=True)
        with Container(id="app-grid"):
            yield Button("choose file", id="left-top")
            with Container(id="middle-top"):
                yield Input(id="path", placeholder="file abs path")
            with Container(id="right-top"):
                yield Button("summary", id="summary")
            with VerticalScroll(id="left-buttom"):
                yield RichLog(wrap=True, markup=True, auto_scroll=True, id="view")
            with Container(id="right-bottom"):
                yield Input(id="model", placeholder="model name")
                yield Input(id="api-key", placeholder="api key", password=True)
                yield Input(id="baseUrl", placeholder="api address")
                yield Input(id="type", placeholder="code type")
                yield Label("input code description below", id="label")
                yield TextArea(id="description")
                yield Button("submit description", id="descriptionSubmit")

    def on_ready(self) -> None:
        self._chooseFile = self.query_one("#left-top") 
        if systemType()!="Windows":
            self._chooseFile.visible = False
        self._path = self.query_one("#path")
        self._summary = self.query_one("#summary")
        self._view = self.query_one("#view")
        self._model = self.query_one("#model")
        self._apiKey = self.query_one("#api-key")
        self._baseUrl = self.query_one("#baseUrl")
        self._type = self.query_one("#type")
        self._description = self.query_one("#description")
        self._MODEL = "qwen-long"
        self._API_KEY = getenv("SUMMARYCODE_API_KEY")
        self._BASE_RUL = getenv("SUMMARYCODE_API_ADDRESS")
        self._TYPE = "python"
        self._DESCRIPTION = ""
        self._descriptionSubmit = self.query_one("#descriptionSubmit")
        self._echo(INIT_TEXT_0)
        self._echo(
                    INIT_TEXT_1.format(
                                        self._MODEL, 
                                        self._API_KEY, 
                                        self._BASE_RUL, 
                                        self._TYPE
                                    )
                )

    def _echo(self, text:str) -> None:
        text_ = Text(text)
        self._view.write(text_)

    def _turnON(self) -> None:
        self._chooseFile.disabled = False
        self._path.disabled = False
        self._summary.disabled = False
        self._model.disabled = False
        self._apiKey.disabled = False
        self._baseUrl.disabled = False
        self._type.disabled = False
        self._description.disabled = False
        self._descriptionSubmit.disabled = False

    def _turnOFF(self) -> None:
        self._chooseFile.disabled = True
        self._path.disabled = True
        self._summary.disabled = True
        self._model.disabled = True
        self._apiKey.disabled = True
        self._baseUrl.disabled = True
        self._type.disabled = True
        self._description.disabled = True
        self._descriptionSubmit.disabled = True

    @on(Button.Pressed, "#left-top")
    def setSourcePath(self) -> None:
        try:
            tmpPath = askopenfilename()
            if path.exists(tmpPath) and path.isfile(tmpPath):
                self._SOURCE = tmpPath
                self._path.value = self._SOURCE
                self._echo(f"set code file:\t{self._SOURCE}")
            else:
                self._echo("ERROE: no such file or it's not a file.")
        except:
            self._echo("ERROR: unknown")

    @on(Input.Submitted, "#path")
    def setSourcePath_2(self) -> None:
        try:
            if path.exists(self._path.value) and path.isfile(self._path.value):
                self._SOURCE = self._path.value
                self._path.value = ""
                self._echo(f"set code file:\t{self._SOURCE}")
            else:
                self._echo("ERROE: no such file or it's not a file.")
        except:
            self._echo("ERROR: unknown")

    def _checkBeforeRun(self) -> bool:
        EMPTY = ("", None)
        if self._MODEL in EMPTY or\
            self._API_KEY in EMPTY or\
            self._BASE_RUL in EMPTY or\
            self._TYPE in EMPTY:
                self._echo("ERROR: empty parameter.")
                return False
        else:
            if path.exists(self._SOURCE) and path.isfile(self._SOURCE):
                return True
            else:
                self._echo("ERROR: no such file or it's not a file.")
                return False

    @on(Button.Pressed, "#summary")
    def summary(self) -> None:
        try:
            self._turnOFF()
            if self._checkBeforeRun:
                self._runSummary()
            else:
                self._echo("ERROR: parameter error, unable to run summary.")
        except Exception as e:
            self._echo(f"ERROR: {e}")

    @work(thread=True)
    def _runSummary(self) -> None:
        try:
            config = {
                        "apiKey":self._API_KEY, 
                        "baseUrl":self._BASE_RUL, 
                        "model":self._MODEL, 
                        "scriptPath":self._SOURCE, 
                        "scriptType":self._TYPE, 
                        "scriptDescription":self._DESCRIPTION,     
                    }
            for out in _summaryCode(**config):
                self.call_from_thread(self._echo, out)
            else:
                out = out[:-52]
                sourceName = path.basename(self._SOURCE)
                sN_re = findall(r"(.+)\..+$", sourceName)
                if len(sN_re):
                    outPath = path.join(path.dirname(__file__), f"#SUMMARY#{sN_re[0]}.md")
                    with open(outPath, mode="wt", encoding="utf-8") as o:
                        o.write(out)
                    self.call_from_thread(self._echo, f"summary save as {outPath}")
        except Exception as e:
            self.call_from_thread(self._echo, f"ERROR: quit summary\n{e}")

    @on(Worker.StateChanged)
    def workerSpy(self) -> None:
        for worker in self.workers:
            if worker.state in self._WORKER_STATE:
                self._turnON()

    @on(Input.Submitted, "#model")
    def setModel(self) -> None:
        try:
            self._MODEL = self._model.value
            self._model.clear()
            self._echo(f"set model: {self._MODEL}")
        except Exception as e:
            self._echo(f"ERROR: {e}")

    @on(Input.Submitted, "#api-key")
    def setApiKey(self) -> None:
        try:
            self._API_KEY = self._apiKey.value
            self._apiKey.clear()
            self._echo(f"set api key: {self._API_KEY}")
        except Exception as e:
            self._echo(f"ERROR: {e}")

    @on(Input.Submitted, "#baseUrl")
    def setBaseUrl(self) -> None:
        try:
            self._BASE_RUL = self._baseUrl.value
            self._baseUrl.clear()
            self._echo(f"set api address: {self._BASE_RUL}")
        except Exception as e:
            self._echo(f"ERROR: {e}")

    @on(Input.Submitted, "#type")
    def setType(self) -> None:
        try:
            self._TYPE = self._type.value
            self._type.clear()
            self._echo(f"set code type: {self._TYPE}")
        except Exception as e:
            self._echo(f"ERROR: {e}")

    @on(Button.Pressed, "#descriptionSubmit")
    def setDescription(self) -> None:
        try:
            if self._description.text!="":
                self._DESCRIPTION = self._description.text
                self._description.clear()
                self._echo(f"set description: \n\t{self._DESCRIPTION}")
            else:
                self._echo("set description: None")
        except Exception as e:
            self._echo(f"ERROR: {e}")

def main():
    app = Tui()
    app.run()

if __name__=="__main__":
    try:
        tfsm = TerminalFontSizeManager()
    except Exception as e:
        print(e)
        tfsm = None
    try:
        if tfsm:
            try:
                fontSize = int(argv[1])
            except:
                fontSize = None
            tfsm(fontSize)
        main()
    finally:
        tfsm and tfsm()