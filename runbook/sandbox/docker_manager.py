from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
import docker
from docker.errors import NotFound

@dataclass
class ExecResult:
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False

class SandboxManager:
    def __init__(self, image: str):
        self._client = docker.from_env()
        self._image = image

    def create_session(self, repo_url: str, auth_token: str | None = None) -> str:
        container = self._client.containers.run(self._image, detach=True, working_dir="/workspace")
        clone_url = repo_url
        if auth_token:
            clone_url = repo_url.replace("https://", f"https://{auth_token}@")

        clone_result = self.exec(container.id, ["git", "clone", clone_url, "."])
        if clone_result.exit_code != 0:
            container.stop()
            container.remove()
            raise RuntimeError(f"git clone failed: {clone_result.stderr}")

        return container.id

    def exec(self, container_id: str, command: list[str], timeout: int = 60) -> ExecResult:
        container = self._client.containers.get(container_id)
        exec_id = container.client.api.exec_create(container.id, command, workdir="/workspace")["Id"]

        def run():
            output = container.client.api.exec_start(exec_id, stream=False)
            exit_info = container.client.api.exec_inspect(exec_id)
            return output, exit_info

        pool = ThreadPoolExecutor(max_workers=1)
        future = pool.submit(run)
        try:
            output, exit_info = future.result(timeout=timeout)
        except FutureTimeoutError:
            pool.shutdown(wait=False)
            return ExecResult(exit_code=-1, stdout="", stderr="command timed out", timed_out=True)
        pool.shutdown(wait=False)

        stdout = output.decode("utf-8", errors="replace") if isinstance(output, bytes) else str(output)
        return ExecResult(exit_code=exit_info["ExitCode"] or 0, stdout=stdout, stderr="", timed_out=False)

    def read_file(self, container_id: str, path: str) -> str:
        result = self.exec(container_id, ["cat", path])
        if result.exit_code != 0:
            raise FileNotFoundError(f"{path} not found in container {container_id}")
        return result.stdout

    def destroy(self, container_id: str) -> None:
        try:
            container = self._client.containers.get(container_id)
            container.stop(timeout=5)
            container.remove()
        except NotFound:
            pass
