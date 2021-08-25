## Goal

- [ ] スクレイピングできる
- [ ] AWS で実行できる
- [ ] 定期的に実行できる
- [ ] 環境を再現できる

## init

```
poetry config virtualenvs.in-project true
poetry install
```

## Scripts

### Run local

```sh
poetry run task start
```

## Memo

### poetry manual

よく使うコマンド例

```sh
# Install to dev-dependencies
poetry add --dev pylint

# Install exact version
poetry add "Flask==1.1.1"

# Uninstall library from dev-dependencies (注意: npm とは違い、`pyproject.toml` から記述削除しただけでは Uninstall されない)
poetry remove --dev taskipy
```
