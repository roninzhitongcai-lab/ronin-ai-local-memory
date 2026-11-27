# Ronin 个人数据库

## 现状

共享账号按 ISOLATION.md 和 SOUL.md 确认当前身份。Git 中的 Markdown 为原始记录，database/ronin.sqlite3 是它们的本地 SQLite 快照。范围为 USER、SOUL、AGENTS，以及 projects、tasks、knowledge 下的 Markdown。仅使用本仓库资料。

## 使用与下一步

1. 新对话先声明「我是 Ronin，本次只使用我的记忆库 https://github.com/roninzhitongcai-lab/ronin-ai-local-memory」。仅需通用帮助时可跳过个人库。换人另开对话。
2. 确认身份后，拉取最新仓库。在仓库根目录运行 `python3 database/memory.py --owner ronin list` 查看文件清单，或用 `read projects/whalesbot.md` 替换 `list` 读取单篇。
3. 更新 Markdown 后运行 `python3 database/memory.py --owner ronin build`，将数据库及原文一起提交、推送。只让一个人写入；出现版本冲突时先合并 Markdown，再重新生成数据库。
4. 身份参数防误选。该工具无法识别键盘前的人，也无法控制共享账号的聊天历史。其他使用者使用各自的仓库。
