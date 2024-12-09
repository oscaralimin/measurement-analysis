import logging
from pathlib import Path
from typing import Dict, List
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

from .plotter import ChannelPlotter

class ReportGenerator:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        self.plotter = ChannelPlotter()

    def generate_report(self, results: Dict, mf4_file: Path, 
                       channels: Dict, configs: Dict) -> None:
        output_file = self.output_dir / f"{mf4_file.stem}_report.pdf"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        with PdfPages(output_file) as pdf:
            # Add summary page
            self._add_summary_page(pdf, results, mf4_file)
            
            # Add individual channel plots
            for channel_name, result in results.items():
                try:
                    fig = self.plotter.create_plot(
                        channel_name,
                        channels[channel_name].data,
                        channels[channel_name].timestamps,
                        configs[channel_name],
                        result.violations
                    )
                    pdf.savefig(fig)
                    plt.close(fig)
                except Exception as e:
                    self.logger.error(
                        f"Failed to create plot for {channel_name}: {str(e)}")

    def _add_summary_page(self, pdf: PdfPages, results: Dict, 
                         mf4_file: Path) -> None:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('off')
        
        # Calculate statistics
        total = len(results)
        passed = sum(1 for r in results.values() if r.passed)
        
        # Create summary text
        summary = [
            f"Analysis Report: {mf4_file.name}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Channels: {total}",
            f"Passed: {passed}",
            f"Failed: {total - passed}",
        ]
        
        ax.text(0.5, 0.5, '\n'.join(summary), 
                ha='center', va='center', fontsize=12)
        
        pdf.savefig(fig)
        plt.close(fig)