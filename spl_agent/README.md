# SPL 纯生成器

这个项目只保留一项能力：对 **Git 仓库 URL** 生成 SPL，并最终只保留一个 markdown 文件。

## 行为

- 仅支持输入 Git 仓库 URL
- 在 `spl_agent/.spl_i` 下创建临时工作区
- 生成函数级 SPL 内容
- 汇总到 `spl_agent/SPL_RESULT.md`（可在配置中改名）
- 自动删除临时源码和中间 SPL 文件，只保留 markdown 结果

## 使用

```bash
python run_from_config.py --config settings.yaml --url https://github.com/owner/repo.git
```

指定分支/提交：

```bash
python run_from_config.py --config settings.yaml --url https://github.com/owner/repo.git --commit main
```

或

```bash
spl-run --config settings.yaml --url https://github.com/owner/repo.git
```

## 默认结果文件

- `SPL_RESULT.md`
