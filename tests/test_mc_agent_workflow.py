"""Offline checks for the mention detector's token and read-only behavior."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

import yaml


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/mc-agent.yml"
NODE = shutil.which("node")
HARNESS = r"""
const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const outputs = {}, calls = [];
const read = (name, value) => async (args) => {
    calls.push({name, args});
    return {data: value};
};
const github = {rest: {
    issues: {
        get: read('issues.get', {body: ''}),
        listComments: read('issues.listComments', input.comments || []),
    },
    pulls: {get: read('pulls.get', {body: ''})},
}};
const mockRequire = (name) => {
    if (name !== 'fs') throw new Error(`Unexpected module: ${name}`);
    return {readFileSync: () => JSON.stringify(['controller'])};
};
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
const detect = new AsyncFunction('require', 'github', 'context', 'core', 'console', input.script);
detect(mockRequire, github, input.context, {setOutput: (key, value) => outputs[key] = value},
       {log: () => {}}).then(() => process.stdout.write(JSON.stringify({outputs, calls})))
    .catch(error => {console.error(error); process.exitCode = 1;});
"""


class MentionDetectionWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.job = yaml.safe_load(WORKFLOW.read_text())["jobs"]["check-mention"]
        cls.detect = next(step for step in cls.job["steps"] if step.get("id") == "detect")

    def test_detection_does_not_require_a_repository_secret(self):
        self.assertEqual(self.detect["with"]["github-token"], "${{ github.token }}")
        self.assertNotIn("secrets.", json.dumps(self.job))
        self.assertEqual(self.job["permissions"], {
            "contents": "read", "issues": "read", "pull-requests": "read",
        })

    def run_detection(self, context, comments=None):
        if NODE is None:
            self.skipTest("Node.js is needed to exercise the workflow's JavaScript")
        context["repo"] = {"owner": "example", "repo": "model-cards"}
        result = subprocess.run(
            [NODE, "-e", HARNESS],
            input=json.dumps({"script": self.detect["with"]["script"],
                              "context": context, "comments": comments or []}),
            text=True, capture_output=True, check=True, timeout=10,
        )
        return json.loads(result.stdout)

    def test_pull_request_detection_preserves_authorization_without_api_writes(self):
        for body, login, expected in (
            ("Documentation correction", "controller", False),
            ("@mcassistant inspect the card", "visitor", False),
            ("@mcassistant inspect the card", "controller", True),
        ):
            with self.subTest(body=body, login=login):
                result = self.run_detection({
                    "eventName": "pull_request",
                    "payload": {"pull_request": {
                        "body": body, "user": {"login": login}, "number": 42,
                    }},
                })
                self.assertEqual(result["outputs"]["qualified-mention"], expected)
                self.assertEqual(result["outputs"]["prompt"], "inspect the card" if expected else "")
                self.assertEqual(result["calls"], [])

    def test_manual_issue_and_pr_detection_need_only_read_endpoints(self):
        for item_type, endpoint in (("issue", "issues.get"), ("pull_request", "pulls.get")):
            with self.subTest(item_type=item_type):
                result = self.run_detection({
                    "eventName": "workflow_dispatch", "actor": "controller",
                    "payload": {"inputs": {"item-type": item_type, "item-number": "42"}},
                }, comments=[{"body": "@mcassistant inspect the card"}])
                self.assertTrue(result["outputs"]["qualified-mention"])
                self.assertEqual(result["outputs"]["item-type"], item_type)
                self.assertEqual(result["outputs"]["item-number"], 42)
                self.assertEqual([call["name"] for call in result["calls"]],
                                 [endpoint, "issues.listComments"])


if __name__ == "__main__":
    unittest.main()
