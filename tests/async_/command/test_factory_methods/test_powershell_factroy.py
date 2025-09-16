import os

from danielutils.async_.async_command import AsyncCommand
from ..base import BaseCommandTest


class TestPowerShellFactory(BaseCommandTest):
    """Test cases for AsyncCommand.powershell factory method."""

    def test_echo_one_word_unquoted(self):
        """Test echo with one word unquoted."""
        cmd = AsyncCommand.powershell("Write-Host test")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test", result.stdout.strip())

    def test_echo_two_words_unquoted(self):
        """Test echo with two words unquoted."""
        cmd = AsyncCommand.powershell("Write-Host hello world")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello world", result.stdout.strip())

    def test_echo_sentence_unquoted(self):
        """Test echo with sentence unquoted."""
        cmd = AsyncCommand.powershell("Write-Host this is a test sentence")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("this is a test sentence", result.stdout.strip())

    def test_echo_one_word_double_quoted(self):
        """Test echo with one word double quoted."""
        cmd = AsyncCommand.powershell('Write-Host "test"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test", result.stdout.strip())

    def test_echo_two_words_double_quoted(self):
        """Test echo with two words double quoted."""
        cmd = AsyncCommand.powershell('Write-Host "hello world"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello world", result.stdout.strip())

    def test_echo_sentence_double_quoted(self):
        """Test echo with sentence double quoted."""
        cmd = AsyncCommand.powershell('Write-Host "this is a test sentence"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("this is a test sentence", result.stdout.strip())

    def test_echo_one_word_single_quoted(self):
        """Test echo with one word single quoted."""
        cmd = AsyncCommand.powershell("Write-Host 'test'")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test", result.stdout.strip())

    def test_echo_two_words_single_quoted(self):
        """Test echo with two words single quoted."""
        cmd = AsyncCommand.powershell("Write-Host 'hello world'")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello world", result.stdout.strip())

    def test_echo_sentence_single_quoted(self):
        """Test echo with sentence single quoted."""
        cmd = AsyncCommand.powershell("Write-Host 'this is a test sentence'")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("this is a test sentence", result.stdout.strip())

    def test_echo_multiple_quotes(self):
        """Test echo with multiple quotes."""
        cmd = AsyncCommand.powershell('Write-Host "hello" "world" "test"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello", result.stdout.strip())
        self.assertIn("world", result.stdout.strip())
        self.assertIn("test", result.stdout.strip())

    def test_echo_mixed_quote_types(self):
        """Test echo with mixed quote types."""
        cmd = AsyncCommand.powershell('Write-Host "hello" \'world\' "test"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello", result.stdout.strip())
        self.assertIn("world", result.stdout.strip())
        self.assertIn("test", result.stdout.strip())

    def test_echo_with_front_slashes(self):
        """Test echo with front slashes."""
        cmd = AsyncCommand.powershell("Write-Host /path/to/file")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("/path/to/file", result.stdout.strip())

    def test_echo_with_back_slashes(self):
        """Test echo with back slashes."""
        cmd = AsyncCommand.powershell("Write-Host C:\\Users\\Test\\file.txt")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("C:\\Users\\Test\\file.txt", result.stdout.strip())

    def test_echo_with_path_and_spaces(self):
        """Test echo with path containing spaces."""
        cmd = AsyncCommand.powershell('Write-Host "C:\\Program Files\\Test App\\file.txt"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("C:\\Program Files\\Test App\\file.txt", result.stdout.strip())

    def test_echo_with_piping(self):
        """Test echo with piping."""
        cmd = AsyncCommand.powershell("Write-Host hello | Select-String hello")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello", result.stdout.strip())

    def test_echo_with_output_redirection(self):
        """Test echo with output redirection."""
        cmd = AsyncCommand.powershell("Write-Host test | Out-File -FilePath output.txt")
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

        cmd = AsyncCommand.powershell("Get-Content input.txt")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test input", result.stdout.strip())

        # Clean up
        if os.path.exists("input.txt"):
            os.remove("input.txt")

    def test_complex_combination(self):
        """Test complex combination of quotes, paths, and redirection."""
        cmd = AsyncCommand.powershell(
            'Write-Host "C:\\Program Files\\Test" | Out-File -FilePath output.txt; Get-Content output.txt')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("C:\\Program Files\\Test", result.stdout.strip())

        # Clean up
        if os.path.exists("output.txt"):
            os.remove("output.txt")

    def test_unicode_characters(self):
        """Test echo with unicode characters."""
        cmd = AsyncCommand.powershell("Write-Host 你好世界")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("你好世界", result.stdout.strip())

    def test_special_characters(self):
        """Test echo with special characters."""
        cmd = AsyncCommand.powershell('Write-Host "Special chars: !@#$%^&*()_+-=[]{}|;:,.<>?"')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("Special chars", result.stdout.strip())

    def test_multiple_commands(self):
        """Test multiple commands with semicolon."""
        cmd = AsyncCommand.powershell("Write-Host hello; Write-Host world")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("hello", result.stdout.strip())
        self.assertIn("world", result.stdout.strip())

    def test_empty_string(self):
        """Test powershell factory with empty string."""
        cmd = AsyncCommand.powershell("")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")

    def test_whitespace_stripping(self):
        """Test powershell factory strips leading/trailing whitespace."""
        cmd = AsyncCommand.powershell("  Write-Host test  ")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test", result.stdout.strip())

    def test_environment_variables(self):
        """Test powershell factory with environment variables."""
        cmd = AsyncCommand.powershell("Write-Host $env:USERNAME")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn(os.getenv("USERNAME", ""), result.stdout.strip())

    def test_powershell_variables(self):
        """Test powershell factory with PowerShell variables."""
        cmd = AsyncCommand.powershell("$var = 'test'; Write-Host $var")
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("test", result.stdout.strip())

    def test_escaped_quotes(self):
        """Test powershell factory with escaped quotes."""
        cmd = AsyncCommand.powershell('Write-Host "He said \"Hello World\""')
        result = self.run_async(cmd.execute())
        self.assertTrue(result.success, f"Command failed with stderr: {result.stderr}")
        self.assertIn("He said", result.stdout.strip())
        self.assertIn("Hello World", result.stdout.strip())
