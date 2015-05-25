import sys
def main():
    import logutil
    logger = logutil.get_logger(__name__)

    try:
        import configutil
        configutil.initialize('env_sample_work_flow.cfg')
        
        from gevent import monkey
        monkey.patch_all()

        import worker
        worker.get_task_work()
    except (SystemExit, KeyboardInterrupt):
        pass
    except Exception:
        logger.exception("launch service failed")
        sys.exit(1)

if __name__ == "__main__":
    main()