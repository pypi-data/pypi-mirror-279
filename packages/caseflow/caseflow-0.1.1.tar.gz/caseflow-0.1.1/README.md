# caseflow

使用langchain 的LCEL语法来编排用例组成，每一步，每一个用例都是runnable对象。

每个步骤或用例都可使用 lanngchain的callbackmanager、retry等

每个自动化用例都可装饰成agent tool，供agent使用。此agent即为具有AI的RPA（Robotic Process Automation）。

用例采用接口录制har文件转接口自动化用例，并完成用例参数化。（todo: 此转换过程也可交由agent来自动转换）

# 安装

``` shell
pip install caseflow
```

# 示例

``` python

import asyncio

from langchain_core.globals import set_verbose

from caseflow import CaseStep
from caseflow.run_case import parse_har

set_verbose(True)

stepJson_1 = parse_har("file/request.step_1.har")
stepJson_2 = parse_har("file/request.step_2.har")

flow = (
    CaseStep(step_json_file_path=stepJson_1)
    | CaseStep(step_json_file_path=stepJson_2)
)
    

# invoke
result = flow.invoke({})
print(result)

# ainvoke
result = asyncio.run(
    flow.ainvoke(
        {},
        config={
            "callbacks": [
                # CaseStepStdOutCallbackHandler(),
            ]
        },
    )
)
print(result)

# stream
for chunk in flow.stream({}):
    print(chunk)


# astream
async def stream_output():
    async for chunk in flow.astream({}):
        print(chunk)


asyncio.run(stream_output())

```

