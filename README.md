## Goal

- [x] スクレイピングできる
- [x] AWS で実行できる
- [x] 定期的に実行できる
- [x] 環境を再現できる

## init

```sh
poetry config virtualenvs.in-project true
poetry install
cp .chalice/example.config.json .chalice/config.json
# And edit .chalice/config.json for credential variables
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

# poetry で install した libs を CLI 実行したい時に使う
poetry shell
```

### chalice docs

https://aws.github.io/chalice/topics/events.html#scheduled-events

### chalice deploy の IAM 権限

以下の policy 作ったらできた
https://github.com/aws/chalice/issues/59#issuecomment-785777473
