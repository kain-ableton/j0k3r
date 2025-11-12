#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###
# Core > Process Launcher
###
import os
import subprocess
import sys
from typing import Dict, Optional, Sequence, Tuple, Union

from lib.output.Logger import logger

CommandType = Union[str, Sequence[str]]


class ProcessLauncher:

    def __init__(self, command: CommandType, *, cwd: Optional[str] = None,
                 env: Optional[Dict[str, str]] = None, shell: Optional[bool] = None):
        """Initialize the launcher with the command to execute."""

        if isinstance(command, str):
            self.command = command.strip()
        else:
            self.command = tuple(command)
        self.cwd = cwd
        self.env = env or {}
        if shell is None:
            self.shell = isinstance(command, str)
        else:
            self.shell = shell

    # ------------------------------------------------------------------------------------

    def start(self, *, cwd: Optional[str] = None,
              env: Optional[Dict[str, str]] = None,
              shell: Optional[bool] = None) -> Tuple[int, str]:
        """Start the process in the current terminal."""

        return self.__create_subprocess(
            self.command,
            cwd=cwd if cwd is not None else self.cwd,
            env=env if env is not None else self.env,
            shell=self.shell if shell is None else shell,
        )

    def start_in_new_window(self, title=None, *, cwd: Optional[str] = None,
                            env: Optional[Dict[str, str]] = None) -> Tuple[int, str]:
        """Start process in a new terminal window using gnome-terminal."""

        cmd = 'gnome-terminal '
        if title is not None:
            cmd += '--title="{0}" '.format(title.replace('"', '\\"'))
        cmd += '--geometry=140x80 '
        cmd += '--command="bash -c \'{0}; exec bash\'"'.format(
            self._command_as_shell_string())
        return self.__create_subprocess(cmd, cwd=cwd, env=env, shell=True)

    def start_in_new_tab(self, *, cwd: Optional[str] = None,
                         env: Optional[Dict[str, str]] = None) -> Tuple[int, str]:
        """Start process in new tab in current terminal session."""

        cmd = 'WID=$(xprop -root | grep "_NET_ACTIVE_WINDOW(WINDOW)"| '
        cmd += 'awk \'{print $5}\');'
        cmd += 'xdotool windowfocus $WID;'
        cmd += 'xdotool key ctrl+shift+t;'
        cmd += 'xdotool type "{0}";'.format(self._command_as_shell_string())
        cmd += 'xdotool key Return'
        return self.__create_subprocess(cmd, cwd=cwd, env=env, shell=True)

    # ------------------------------------------------------------------------------------

    def _command_as_shell_string(self) -> str:
        if isinstance(self.command, str):
            return self.command.strip()
        return ' '.join(subprocess.list2cmdline([part]) for part in self.command)

    @staticmethod
    def __create_subprocess(cmd: CommandType, *, cwd: Optional[str] = None,
                            env: Optional[Dict[str, str]] = None,
                            shell: bool = False) -> Tuple[int, str]:
        """Run a command, streaming combined stdout/stderr to the console."""

        merged_env: Dict[str, str] = os.environ.copy()
        if env:
            merged_env.update(env)

        try:
            process = subprocess.Popen(
                cmd,
                shell=shell,
                executable='/bin/bash' if shell else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=cwd,
                env=merged_env,
                text=True,
                bufsize=1,
            )
        except Exception as exc:  # pragma: no cover - surface launch issues
            logger.error('Error when trying to run command: {exception}'.format(
                exception=exc))
            return (-1, '')

        output_lines = []
        try:
            assert process.stdout is not None  # for type checkers
            for line in process.stdout:
                sys.stdout.write(line)
                output_lines.append(line)
        finally:
            if process.stdout is not None:
                process.stdout.close()
            process.wait()

        return (process.returncode, ''.join(output_lines))
