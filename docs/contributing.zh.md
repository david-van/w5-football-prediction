# 为 W-5 足球预测框架做贡献

感谢您有兴趣为 W-5 项目做出贡献！本文档提供了为这个研究实现做贡献的指南。

## 行为准则

我们致力于提供一个欢迎和包容的环境。请在所有互动中保持尊重和建设性。

## 如何贡献

### 报告问题

如果您发现错误或有建议：

1. 检查 [GitHub Issues](https://github.com/Winner12-AI/w5-football-prediction/issues) 中是否已存在该问题
2. 如果没有，创建一个新问题，包括：
   - 清晰的标题和描述
   - 重现步骤（针对错误）
   - 预期与实际行为
   - 您的环境信息（操作系统、Python 版本等）

### 提交代码

1. **Fork 仓库**并创建新分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **进行更改**：
   - 编写清晰、有注释的代码
   - 遵循现有的代码风格
   - 为新功能添加测试
   - 根据需要更新文档

3. **测试您的更改**：
   ```bash
   pytest tests/
   ```

4. **使用清晰的提交信息**：
   ```bash
   git commit -m "Add: Brief description of changes"
   ```

5. **推送并创建 Pull Request**：
   ```bash
   git push origin feature/your-feature-name
   ```

## 开发环境设置

```bash
# Clone 你的 fork
git clone https://github.com/Winner12-AI/w5-football-prediction.git
cd w5-football-prediction

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows 上：venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install pytest pytest-cov mypy black flake8

# 运行测试
pytest tests/
```

## 代码风格

我们遵循 PEP 8 风格指南。要点：

- 使用 4 个空格缩进（不使用制表符）
- 最大行长度：88 个字符（Black 默认）
- 使用描述性的变量名
- 为所有函数和类添加文档字符串
- 鼓励使用类型提示

使用 Black 格式化代码：
```bash
black src/ examples/
```

使用 flake8 检查：
```bash
flake8 src/ examples/
```

## 测试

- 为新功能编写单元测试
- 在提交 PR 前确保所有测试通过
- 目标代码覆盖率 >80%

```bash
# 运行带覆盖率的测试
pytest --cov=src tests/
```

## 文档

- 添加新功能时更新 README.md
- 为新函数/类添加文档字符串
- 更新 `docs/` 中的相关文档
- 在适当的情况下包含使用示例

## 我们接受的内容

✅ **我们欢迎以下贡献：**
- 修复错误或改进现有代码
- 添加新的基线模型或评估指标
- 改进文档和示例
- 提高代码质量和测试覆盖率
- 添加对新数据源的支持（具有适当的许可）

## 我们不接受的内容

❌ **我们不能接受以下贡献：**
- 包含未经授权的专有数据
- 试图逆向工程商业模型
- 添加赌博或博彩功能
- 违反道德准则或许可协议
- 包含恶意代码或安全漏洞

## 研究贡献

如果您的贡献涉及新研究：

1. 提供清晰的方法论文档
2. 包含相关论文的引用
3. 确保可重复性并提供样本数据
4. 考虑单独发布您的发现

## 商业用途

本项目是开源的（MIT 许可证），但请注意：

- 商业产品 WINNER12 包含专有增强功能
- 如果您构建商业应用程序，请：
  - 正确归属 W-5 框架
  - 遵守所有适用的法律法规
  - 考虑道德影响

## 有问题？

- **技术问题**：[GitHub Issues](https://github.com/Winner12-AI/w5-football-prediction/issues)
- **商业咨询**：[WINNER12 网站](https://winner12.ai)

## 许可证

通过贡献，您同意您的贡献将根据 MIT 许可证进行许可。

---

感谢您帮助改进 W-5 框架！🚀⚽
