import argparse
import pytest
from unittest.mock import patch, mock_open
from tree_maker import main

def test_main_default_args():
    with patch('tree_maker.generate_tree', return_value="tree structure") as mock_generate_tree:
        with patch('builtins.print') as mock_print:
            with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(folder_path='.', depth=None, exclude=[], show_hidden=False, output=None, clipboard=False)):
                main()
                mock_generate_tree.assert_called_once_with('.', None, False, excluded_files=[])
                mock_print.assert_called_once_with('tree_maker_cli\ntree structure')

def test_main_output_to_file():
    with patch('tree_maker.generate_tree', return_value="tree structure") as mock_generate_tree:
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(folder_path='.', depth=None, exclude=[], show_hidden=False, output='output.txt', clipboard=False)):
                main()
                mock_file.assert_called_once_with('output.txt', 'w')
                mock_file().write.assert_called_once_with('tree_maker_cli\ntree structure')

def test_main_clipboard():
    with patch('tree_maker.generate_tree', return_value="tree structure") as mock_generate_tree:
        with patch('pyperclip.copy') as mock_copy:
            with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(folder_path='.', depth=None, exclude=[], show_hidden=False, output=None, clipboard=True)):
                main()
                mock_copy.assert_called_once_with('tree_maker_cli\ntree structure')
                mock_generate_tree.assert_called_once_with('.', None, False, excluded_files=[])
