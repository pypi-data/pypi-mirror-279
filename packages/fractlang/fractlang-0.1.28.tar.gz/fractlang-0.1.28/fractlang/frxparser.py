#!/usr/bin/env python
import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import init, Fore
from parsers.var_strict_int import VarStrictIntParser
from parsers.var_strict_string import VarStrictStringParser
from parsers.print import PrintParser
import argparse

# Initialize colorama
init()

# FRXParser class for parsing and transpiling
class FRXParser:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.parsers = [
            VarStrictIntParser(),
            VarStrictStringParser(),
            PrintParser()
        ]

    def parse_line(self, line, line_number):
        for parser in self.parsers:
            try:
                result = parser.parse_line(line, line_number)
                if result:
                    return result
            except ValueError as e:
                print(f'{Fore.RED}{e}{Fore.RESET}')
                raise  # Rethrow the exception

        # If no valid syntax matched, raise ValueError
        raise ValueError(f'{Fore.RED}Error parsing line {line_number}, reason? Invalid syntax: {line}{Fore.RESET}')

    def parse(self, file_content):
        lines = file_content.split('\n')
        python_code = []
        for idx, line in enumerate(lines, start=1):
            try:
                result = self.parse_line(line, idx)
                if result:
                    python_code.append(result)
            except ValueError as e:
                print(e)
                sys.exit(1)  # Exit if there's an error
        return python_code

    def transpile(self):
        try:
            with open(self.input_path, 'r') as file:
                file_content = file.read()
            python_code = self.parse(file_content)

            with open(self.output_path, 'w') as output_file:
                output_file.write('\n'.join(python_code))

            # Execute the generated Python code
            subprocess.run(['python', self.output_path], check=True)
        
        except Exception as e:
            print(f'{Fore.RED}Error during transpilation: {e}{Fore.RESET}')
            sys.exit(1)  # Exit if there's an error

# Watchdog handler to watch for file changes
class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, parser):
        self.parser = parser

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.frx'):
            print(f"Detected change in {event.src_path}")
            self.parser.transpile()

def main():
    parser = argparse.ArgumentParser(description='FRX Compiler')
    parser.add_argument('input_file', metavar='input_file.frx', type=str, help='Input file (.frx)')
    parser.add_argument('-watch', action='store_true', help='Watch for changes in input file')

    args = parser.parse_args()

    input_file = args.input_file
    watch_mode = args.watch

    output_file = 'output.py'   # Replace with your output file

    parser = FRXParser(input_file, output_file)

    if watch_mode:
        event_handler = WatchdogHandler(parser)

        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=False)
        observer.start()

        print(f"Watching for changes in {os.path.abspath(input_file)} (Ctrl+C to exit)")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()
    else:
        parser.transpile()

if __name__ == "__main__":
    main()
