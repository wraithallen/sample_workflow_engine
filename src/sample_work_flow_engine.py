from signal import signal, SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM
import sys

def signal_handler(signal, frame):
    print 'catch signal ' + str(signal)
    sys.exit(0)
    
for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, signal_handler)

def main():
    import logutil
    logger = logutil.get_logger(__name__)

    try:
        import configutil
        configutil.initialize('env_sample_work_flow.cfg')
        import to_do_queue
        to_do_queue.initiliaze()
        
        TaskAll = {
            'tasks' : [
                {"cmd":"ls"},
                {"cmd":"whereis python"},
                {"cmd":"whereis vim"}
            ]
        }
        
        result_queue_name, result_num = to_do_queue.add_TaskAll(TaskAll)
        to_do_queue.watch_result(result_queue_name, result_num)

        import sqs
        sqs.clean_all()
        
    except (SystemExit, KeyboardInterrupt):
        pass
    except Exception:
        logger.exception("launch service failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
