# Memos Webhook Python Implementation

This is a simple webhook implementation in Python.

It implements a simple URL resource download feature. All url [you-get](https://github.com/soimort/you-get) support for command `you-get https://xxxxx` can be configured to download. 

## Quick Feel It

1. Create a `docker_compose.yaml` with following contents. Replace `xxxxxxxx` with your memos token.

    ```yaml
    version: "3.0"
    services:
    memos:
        networks:
        - memos
        image: neosmemo/memos:0.22.1
        container_name: memos
        ports:
        - 5230:5230
    webhook:
        image: ghcr.io/ryojerryyu/memos-webhook-py:0.3.0
        networks:
        - memos
        container_name: webhook
        environment:
        - LOG_LEVEL=debug
        - WEBHOOK_PORT=8000
        - MEMOS_HOST=memos
        - MEMOS_PORT=5230
        - MEMOS_TOKEN=xxxxxxxx
        volumes:
        - ./.download:/app/download

    networks:
    memos:
    ```

2. Run `docker-compose up -d` to start the services.

3. Access `localhost:5230` , login and make sure the Memos server work. Create a webhook to `http://webhook:8000/webhook` . (It's for Memos server after 0.22.2. For before 0.22.1, use `http://webhook:8000/webhook_old`)

4. Post a memo with contents containing a twitter url. If that tweet was attached with some image, the webhook will download them and upload to the Memo server automatically.

You can use a config file to configure what url you want to download. The default config file is [config.yaml](example/config.yaml).


## Config

You can use a config file by setting the environment variable `CONFIG_PATH`. Here is a docker_compose.yaml example:

```yaml
version: "3.0"
services:
  memos:
    networks:
      - memos
    image: neosmemo/memos:0.22.1
    container_name: memos
    ports:
      - 5230:5230
  webhook:
    image: ghcr.io/ryojerryyu/memos-webhook-py:0.3.0
    networks:
      - memos
    container_name: webhook
    environment:
      - CONFIG_PATH=/app/config.yaml
    volumes:
      - ./.download:/app/download
      - ./path/to/your/local/config/file.yaml:/app/config.yaml

networks:
  memos:
```

You should place your config file in `./path/to/your/local/config/file.yaml` and the webhook will read the config from it.

Here is an example of the configuration file: [config.yaml](example/config.yaml)

```yaml
webhook:
  host: localhost
  port: 11100

memos:
  host: localhost
  port: 5230
  token: xxxxxxx

plugins:
  - name: download
    tag: webhook/download
    you_get_plugin:
      patterns:
        - https://twitter.com/\w+/status/\d+
        - https://x.com/\w+/status/\d+
  - name: fix_typos
    tag: task/fix_typos
    zhipu_plugin:
      api_key: xxxxxxx
      prompt: |
        You are a fix typos plugin.
        Please fix the typos in the text.

        The text is:
        ```
        {content}
        ```
```

And config definitionn is in [config.py](src/dependencies/config.py)
