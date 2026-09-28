import subprocess
import logging

logging.basicConfig(
    filename="pipelines/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def run_pipeline():
    print("Apex Manufacturing Data Pipeline")
    print("---------------------------------")
    print("Pipeline started")
    logger.info("Pipeline started")

    print("\nRunning data validation...")
    subprocess.run(["python", "pipelines/validate_data.py"], check=True)
    logger.info("Data validation completed successfully")

    print("\nLoading data into PostgreSQL...")
    subprocess.run(["python", "pipelines/load_data.py"], check=True)
    logger.info("Data loading completed successfully")

    print("\nPipeline completed successfully.")
    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()