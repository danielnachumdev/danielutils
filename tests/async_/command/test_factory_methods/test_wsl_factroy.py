import unittest
import os

from danielutils.async_.async_command import AsyncCommand
from ..base import BaseCommandTest

class TestWslFactory(BaseCommandTest):
    """Test cases for AsyncCommand.wsl factory method."""

    @classmethod
    def setUpClass(cls):
        """Check if WSL is available before running any tests."""
        super().setUpClass()

        # Test if WSL is available by running a simple command
        try:
            import subprocess
            result = subprocess.run(['wsl', 'echo', 'test'],
                                    capture_output=True,
                                    text=True,
                                    timeout=10)
            if result.returncode != 0:
                raise unittest.SkipTest("WSL is not available or not working properly")
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            raise unittest.SkipTest("WSL is not available on this system")

    def test_echo_one_word_unquoted(self):
        """Test echo with one word unquoted."""
        cmd = AsyncCommand.wsl("echo test")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test", result.stdout.strip())

    def test_echo_two_words_unquoted(self):
        """Test echo with two words unquoted."""
        cmd = AsyncCommand.wsl("echo hello world")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello world", result.stdout.strip())

    def test_echo_sentence_unquoted(self):
        """Test echo with sentence unquoted."""
        cmd = AsyncCommand.wsl("echo this is a test sentence")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("this is a test sentence", result.stdout.strip())

    def test_echo_one_word_double_quoted(self):
        """Test echo with one word double quoted."""
        cmd = AsyncCommand.wsl('echo "test"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test", result.stdout.strip())

    def test_echo_two_words_double_quoted(self):
        """Test echo with two words double quoted."""
        cmd = AsyncCommand.wsl('echo "hello world"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello world", result.stdout.strip())

    def test_echo_sentence_double_quoted(self):
        """Test echo with sentence double quoted."""
        cmd = AsyncCommand.wsl('echo "this is a test sentence"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("this is a test sentence", result.stdout.strip())

    def test_echo_one_word_single_quoted(self):
        """Test echo with one word single quoted."""
        cmd = AsyncCommand.wsl("echo 'test'")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test", result.stdout.strip())

    def test_echo_two_words_single_quoted(self):
        """Test echo with two words single quoted."""
        cmd = AsyncCommand.wsl("echo 'hello world'")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello world", result.stdout.strip())

    def test_echo_sentence_single_quoted(self):
        """Test echo with sentence single quoted."""
        cmd = AsyncCommand.wsl("echo 'this is a test sentence'")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("this is a test sentence", result.stdout.strip())

    def test_echo_multiple_quotes(self):
        """Test echo with multiple quotes."""
        cmd = AsyncCommand.wsl('echo "hello" "world" "test"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello", result.stdout.strip())
        self.assertIn("world", result.stdout.strip())
        self.assertIn("test", result.stdout.strip())

    def test_echo_mixed_quote_types(self):
        """Test echo with mixed quote types."""
        cmd = AsyncCommand.wsl('echo "hello" \'world\' "test"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello", result.stdout.strip())
        self.assertIn("world", result.stdout.strip())
        self.assertIn("test", result.stdout.strip())

    def test_echo_with_front_slashes(self):
        """Test echo with front slashes."""
        cmd = AsyncCommand.wsl("echo /path/to/file")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("/path/to/file", result.stdout.strip())

    def test_echo_with_back_slashes(self):
        """Test echo with back slashes."""
        cmd = AsyncCommand.wsl("echo 'C:\\\\Users\\\\Test\\\\file.txt'")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("C:\\Users\\Test\\file.txt", result.stdout.strip())

    def test_echo_with_path_and_spaces(self):
        """Test echo with path containing spaces."""
        cmd = AsyncCommand.wsl('echo "/home/user/Test App/file.txt"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("/home/user/Test App/file.txt", result.stdout.strip())

    def test_echo_with_piping(self):
        """Test echo with piping."""
        cmd = AsyncCommand.wsl("echo hello | grep hello")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello", result.stdout.strip())

    def test_echo_with_output_redirection(self):
        """Test echo with output redirection."""
        cmd = AsyncCommand.wsl("echo test > output.txt")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        # Check if file was created
        self.assertTrue(os.path.exists("output.txt"))
        # Clean up
        if os.path.exists("output.txt"):
            os.remove("output.txt")

    def test_echo_with_input_redirection(self):
        """Test echo with input redirection."""
        # Create a test file first
        with open("input.txt", "w") as f:
            f.write("test input")

        cmd = AsyncCommand.wsl("cat input.txt")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test input", result.stdout.strip())

        # Clean up
        if os.path.exists("input.txt"):
            os.remove("input.txt")

    def test_complex_combination(self):
        """Test complex combination of quotes, paths, and redirection."""
        cmd = AsyncCommand.wsl('echo "/home/user/Test" > output.txt && cat output.txt')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("/home/user/Test", result.stdout.strip())

        # Clean up
        if os.path.exists("output.txt"):
            os.remove("output.txt")

    def test_unicode_characters(self):
        """Test echo with unicode characters."""
        cmd = AsyncCommand.wsl("echo 你好世界")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("你好世界", result.stdout.strip())

    def test_special_characters(self):
        """Test echo with special characters."""
        cmd = AsyncCommand.wsl('echo "Special chars: !@#$%^&*()_+-=[]{}|;:,.<>?"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("Special chars", result.stdout.strip())

    def test_multiple_commands(self):
        """Test multiple commands with &&."""
        cmd = AsyncCommand.wsl("echo hello && echo world")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello", result.stdout.strip())
        self.assertIn("world", result.stdout.strip())

    def test_empty_string(self):
        """Test wsl factory with empty string."""
        cmd = AsyncCommand.wsl("")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")

    def test_whitespace_stripping(self):
        """Test wsl factory strips leading/trailing whitespace."""
        cmd = AsyncCommand.wsl("  echo test  ")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test", result.stdout.strip())

    def test_environment_variables(self):
        """Test wsl factory with environment variables."""
        cmd = AsyncCommand.wsl("echo $HOME")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("/home", result.stdout.strip())

    def test_linux_commands(self):
        """Test wsl factory with typical Linux commands."""
        cmd = AsyncCommand.wsl("pwd")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        # Should return current working directory

