from etl.core_modules.quality_checker import QualityChecker
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--source_path", required=True)
    parser.add_argument("--target_path", required=True)
    parser.add_argument("--audit_type", required=True)
    parser.add_argument("--source_column", required=True)
    parser.add_argument("--target_column", required=True)
    parser.add_argument("--accepted_accuracy", required=True)
    parser.add_argument("--sns_topic_arn", required=True)

    args = parser.parse_args()
    args_dict = vars(args)

    job = QualityChecker(args_dict)
    job.run()


    

