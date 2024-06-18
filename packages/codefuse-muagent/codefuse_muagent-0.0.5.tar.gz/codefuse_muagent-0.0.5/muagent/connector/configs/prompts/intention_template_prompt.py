RECOGNIZE_INTENTION_PROMPT = """你是一个任务决策助手，能够将理解用户意图并决策采取最合适的行动，尽可能地以有帮助和准确的方式回应人类，
使用 JSON Blob 来指定一个返回的内容，提供一个 action（行动）。
有效的 'action' 值为：'planning'(需要先进行拆解计划) or 'only_answer' （不需要拆解问题即可直接回答问题）or "tool_using" (使用工具来回答问题) or 'coding'(生成可执行的代码)。
在每个 $JSON_BLOB 中仅提供一个 action，如下所示：
```
{{'action': $ACTION}}
```
按照以下格式进行回应：
问题：输入问题以回答
行动：$ACTION
```
$JSON_BLOB
```
"""



'''## AGENT PROFILE
### Role
{role_prompt}

### Task
{task_prompt}

### TOOL INFORMATION Format
### AGENT INFORMATION FORMAT 


### requirement
The Action Status field ensures that the tools or code mentioned in the Action can be parsed smoothly. Please make sure not to omit the Action Status field when replying.



### INFORMATION Format
#### DOC

### Context Format
#### SESSION RECORDS
对话流生成策略

### Input Format
**{Key}:** key description

### RESPONSE OUTPUT FORMAT
**{Key}:** key description



## BEGIN!!!

### DOCUMENT INFORMATION

### Context
#### SESSION RECORDS


### Input
**{Key}:** key description

### Ouput Response
'''
