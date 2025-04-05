from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompt_values import PromptValue
from typing import Optional, Iterator


def readScript(scriptPath:str) -> Optional[str]:
    PREFIX = "```CODE BEGIN\n"
    SUFFIX = "```CODE END\n"
    try:
        with open(scriptPath, mode="rt", encoding="utf-8") as file:
            _ = PREFIX+file.read()+SUFFIX
        return _
    except:
        return None

def writePrompt(
        script:str, 
        scriptType:Optional[str]="python", 
        scriptDescription:Optional[str]="",
    ) -> PromptValue:
    promptTemplate = ChatPromptTemplate.from_messages(
        [
            ("system", f"你是{scriptType}代码专家，用户会向你传送代码。{scriptDescription}\n请你向用户总结这段代码的实现思路。"),  
            ("user", "{text}")]
        )
    return promptTemplate.invoke({"text":script})

def _summaryCode(
        apiKey:str, 
        baseUrl:str, 
        model:str, 
        scriptPath:str, 
        scriptType:Optional[str]="python", 
        scriptDescription:Optional[str]="",
    ) -> Iterator[str]:
    DELIMITER = "\n=======================TASK=======================\n"
    yield DELIMITER+"summaryCode is working.\nloading LLM..."
    try:
        llm = init_chat_model(
                model=model,
                model_provider="openai",
                api_key=apiKey,
                base_url=baseUrl,
            )
        yield "loaded LLM.\nreading script..."
        script = readScript(scriptPath)
        yield "got script."
        if script:
            yield "writing prompt..."
            prompt = writePrompt(
                        script, 
                        scriptType, 
                        scriptDescription,
                    )
            yield "wrote prompt.\nasking LLM..."
            response = llm.invoke(prompt)
            yield "***************ANSWER FROM LLM***************\n"
            _ = response.content
        else:
            _ = "something wrong when load script."
    except Exception as e:
        _ = f"{e}"
    finally:
        yield _+DELIMITER