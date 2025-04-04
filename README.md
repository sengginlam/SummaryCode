# SummaryCode

README.md almost generated by AI.

SummaryCode is a Python-based tool designed to summarize code snippets using a LLM.

## Dependencies

1. [textual](https://textual.textualize.io/getting_started/)
2. [langchain](https://python.langchain.com/docs/how_to/installation/)
3. [pydantic](https://docs.pydantic.dev/latest/install/)

## Usage

1. set environment variable (optional)
   - `SUMMARYCODE_API_KEY`=your_api_key
   - `SUMMARYCODE_API_ADDRESS`=your_api_address

2. run UI
   - Windows:

        double click summaryCode.exe

    &emsp;&emsp;&emsp;or

   ```shell
   python -m summaryCode [display-font-size]
   ```

    &emsp;&emsp;&emsp;or

   ```shell
   summaryCode.exe [display-font-size]
   ```

   - Others (override `terminalFontSizeManager.TerminalFontSizeManager._setTerminalFontSize` and `terminalFontSizeManager.TerminalFontSizeManager._resetTerminalFontSize` for your platform to support display-font-size):

   ```shell
   python -m summaryCode
   ```

## Project Structure

### `_summaryCode.py`

This script contains the core logic for summarizing code using an LLM. It likely interacts with the LLM API to process and generate summaries for the provided code snippets.

### `summaryCode.py`

This is the main entry point for the SummaryCode tool. It orchestrates the summarization process and integrates various components of the tool.

### `terminalFontSizeManager.py`

This script manages display font sizes, providing a better user interface for viewing summarized code or other outputs.
Only support Windows, override `.TerminalFontSizeManager._setTerminalFontSize` and `.TerminalFontSizeManager._resetTerminalFontSize` for your platform to support display-font-size
