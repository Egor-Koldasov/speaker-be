"""Tests for main CLI entry point."""

import argparse

from unittest.mock import patch

import pytest

from langtools.mcp.main import main, parse_args


class TestCLI:
    """Test cases for CLI functionality."""

    def test_parse_args_defaults(self):
        """Test argument parsing with defaults."""
        with patch("sys.argv", ["langtools-mcp"]):
            args = parse_args()
            assert args.verbose is False

    def test_parse_args_verbose(self):
        """Test argument parsing with verbose flag."""
        with patch("sys.argv", ["langtools-mcp", "--verbose"]):
            args = parse_args()
            assert args.verbose is True

    def test_parse_args_verbose_short(self):
        """Test argument parsing with verbose short flag."""
        with patch("sys.argv", ["langtools-mcp", "-v"]):
            args = parse_args()
            assert args.verbose is True

    def test_parse_args_version(self):
        """Test version argument."""
        with patch("sys.argv", ["langtools-mcp", "--version"]), pytest.raises(SystemExit):
            parse_args()

    def test_main_success(self):
        """Test successful main execution."""
        with patch("langtools.mcp.main.mcp") as mock_mcp:
            with patch("langtools.mcp.main.parse_args") as mock_parse_args:
                mock_parse_args.return_value = argparse.Namespace(verbose=False)
                mock_mcp.run.return_value = None

                main()

                mock_mcp.run.assert_called_once()

    def test_main_verbose(self):
        """Test main execution with verbose logging."""
        with patch("langtools.mcp.main.mcp") as mock_mcp:
            with patch("langtools.mcp.main.parse_args") as mock_parse_args:
                with patch("logging.getLogger") as mock_get_logger:
                    mock_parse_args.return_value = argparse.Namespace(verbose=True)
                    mock_logger = mock_get_logger.return_value
                    mock_mcp.run.return_value = None

                    main()

                    mock_mcp.run.assert_called_once()
                    mock_logger.setLevel.assert_called_once()

    def test_main_keyboard_interrupt(self):
        """Test handling of keyboard interrupt."""
        with patch("langtools.mcp.main.mcp") as mock_mcp:
            with patch("langtools.mcp.main.parse_args") as mock_parse_args:
                mock_parse_args.return_value = argparse.Namespace(verbose=False)
                mock_mcp.run.side_effect = KeyboardInterrupt()

                # Should not raise exception
                main()

                mock_mcp.run.assert_called_once()

    def test_main_exception(self):
        """Test handling of general exceptions."""
        with patch("langtools.mcp.main.mcp") as mock_mcp:
            with patch("langtools.mcp.main.parse_args") as mock_parse_args:
                mock_parse_args.return_value = argparse.Namespace(verbose=False)
                mock_mcp.run.side_effect = Exception("Server error")

                with pytest.raises(SystemExit):
                    main()

                mock_mcp.run.assert_called_once()
