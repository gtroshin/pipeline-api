import unittest
from unittest.mock import patch, Mock
import click
from click.testing import CliRunner
from cli.cli import cli


class CLITestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.api_key = "test_api_key"

    @patch("cli.cli.requests.get")
    def test_get_pipeline(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Pipeline not found"}
        mock_get.return_value = mock_response

        result = self.runner.invoke(
            cli, ["get-pipeline", "1", "--api-key", self.api_key]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Pipeline not found", result.output)

    @patch("cli.cli.requests.post")
    def test_create_pipeline(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 1}
        mock_post.return_value = mock_response

        pipeline_data = '{"stages": [{"type": "run", "command": "echo \\"Running tests\\""}, {"type": "build", "dockerfile": "Dockerfile"}, {"type": "deploy", "manifest": "k8s/deployment.yaml"}]}'
        result = self.runner.invoke(
            cli, ["create-pipeline", pipeline_data, "--api-key", self.api_key]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("id", result.output)

    @patch("cli.cli.requests.put")
    def test_update_pipeline(self, mock_put):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Pipeline updated"}
        mock_put.return_value = mock_response

        pipeline_data = '{"stages": [{"type": "run", "command": "echo \\"Running updated tests\\""}, {"type": "build", "dockerfile": "UpdatedDockerfile"}, {"type": "deploy", "manifest": "k8s/updated_deployment.yaml"}]}'
        result = self.runner.invoke(
            cli, ["update-pipeline", "1", pipeline_data, "--api-key", self.api_key]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Pipeline updated", result.output)

    @patch("cli.cli.requests.delete")
    def test_delete_pipeline(self, mock_delete):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Pipeline deleted"}
        mock_delete.return_value = mock_response

        result = self.runner.invoke(
            cli, ["delete-pipeline", "1", "--api-key", self.api_key]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Pipeline deleted", result.output)

    @patch("cli.cli.requests.post")
    def test_trigger_pipeline(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Pipeline triggered"}
        mock_post.return_value = mock_response

        result = self.runner.invoke(
            cli, ["trigger-pipeline", "1", "--api-key", self.api_key]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Pipeline triggered", result.output)

    @patch("cli.cli.requests.post")
    def test_create_pipeline_invalid_json(self, mock_post):
        result = self.runner.invoke(
            cli, ["create-pipeline", "invalid json", "--api-key", self.api_key]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Error: Invalid JSON format.", result.output)
        mock_post.assert_not_called()

    @patch("cli.cli.requests.put")
    def test_update_pipeline_invalid_json(self, mock_put):
        result = self.runner.invoke(
            cli, ["update-pipeline", "1", "invalid json", "--api-key", self.api_key]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Error: Invalid JSON format.", result.output)
        mock_put.assert_not_called()

    @patch(
        "cli.cli.get_headers", side_effect=click.ClickException("API key is required")
    )
    def test_get_pipeline_missing_api_key(self, mock_get_headers):
        result = self.runner.invoke(cli, ["get-pipeline", "1"])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("API key is required", result.output)
        mock_get_headers.assert_called_once()

    @patch("cli.cli.requests.post")
    def test_create_pipeline_400(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Invalid input"}
        mock_post.return_value = mock_response

        pipeline_data = '{"stages": [{"type": "run", "command": "echo \\"Running tests\\""}, {"type": "build", "dockerfile": "Dockerfile"}, {"type": "deploy", "manifest": "k8s/deployment.yaml"}]}'
        result = self.runner.invoke(
            cli, ["create-pipeline", pipeline_data, "--api-key", self.api_key]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Error: Invalid input", result.output)

    @patch("cli.cli.requests.post")
    def test_create_pipeline_403(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"error": "Forbidden"}
        mock_post.return_value = mock_response

        pipeline_data = '{"stages": [{"type": "run", "command": "echo \\"Running tests\\""}, {"type": "build", "dockerfile": "Dockerfile"}, {"type": "deploy", "manifest": "k8s/deployment.yaml"}]}'
        result = self.runner.invoke(
            cli, ["create-pipeline", pipeline_data, "--api-key", self.api_key]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "Forbidden: You don't have permission to access this resource.",
            result.output,
        )

    @patch("cli.cli.requests.post")
    def test_create_pipeline_500(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        pipeline_data = '{"stages": [{"type": "run", "command": "echo \\"Running tests\\""}, {"type": "build", "dockerfile": "Dockerfile"}, {"type": "deploy", "manifest": "k8s/deployment.yaml"}]}'
        result = self.runner.invoke(
            cli, ["create-pipeline", pipeline_data, "--api-key", self.api_key]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Error: 500 - Internal Server Error", result.output)


if __name__ == "__main__":
    unittest.main()
