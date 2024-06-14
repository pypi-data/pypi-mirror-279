# LogAssist

A simple and customizable logging library for Python.

## Installation

```powershell
pip install LogAssist
```

## Features

- Easy to use and configure
- Supports multiple log levels (debug, info, warning, error)
- Outputs log messages to both console and file
- Allows for log file removal on initialization
- Provides datetime formatting for log messages

## Usage

1. Import the Logger class:

```python
from LogAssist.log import Logger
```

2. Initialize the logger with your desired settings:

```python
Logger.init(log_level='verbose', dir_name='./log', file_name='my_log.log', prev_log_remove=True, out_console=True, out_file=True)
# or
Logger.init()
```

3. Use the logger in your code:

```python
Logger.verbose('MyTag', 'This is a verbose message')
Logger.debug('MyTag', 'This is a debug message')
Logger.info('MyTag', 'This is an info message')
Logger.warning('MyTag', 'This is a warning message')
Logger.error('MyTag', 'This is an error message', exc_info=sys.exc_info())
```

## Configuration

You can configure the logger using the init method or by passing a dictionary of logger information to the logger_init method. The available options are:

- log_level: The log level to set (verbose, debug, info, warning, or error). Default is 'verbose'.
- dir_name: The directory name to use for log files. Default is './log'.
- file_name: The file name to use for logging. Default is None, which will create a file named "Logger.log".
- prev_log_remove: Whether to remove the existing log file on initialization. Default is False.
- out_console: Whether to output log messages to the console. Default is True.
- out_file: Whether to output log messages to a file. Default is True.