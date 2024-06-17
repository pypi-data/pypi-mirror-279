import asyncio
from pathlib import Path
from typing import Any, Union
from langchain.globals import set_verbose

from caseflow.case_step import CaseStep


def debug_case_step(businessJsonFilePath:Union[Path, str], showLog=True) -> Any:
    """debug for case step

    Args:
        businessJsonFilePath (Union[Path, str]): 业务文件路径
        showLog (bool, optional): 是否展示日志. Defaults to True.

    Returns:
        Any: _description_
    """    
    if showLog:
        set_verbose(True)
    businessCase = CaseStep(step_json_file_path=businessJsonFilePath)
    result = asyncio.run(
        businessCase.ainvoke(
            {},
            config={
                "callbacks": [
                    # CaseStepStdOutCallbackHandler(),
                ]
            },
        ),
    )
    return result
