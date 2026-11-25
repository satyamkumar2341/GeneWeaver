
from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical
from textual.widgets import Footer, Header, Static

from geneweaver.system_info import get_gpu_info, get_system_metrics


class GeneWeaverDashboard(App):
    TITLE = "GENEWEAVER | CRISPR ALIGNMENT ENGINE"
    SUB_TITLE = "Bioinformatics & High Performance Computing"

    CSS = """
    Screen {
        background: #101722;
    }

    #banner {
        height: 3;
        content-align: center middle;
        background: #17334a;
        color: white;
        text-style: bold;
        border: round #39b8d4;
    }

    #main-grid {
        grid-size: 2 2;
        grid-columns: 1fr 1fr;
        grid-rows: 1fr 1fr;
        height: 1fr;
        margin: 1 2;
        grid-gutter: 1 2;
    }

    .panel {
        border: round #39b8d4;
        padding: 1 2;
        background: #172331;
        color: white;
    }

    .panel-title {
        color: #42d9e8;
        text-style: bold;
        margin-bottom: 1;
    }

    #status {
        color: #8de7a6;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        yield Static(
            "GENEWEAVER | CRISPR ALIGNMENT & OFF-TARGET ANALYSIS",
            id="banner",
        )

        with Grid(id="main-grid"):
            with Vertical(classes="panel"):
                yield Static("SYSTEM MONITOR", classes="panel-title")
                yield Static("Loading...", id="system")

            with Vertical(classes="panel"):
                yield Static("GPU DETECTION", classes="panel-title")
                yield Static("Detecting...", id="gpu")

            with Vertical(classes="panel"):
                yield Static("ALIGNMENT ENGINE", classes="panel-title")
                yield Static(
                    "CPU backend: Planned\n"
                    "Intel GPU backend: Under evaluation\n"
                    "NVIDIA CUDA: Optional",
                    id="engine",
                )

            with Vertical(classes="panel"):
                yield Static("PROJECT STATUS", classes="panel-title")
                yield Static(
                    "FASTA parser: Pending\n"
                    "Sequence alignment: Pending\n"
                    "Off-target scoring: Pending\n"
                    "Benchmarking: Pending",
                    id="status",
                )

        yield Footer()

    def on_mount(self) -> None:
        self.refresh_metrics()
        self.set_interval(2, self.refresh_metrics)

    def refresh_metrics(self) -> None:
        metrics = get_system_metrics()

        self.query_one("#system", Static).update(
            f"CPU Usage: {metrics['cpu_percent']:.1f}%\n"
            f"RAM Usage: {metrics['memory_percent']:.1f}%\n"
            f"RAM Used: {metrics['memory_used_gb']:.2f} GB\n"
            f"RAM Total: {metrics['memory_total_gb']:.2f} GB\n"
            f"Processor: {metrics['processor']}"
        )

        gpu_text = "\n".join(get_gpu_info())

        self.query_one("#gpu", Static).update(gpu_text)


if __name__ == "__main__":
    GeneWeaverDashboard().run()
