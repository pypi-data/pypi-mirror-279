<p align="left">
    <a href="README_zh.md">中文</a>&nbsp ｜ &nbsp<a>English&nbsp </a>
</p>

# <p align="center">CodeFuse-muAgent: A Multi-Agent FrameWork For Faster Build Agents</p>

<p align="center">
    <a href="README.md"><img src="https://img.shields.io/badge/文档-中文版-yellow.svg" alt="ZH doc"></a>
    <a href="README_en.md"><img src="https://img.shields.io/badge/document-English-yellow.svg" alt="EN doc"></a>
    <img src="https://img.shields.io/github/license/codefuse-ai/CodeFuse-muAgent" alt="License">
    <a href="https://github.com/codefuse-ai/CodeFuse-muAgent/issues">
      <img alt="Open Issues" src="https://img.shields.io/github/issues-raw/codefuse-ai/CodeFuse-muAgent" />
    </a>
    <br><br>
</p>



## 🔔 News
- [2024.04.01] codefuse-muagent is now open source, featuring functionalities such as knowledge base, code library, tool usage, code interpreter, and more

## 📜 Contents
- [🤝 Introduction](#-Introduction)
- [🚀 QuickStart](#-QuickStart)
- [🧭 Key Technologies](#-Key-Technologies)
- [🗂 Miscellaneous](#-Miscellaneous)
  - [📱 Contact Us](#-Contact-Us)


## 🤝 Introduction
Developed by the Ant CodeFuse Team, CodeFuse-muAgent is a Multi-Agent framework whose primary goal is to streamline the Standard Operating Procedure (SOP) orchestration for agents. muagent integrates a rich collection of toolkits, code libraries, knowledge bases, and sandbox environments, enabling users to rapidly construct complex Multi-Agent interactive applications in any field. This framework allows for the efficient execution and handling of multi-layered and multi-dimensional complex tasks.

![](docs/resources/agent_runtime.png)

## 🚀 快速使用
For complete documentation, see: [CodeFuse-muAgent](https://codefuse-ai.github.io/docs/api-docs/MuAgent/overview/multi-agent)
For more [demos](https://codefuse-ai.github.io/docs/api-docs/MuAgent/connector/customed_examples)

1. Installation
```
pip install codefuse-muagent
```

2. Code answer Prepare related llm and embedding model configurations
```
import os

# set your config
api_key = ""
api_base_url= ""
model_name = ""
embed_model = ""
embed_model_path = ""

from muagent.llm_models.llm_config import EmbedConfig, LLMConfig
from muagent.connector.phase import BasePhase
from muagent.connector.schema import Message, Memory
from muagent.codechat.codebase_handler.codebase_handler import CodeBaseHandler

llm_config = LLMConfig(
    model_name=model_name, api_key=api_key,  api_base_url=api_base_url, temperature=0.3
)

embed_config = EmbedConfig(
    embed_engine="model", embed_model=embed_model, embed_model_path=embed_model_path
)
```

<br>

Initialize the codebase
```
from muagent.base_configs.env_config import CB_ROOT_PATH
codebase_name = 'client_local'
code_path = "D://chromeDownloads/devopschat-bot/client_v2/client"

cbh = CodeBaseHandler(
    codebase_name, code_path, crawl_type='dir', use_nh=use_nh,local_graph_path=CB_ROOT_PATH,
    llm_config=llm_config, embed_config=embed_config
)
cbh.import_code(do_interpret=do_interpret)
```

<br>

Start codebase Q&A
```
# 
phase_name = "codeChatPhase"
phase = BasePhase(
    phase_name, embed_config=embed_config, llm_config=llm_config,
)
# 
query_content = "what does the remove' function?"
query = Message(
    role_name="user", role_type="human", input_query=query_content,
    code_engine_name=codebase_name, score_threshold=1.0, top_k=3, cb_search_type="tag",
    local_graph_path=CB_ROOT_PATH, use_nh=False
    )
output_message3, output_memory3 = phase.step(query)
print(output_memory3.to_str_messages(return_all=True, content_key="parsed_output_list"))
```

## Key Technologies

- Agent Base：Four fundamental Agent types are constructed – BaseAgent, ReactAgent, ExecutorAgent, SelectorAgent, supporting basic activities across various scenarios 
- Communication: Information transmission between Agents is accomplished through Message and Parse Message entities, interacting with Memory Manager and managing memories in the Memory Pool 
- Prompt Manager: Customized Agent Prompts are automatically assembled with the aid of Role Handler, Doc/Tool Handler, Session Handler, and Customized Handler 
- Memory Manager: Facilitates the management of chat history storage, information compression, and memory retrieval, culminating in storage within databases, local systems, and vector databases via the Memory Pool 
- Component: Auxiliary ecosystem components to construct Agents, including Retrieval, Tool, Action, Sandbox, etc. 
- Customized Model: Supports the integration of private LLM and Embedding models

##  Contribution
We are deeply grateful for your interest in the Codefuse project and warmly welcome any suggestions, opinions (including criticism), comments, and contributions. 

Feel free to raise your suggestions, opinions, and comments directly through GitHub Issues. There are numerous ways to participate in and contribute to the Codefuse project: code implementation, writing tests, process tool improvements, documentation enhancements, etc. 

We welcome any contribution and will add you to the list of contributors. See [Contribution Guide...](https://codefuse-ai.github.io/contribution/contribution)


## 🗂 Miscellaneous
### 📱 Contact Us
<div align=center>
  <img src="docs/resources/wechat.png" alt="图片", width="360">
</div>
