"""
Tests for AsyncCommand._parse_command_string method.

This module tests the smart command parsing functionality that handles quoted strings
and complex command structures properly.
"""

import unittest
from unittest import skip

from danielutils import AsyncCommand


class TestParseCommandString(unittest.TestCase):
    """Test cases for the _parse_command_string method."""

    def test_basic_parsing(self):
        """Test basic command parsing without quotes."""
        result = AsyncCommand._parse_command_string("echo hello world")
        self.assertListEqual(["echo", "hello", "world"], result)

    def test_empty_string(self):
        """Test parsing empty string."""
        result = AsyncCommand._parse_command_string("")
        self.assertListEqual([], result)

    def test_whitespace_only(self):
        """Test parsing whitespace-only string."""
        result = AsyncCommand._parse_command_string("   \t\n  ")
        self.assertListEqual([], result)

    def test_single_double_quotes(self):
        """Test parsing with double quotes."""
        result = AsyncCommand._parse_command_string('echo "hello world"')
        self.assertListEqual(["echo", "hello world"], result)

    def test_single_quotes(self):
        """Test parsing with single quotes."""
        result = AsyncCommand._parse_command_string("echo 'hello world'")
        self.assertListEqual(["echo", "hello world"], result)

    def test_mixed_quotes(self):
        """Test parsing with mixed single and double quotes."""
        result = AsyncCommand._parse_command_string('echo "hello" and \'world\'')
        self.assertListEqual(["echo", "hello", "and", "world"], result)

    def test_nested_quotes(self):
        """Test parsing with nested quotes."""
        result = AsyncCommand._parse_command_string('echo "He said \'Hello World\'"')
        self.assertListEqual(["echo", "He said 'Hello World'"], result)

    @skip("This is implementation specific because we need escape char")
    def test_escaped_quotes(self):
        """Test parsing with escaped quotes."""
        result = AsyncCommand._parse_command_string('echo "He said "Hello World""')
        self.assertListEqual(["echo", 'He said "Hello World"'], result)

    def test_multiple_spaces(self):
        """Test parsing with multiple spaces between arguments."""
        result = AsyncCommand._parse_command_string("echo    hello    world")
        self.assertListEqual(["echo", "hello", "world"], result)

    def test_leading_trailing_spaces(self):
        """Test parsing with leading and trailing spaces."""
        result = AsyncCommand._parse_command_string("  echo hello world  ")
        self.assertListEqual(["echo", "hello", "world"], result)

    def test_complex_command(self):
        """Test parsing complex command with multiple quoted arguments."""
        result = AsyncCommand._parse_command_string('git commit -m "fix bug" --author "John Doe"')
        self.assertListEqual(["git", "commit", "-m", "fix bug", "--author", "John Doe"], result)

    def test_powershell_command(self):
        """Test parsing PowerShell command with complex quoting."""
        cmd = """powershell -Command "Get-Process | Where-Object {$_.Name -eq 'chrome'}"""""
        result = AsyncCommand._parse_command_string(cmd)
        self.assertListEqual(["powershell", "-Command", "Get-Process | Where-Object {$_.Name -eq 'chrome'}"], result)

    def test_cmd_command(self):
        """Test parsing Windows cmd command."""
        result = AsyncCommand._parse_command_string('cmd /c "echo hello world"')
        self.assertListEqual(["cmd", "/c", "echo hello world"], result)

    def test_unclosed_quotes(self):
        """Test parsing with unclosed quotes (should still work)."""
        result = AsyncCommand._parse_command_string('echo "unclosed quote')
        self.assertListEqual(["echo", "unclosed quote"], result)

    def test_quotes_at_end(self):
        """Test parsing with quotes at the end."""
        result = AsyncCommand._parse_command_string('echo hello "world"')
        self.assertListEqual(["echo", "hello", "world"], result)

    def test_quotes_at_beginning(self):
        """Test parsing with quotes at the beginning."""
        result = AsyncCommand._parse_command_string('"hello world" echo')
        self.assertListEqual(["hello world", "echo"], result)

    def test_only_quoted_string(self):
        """Test parsing only a quoted string."""
        result = AsyncCommand._parse_command_string('"hello world"')
        self.assertListEqual(["hello world"], result)

    def test_empty_quotes(self):
        """Test parsing with empty quotes."""
        result = AsyncCommand._parse_command_string('echo "" hello')
        self.assertListEqual(["echo", "hello"], result)

    def test_single_character_args(self):
        """Test parsing single character arguments."""
        result = AsyncCommand._parse_command_string("a b c d")
        self.assertListEqual(["a", "b", "c", "d"], result)

    def test_special_characters(self):
        """Test parsing with special characters."""
        result = AsyncCommand._parse_command_string('echo "path/to/file with spaces.txt"')
        self.assertListEqual(["echo", "path/to/file with spaces.txt"], result)

    def test_unicode_characters(self):
        """Test parsing with unicode characters."""
        result = AsyncCommand._parse_command_string('echo "Hello 世界"')
        self.assertListEqual(["echo", "Hello 世界"], result)

    def test_tab_characters(self):
        """Test parsing with tab characters."""
        result = AsyncCommand._parse_command_string("echo hello\tworld")
        self.assertListEqual(["echo", "hello\tworld"], result)

    def test_newline_characters(self):
        """Test parsing with newline characters."""
        result = AsyncCommand._parse_command_string("echo hello\nworld")
        self.assertListEqual(["echo", "hello\nworld"], result)

    def test_quotes_with_spaces_around(self):
        """Test parsing with spaces around quotes."""
        result = AsyncCommand._parse_command_string('echo " hello world " ')
        self.assertListEqual(["echo", " hello world "], result)

    def test_multiple_quoted_sections(self):
        """Test parsing multiple quoted sections."""
        result = AsyncCommand._parse_command_string('echo "first" and "second"')
        self.assertListEqual(["echo", "first", "and", "second"], result)

    def test_quotes_with_escaped_backslashes(self):
        """Test parsing with escaped backslashes in quotes."""
        result = AsyncCommand._parse_command_string('echo "path\\to\\file"')
        self.assertListEqual(["echo", "path\\to\\file"], result)

    def test_real_world_examples(self):
        """Test with real-world command examples."""
        # Chrome command
        chrome_cmd = 'chrome --user-data-dir="C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1" --profile-directory="Profile 1" "https://example.com"'
        result = AsyncCommand._parse_command_string(chrome_cmd)
        expected = [
            "chrome",
            "--user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1",
            "--profile-directory=Profile 1",
            "https://example.com"
        ]
        self.assertListEqual(expected, result)

        # Docker command
        docker_cmd = 'docker run -it --name "my container" ubuntu:latest /bin/bash'
        result = AsyncCommand._parse_command_string(docker_cmd)
        expected = ["docker", "run", "-it", "--name", "my container", "ubuntu:latest", "/bin/bash"]
        self.assertListEqual(expected, result)

    def test_edge_cases(self):
        """Test various edge cases."""
        # Only spaces
        result = AsyncCommand._parse_command_string("   ")
        self.assertListEqual([], result)

        # Only quotes
        result = AsyncCommand._parse_command_string('""')
        self.assertListEqual([], result)

        # Quote in the middle
        result = AsyncCommand._parse_command_string('echo "hello" world')
        self.assertListEqual(["echo", "hello", "world"], result)

        # Multiple consecutive quotes
        result = AsyncCommand._parse_command_string('echo """"')
        self.assertListEqual(["echo"], result)

    def test_performance_with_long_command(self):
        """Test performance with a long command string."""
        long_command = ' '.join(['arg' + str(i) for i in range(1000)])
        result = AsyncCommand._parse_command_string(long_command)
        self.assertEqual(1000, len(result))
        self.assertEqual("arg0", result[0])
        self.assertEqual("arg999", result[-1])

    def test_process_list(self):
        actual = AsyncCommand._parse_command_string('tasklist /FI "IMAGENAME eq {self.app_name}" /FO CSV')
        self.assertListEqual(["tasklist", "/FI", "IMAGENAME eq {self.app_name}", "/FO", "CSV"], actual)


if __name__ == '__main__':
    unittest.main()
