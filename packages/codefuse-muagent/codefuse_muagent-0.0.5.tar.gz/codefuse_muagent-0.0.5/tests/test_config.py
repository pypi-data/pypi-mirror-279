import os, openai, base64
from loguru import logger

try:
    from zdatafront import client
    from zdatafront.client import ZDF_COMMON_QUERY_URL
    # from zdatafront import monkey, OPENAI_API_BASE
    # patch openai sdk
    # monkey.patch_openai()
    os.environ["aes_secret_key"] = base64.b64decode('Z3M1NDBpaXZ6ZXptaWRpMw==').decode('utf-8')
    os.environ["visit_domain"] = 'BU_cto'
    os.environ["visit_biz"] = 'BU_cto_code'
    os.environ["visit_biz_line"] = 'BU_cto_code_line'
    os.environ["visit_domain"] = 'BU_code'
    os.environ["visit_biz"] = 'BU_code_gpt4'
    os.environ["visit_biz_line"] = 'BU_code_gpt4_bingchang'
    # zdatafront 提供的统一加密密钥
    client.aes_secret_key = os.environ.get("aes_secret_key")
    # zdatafront 分配的业务标记
    client.visit_domain = os.environ.get("visit_domain")
    client.visit_biz = os.environ.get("visit_biz")
    client.visit_biz_line = os.environ.get("visit_biz_line")
    OPENAI_API_BASE = ZDF_COMMON_QUERY_URL
except Exception as e:
    OPENAI_API_BASE = "https://api.openai.com/v1"
    logger.error(e)
    pass

os.environ["API_BASE_URL"] = OPENAI_API_BASE
os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"
os.environ["model_name"] = "gpt-3.5-turbo"
os.environ["model_engine"] = "openai"

os.environ["API_BASE_URL"] = "https://api.lingyiwanwu.com/v1"
os.environ["OPENAI_API_KEY"] = "d881838442c3449a911c534ba2b1e5ba"
openai.api_key = "d881838442c3449a911c534ba2b1e5ba"
os.environ["model_name"] =  "yi-34b-chat-0205"
os.environ["model_engine"] = "lingyiwanwu"

os.environ["embed_model"] = "text2vec-base-chinese"
os.environ["embed_model_path"] ="D://project/gitlab/llm/external/ant_code/Codefuse-chatbot/embedding_models/text2vec-base-chinese"

os.environ["DUCKDUCKGO_PROXY"] = os.environ.get("DUCKDUCKGO_PROXY") or "socks5h://127.0.0.1:13659"