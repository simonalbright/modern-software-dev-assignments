# 第 3 周 —— 构建自定义 MCP 服务器

设计并实现一个模型上下文协议（Model Context Protocol，MCP）服务器，使其封装一个真实的外部 API。你可以：
- **本地**运行（STDIO 传输），并与 MCP 客户端（如 Claude Desktop）集成；
- 或**远程**运行（HTTP 传输），由模型代理或客户端调用。后者难度更高，但可获得加分。

如果结合 MCP 授权规范加入认证机制（API Key 或 OAuth2），将额外加分。

## 学习目标
- 理解 MCP 的核心能力：工具（tools）、资源（resources）、提示词（prompts）。
- 实现带类型化参数与稳健错误处理的工具定义。
- 遵循日志与传输的最佳实践（STDIO 服务器不得向 stdout 打印无关内容）。
- （可选）为 HTTP 传输实现授权流程。

## 需求
1. 选择一个外部 API，并说明你将使用它的哪些端点。示例方向：天气、GitHub issues、Notion 页面、影视数据库、日历、任务管理、金融/加密货币、出行、体育数据等。
2. 至少暴露两个 MCP 工具。
3. 实现基本的健壮性：
   - 对 HTTP 失败、超时、空结果给出优雅的错误处理。
   - 尊重 API 限流（例如简单的退避策略，或面向用户的提示）。
4. 打包与文档：
   - 提供清晰的安装说明、环境变量说明与运行命令。
   - 附上一个调用流程示例（在客户端里需要输入/点击什么来触发工具）。
5. 从两种部署方式中选择一种：
   - 本地：STDIO 服务器，可在你自己的机器上运行，并能被 Claude Desktop 或 Cursor 之类的 AI IDE 发现。
   - 远程：可通过网络访问的 HTTP 服务器，能被支持 MCP 的客户端或代理运行时调用。若完成部署且可访问，可获得加分。
6. （可选）加分项：认证
   - 通过环境变量与客户端配置支持 API Key；或
   - 针对 HTTP 传输实现 OAuth2 风格的 Bearer Token，校验令牌受众（audience），且绝不过度转发令牌给上游 API。

## 交付物
- `week3/` 下的源码（建议结构：`week3/server/`，包含一个清晰的入口文件，如 `main.py` 或 `app.py`）。
- `week3/README.md`，需包含：
  - 前置条件、环境搭建与运行说明（本地和/或远程）。
  - 如何配置 MCP 客户端（本地场景以 Claude Desktop 为例）或远程场景下的代理运行时。
  - 工具参考：名称、参数、示例输入/输出与预期行为。

## 评分标准（共 90 分）
- 功能（35 分）：实现了 2 个以上工具，API 集成正确，输出有意义。
- 可靠性（20 分）：输入校验、错误处理、日志、限流意识。
- 开发者体验（20 分）：安装/文档清晰、易于本地运行、目录结构合理。
- 代码质量（15 分）：代码可读、命名清晰、复杂度克制、尽量使用类型注解。
- 加分项（10 分）：
  - +5 提供远程 HTTP MCP 服务器，可被诸如 OpenAI/Claude SDK 之类的代理或客户端调用。
  - +5 正确实现认证（带受众校验的 API Key 或 OAuth2）。

## 参考资源
- MCP 服务器快速上手：[modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)
*注意：你不能直接提交该示例。*
- MCP 授权（HTTP）：[modelcontextprotocol.io/specification/2025-06-18/basic/authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)
- 在 Cloudflare（Agents）上部署远程 MCP：[developers.cloudflare.com/agents/guides/remote-mcp-server/](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)。部署前可先用 modelcontextprotocol 的 inspector 工具在本地调试你的服务器。
- https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel 若你选择远程部署 MCP，Vercel 是带免费额度的不错选择。
