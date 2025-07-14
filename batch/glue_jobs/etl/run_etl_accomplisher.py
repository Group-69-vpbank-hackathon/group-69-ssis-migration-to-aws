from etl.core_modules.accomplisher import Accomplisher
from etl.utils.data_writer_factory import create_writer
import argparse

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("--ssm_parameter_name", required=True)
    parser.add_argument("--lookback", type=int, default=0)
    parser.add_argument("--rolling_window", type=int, default=0)
    parser.add_argument("--granularity", default="daily")
    parser.add_argument("--start_date", required=True)
    parser.add_argument("--end_date", required=True)
    parser.add_argument("--date_format", default=None)

    args, unknown = parser.parse_known_args()
    args_dict = vars(args)
    data_writer = create_writer(args=args_dict)
    
    job = Accomplisher(args_dict, data_writer)
    job.run()
