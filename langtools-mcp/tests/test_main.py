"""Tests for main CLI entry point."""

from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from langtools.mcp.main import Args, main, parse_args


class TestCLI:
    """Test cases for CLI functionality."""

    def test_parse_args_defaults(self) -> None:
        """Test argument parsing with defaults."""
        with patch("sys.argv", ["langtools-mcp"]):
            args = parse_args()
            assert args.verbose is False

    def test_parse_args_verbose(self) -> None:
        """Test argument parsing with verbose flag."""
        with patch("sys.argv", ["langtools-mcp", "--verbose"]):
            args = parse_args()
            assert args.verbose is True

    def test_parse_args_verbose_short(self) -> None:
        """Test argument parsing with verbose short flag."""
        with patch("sys.argv", ["langtools-mcp", "-v"]):
            args = parse_args()
            assert args.verbose is True

    def test_parse_args_version(self) -> None:
        """Test version argument."""
        with patch("sys.argv", ["langtools-mcp", "--version"]), pytest.raises(SystemExit):
            parse_args()

    def test_main_success(self) -> None:
        """Test successful main execution."""
        with patch("langtools.mcp.main.mcp") as mock_mcp:
            with patch("langtools.mcp.main.parse_args") as mock_parse_args:
                mock_parse_args.return_value = Args(verbose=False)
                run_mock = cast(MagicMock, mock_mcp.run)
                run_mock.return_value = None

                main()

                run_mock.assert_called_once()

    def test_main_verbose(self) -> None:
        """Test main execution with verbose logging."""
        with patch("langtools.mcp.main.mcp") as mock_mcp:
            with patch("langtools.mcp.main.parse_args") as mock_parse_args:
                with patch("logging.getLogger") as mock_get_logger:
                    mock_parse_args.return_value = Args(verbose=True)
                    mock_logger = cast(MagicMock, mock_get_logger.return_value)
                    run_mock = cast(MagicMock, mock_mcp.run)
                    run_mock.return_value = None

                    main()

                    run_mock.assert_called_once()
                    set_level_mock = cast(MagicMock, mock_logger.setLevel)
                    set_level_mock.assert_called_once()

    def test_main_keyboard_interrupt(self) -> None:
        """Test handling of keyboard interrupt."""
        with patch("langtools.mcp.main.mcp") as mock_mcp:
            with patch("langtools.mcp.main.parse_args") as mock_parse_args:
                mock_parse_args.return_value = Args(verbose=False)
                run_mock = cast(MagicMock, mock_mcp.run)
                run_mock.side_effect = KeyboardInterrupt()

                # Should not raise exception
                main()

                run_mock.assert_called_once()

    def test_main_exception(self) -> None:
        """Test handling of general exceptions."""
        with patch("langtools.mcp.main.mcp") as mock_mcp:
            with patch("langtools.mcp.main.parse_args") as mock_parse_args:
                mock_parse_args.return_value = Args(verbose=False)
                run_mock = cast(MagicMock, mock_mcp.run)
                run_mock.side_effect = Exception("Server error")

                with pytest.raises(SystemExit):
                    main()

                run_mock.assert_called_once()
