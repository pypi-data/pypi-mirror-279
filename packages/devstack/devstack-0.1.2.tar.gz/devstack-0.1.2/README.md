# devstack

A tool for managing docker stacks.

It reads a yaml file in the docker-compose (for swarm) format and creates the following things:
- a stack name using the 'stem' part of the file (ex: omg.yml → stack name = omg)
- create every external network defined in the file before starting the stack.
- deploy the stack using `docker stack deploy`

In the spirit of kubectl command, `devstack` command take a yaml file as argument.

## List of currently implemented commands:

```
Usage: devstack [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  logs
  create
  status
  destroy
```

* devstack create {stack file}.yml
* devstack status {stack file}.yml
* devstack logs {stack file}.yml {service defined in stack}
* devstack destroy {stack file}.yml

## Example

Go to examples directory a play with the `devstack` command:

```
# cd examples
# devstack create test.yml
Creating service test_nginx
# devstack status test.yml
ID             NAME         MODE         REPLICAS   IMAGE          PORTS
t952y8uhg7wk   test_nginx   replicated   1/1        nginx:alpine   *:8088->80/tcp
# curl http://127.0.0.1:8088
<!DOCTYPE html>
<html lang="en">
<body>
    <h1>Hello world!</h1>
</body>
</html>
# devstack logs test.yml nginx
...
test_nginx.1.1aeijjmut4rh@thosil02    | 2024/03/13 13:28:10 [notice] 1#1: start worker process 46
test_nginx.1.1aeijjmut4rh@thosil02    | 2024/03/13 13:28:10 [notice] 1#1: start worker process 47
test_nginx.1.1aeijjmut4rh@thosil02    | 2024/03/13 13:28:10 [notice] 1#1: start worker process 48
test_nginx.1.1aeijjmut4rh@thosil02    | 2024/03/13 13:28:10 [notice] 1#1: start worker process 49
test_nginx.1.1aeijjmut4rh@thosil02    | 10.0.0.2 - - [13/Mar/2024:13:28:35 +0100] "GET / HTTP/1.1" 200 81 "-" "curl/8.2.1" "-"
^C
Aborted.
# devstack destroy test.yml
Removing service test_nginx
```

## Contributing

This is a python project, with [poetry](https://python-poetry.org/) as package manager

- [install poetry](https://python-poetry.org/docs/#installation)
- install deps: `poetry install`
- make yourself confident with [Typer](https://github.com/tiangolo/typer)
 

Have fun