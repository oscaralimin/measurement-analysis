# Standard library imports
import logging
import sys
from pathlib import Path
from tkinter import filedialog

# Import our custom modules
from core.analyzer import MeasurementAnalyzer
from data.file_handler import FileHandler
from visualization.report import ReportGenerator

def main():
    """Main entry point for the analysis system."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    try:
        # Get configuration file
        config_file = Path("config.xlsx")
        if not config_file.exists():
            config_file = Path(filedialog.askopenfilename(
                filetypes=[("Excel files", "*.xlsx")],
                title="Select configuration file"
            ))

        # Initialize system components
        analyzer = MeasurementAnalyzer(config_file)
        file_handler = FileHandler()
        report_generator = ReportGenerator(Path("reports"))

        # Get MF4 files to analyze
        mf4_files = list(Path("data").glob("*.mf4"))
        if not mf4_files:
            file_path = filedialog.askopenfilename(
                filetypes=[("MF4 files", "*.mf4")],
                title="Select MF4 file"
            )
            mf4_files = [Path(file_path)]

        # Process each file
        for mf4_file in mf4_files:
            logger.info(f"Processing {mf4_file}")
            try:
                # Run analysis
                results = analyzer.analyze_file(mf4_file)
                
                # Generate report
                report_generator.generate_report(
                    results,
                    mf4_file,
                    analyzer.channels,
                    analyzer.config
                )
                
                # Print summary
                passed = sum(1 for r in results.values() if r.passed)
                total = len(results)
                print(f"\nResults for {mf4_file.name}:")
                print(f"Passed: {passed}/{total} channels")
                
            except Exception as e:
                logger.error(f"Failed to process {mf4_file}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Analysis system error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("hello world")