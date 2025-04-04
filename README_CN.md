# SummaryCode

README_CN.md 几乎由 AI 生成。

SummaryCode 是一个基于 Python 的工具，用于使用 LLM 总结代码片段。

## 依赖项

1. [textual](https://textual.textualize.io/getting_started/)
2. [langchain](https://python.langchain.com/docs/how_to/installation/)
3. [pydantic](https://docs.pydantic.dev/latest/install/)

## 使用方法

1. 设置环境变量（可选）
   - `SUMMARYCODE_API_KEY`=your_api_key
   - `SUMMARYCODE_API_ADDRESS`=your_api_address

2. 运行
   - Windows:

        双击summaryCode.exe

    &emsp;&emsp;&emsp;或者

   ```shell
   python -m summaryCode [display-font-size]
   ```

    &emsp;&emsp;&emsp;或者

   ```shell
   summaryCode.exe [display-font-size]
   ```

   - 其他平台（需要覆盖 `terminalFontSizeManager.TerminalFontSizeManager._setTerminalFontSize` 和 `terminalFontSizeManager.TerminalFontSizeManager._resetTerminalFontSize` 以支持display-font-size）：

   ```shell
   python -m summaryCode
   ```

## 项目结构

### `_summaryCode.py`

此脚本包含使用 LLM 总结代码的核心逻辑。它可能与 LLM API 交互以处理并生成提供的代码片段的摘要。

### `summaryCode.py`

这是 SummaryCode 工具的主要入口点。它负责协调摘要过程并集成工具的各个组件。

### `terminalFontSizeManager.py`

此脚本管理显示字体大小，为查看摘要代码或其他输出提供更好的用户界面。
仅支持 Windows，其他平台需要覆盖 `.TerminalFontSizeManager._setTerminalFontSize` 和 `.TerminalFontSizeManager._resetTerminalFontSize` 以支持display-font-size。
