
import sys
import logging
import traceback
from typing import Callable, Optional

from .argparser import ArgParser
from .command import Command
from .exceptions import CommandException
from .interface import Interface
from .utils import validate_type_hints

class Commander:

	def __init__(self, error_handler: Callable[[Exception], None] = None, debug: bool = False):
		self.__error_handler = error_handler
		self.__config_logger(debug)
		self.__commands: list[Command] = []

		@self.command("help")
		def help_command(command: str = None):
			"""
			Show help message or usage message when command is specified.
			:param command: command for which instructions for use will be displayed
			"""
			self.__help_command(command)

	def command(self, *cmds: str) -> Callable[[Callable], Callable]:
		def dec(func: Callable) -> Callable:
			for command in self.__commands:
				if command.match(cmds):
					self.__logger.debug(f"duplicate commands: {func.__name__}, {command.func.__name__}")
					raise CommandException(f"Duplicated command: {", ".join(cmds)}")
			validate_type_hints(func)
			self.__logger.debug(f"append new command: {func.__name__} ({cmds})")
			self.__commands.append(Command(cmds, func))
			return func
		return dec

	def process(self, argv: list[str] = None):
		if argv is None:
			argv = sys.argv[1:]
		command = self.__find_command(argv[0] if len(argv) > 0 else "help")
		if command is None:
			print(f"\nUnknown command '{argv[0]}'")
			self.__help_command()
			return
		try:
			args, kwargs = ArgParser.parse(argv[1:], command)
			command.func(*args, **kwargs)
		except CommandException as e:
			print("\n" + str(e))
			Interface.command_usage(command)
		except Exception as e:
			print("\n" + traceback.format_exc())
			if isinstance(self.__error_handler, Callable):
				self.__error_handler(e)

	def __find_command(self, cmd: str) -> Optional[Command]:
		for command in self.__commands:
			if command.match(cmd):
				return command

	def __help_command(self, cmd: str = None):
		if cmd is not None:
			command = self.__find_command(cmd)
			if command and command.match(cmd):
				Interface.command_usage(command)
				return
		Interface.commands_list(self.__commands)

	def __config_logger(self, debug: bool = False):
		self.__logger = logging.getLogger("petcmd")
		if not debug:
			self.__logger.disabled = True
			return
		self.__logger.setLevel(logging.DEBUG)
		handler = logging.StreamHandler()
		handler.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s',
			datefmt='%Y/%m/%d %H:%M:%S')
		handler.setFormatter(formatter)
		self.__logger.addHandler(handler)

