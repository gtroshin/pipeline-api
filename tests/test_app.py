import unittest
import json
from app import create_app
from app.config import API_KEY


class PipelineTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }

    def test_create_pipeline(self):
        data = {
            "stages": [
                {"type": "run", "command": "echo 'Running tests'"},
                {"type": "build", "dockerfile": "Dockerfile"},
                {"type": "deploy", "manifest": "k8s/deployment.yaml"},
            ]
        }
        response = self.client.post(
            "/pipelines", headers=self.headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_create_pipeline_invalid_json(self):
        response = self.client.post(
            "/pipelines", headers=self.headers, data="invalid json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, expected JSON", response.json["error"])


def test_create_pipeline_missing_stages(self):
    data = {}
    response = self.client.post(
        "/pipelines", headers=self.headers, data=json.dumps(data)
    )
    self.assertEqual(response.status_code, 400)
    self.assertIn(
        "Invalid pipeline configuration, 'stages' must be a list",
        response.json["error"],
    )

    def test_create_pipeline_invalid_command_type(self):
        data = {"stages": [{"type": "invalid", "command": "echo 'Running tests'"}]}
        response = self.client.post(
            "/pipelines", headers=self.headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid command type: invalid", response.json["error"])

    def test_create_pipeline_missing_required_fields(self):
        data = {"stages": [{"type": "run"}]}
        response = self.client.post(
            "/pipelines", headers=self.headers, data=json.dumps(data)
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing 'command' for RUN stage", response.json["error"])

    def test_get_pipeline(self):
        # First, create a pipeline
        data = {
            "stages": [
                {"type": "run", "command": "echo 'Running tests'"},
                {"type": "build", "dockerfile": "Dockerfile"},
                {"type": "deploy", "manifest": "k8s/deployment.yaml"},
            ]
        }
        create_response = self.client.post(
            "/pipelines", headers=self.headers, data=json.dumps(data)
        )
        pipeline_id = create_response.json["id"]

        # Now, get the pipeline
        response = self.client.get(f"/pipelines/{pipeline_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["stages"], data["stages"])

    def test_get_non_existent_pipeline(self):
        response = self.client.get("/pipelines/999", headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Pipeline not found", response.json["error"])

    def test_update_pipeline(self):
        # First, create a pipeline
        data = {
            "stages": [
                {"type": "run", "command": "echo 'Running tests'"},
                {"type": "build", "dockerfile": "Dockerfile"},
                {"type": "deploy", "manifest": "k8s/deployment.yaml"},
            ]
        }
        create_response = self.client.post(
            "/pipelines", headers=self.headers, data=json.dumps(data)
        )
        pipeline_id = create_response.json["id"]

        # Now, update the pipeline
        updated_data = {
            "stages": [
                {"type": "run", "command": "echo 'Running updated tests'"},
                {"type": "build", "dockerfile": "UpdatedDockerfile"},
                {"type": "deploy", "manifest": "k8s/updated_deployment.yaml"},
            ]
        }
        response = self.client.put(
            f"/pipelines/{pipeline_id}",
            headers=self.headers,
            data=json.dumps(updated_data),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Pipeline updated")

    def test_update_non_existent_pipeline(self):
        updated_data = {
            "stages": [
                {"type": "run", "command": "echo 'Running updated tests'"},
                {"type": "build", "dockerfile": "UpdatedDockerfile"},
                {"type": "deploy", "manifest": "k8s/updated_deployment.yaml"},
            ]
        }
        response = self.client.put(
            "/pipelines/999",
            headers=self.headers,
            data=json.dumps(updated_data),
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Pipeline not found", response.json["error"])

    def test_delete_pipeline(self):
        # First, create a pipeline
        data = {
            "stages": [
                {"type": "run", "command": "echo 'Running tests'"},
                {"type": "build", "dockerfile": "Dockerfile"},
                {"type": "deploy", "manifest": "k8s/deployment.yaml"},
            ]
        }
        create_response = self.client.post(
            "/pipelines", headers=self.headers, data=json.dumps(data)
        )
        pipeline_id = create_response.json["id"]

        # Now, delete the pipeline
        response = self.client.delete(f"/pipelines/{pipeline_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Pipeline deleted")

    def test_delete_non_existent_pipeline(self):
        response = self.client.delete("/pipelines/999", headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Pipeline not found", response.json["error"])

    def test_trigger_pipeline(self):
        # First, create a pipeline
        data = {
            "stages": [
                {"type": "run", "command": "echo 'Running tests'"},
                {"type": "build", "dockerfile": "Dockerfile"},
                {"type": "deploy", "manifest": "k8s/deployment.yaml"},
            ]
        }
        create_response = self.client.post(
            "/pipelines", headers=self.headers, data=json.dumps(data)
        )
        pipeline_id = create_response.json["id"]

        # Now, trigger the pipeline
        response = self.client.post(
            f"/pipelines/{pipeline_id}/trigger", headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Pipeline triggered")

    def test_trigger_non_existent_pipeline(self):
        response = self.client.post("/pipelines/999/trigger", headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Pipeline not found", response.json["error"])


if __name__ == "__main__":
    unittest.main()
