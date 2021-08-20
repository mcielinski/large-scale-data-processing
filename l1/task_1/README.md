# L1 - 2019

## Task 1
Write shell (Bash) scripts, which:
- copies certain files from one machine to another
```bash
$ ./copy.sh <user@source-machine-IP:/path/to/files> <user@target-machine-IP:/path/to/files> <file-1> <file-2> ... <file-N>
```
- runs an infinite command in background and kills the command (use: `&`, `kill/killall/pidof`)
```bash
$ ./run-backgroud.sh <command-to-run>
$ ./kill.sh <command-to-run>
```
- filters an random data stream (use: `/dev/urandom`.  `sed/tr`)
```bash
$ ./filter.sh
```

