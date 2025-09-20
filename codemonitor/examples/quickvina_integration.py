from codemonitor import Monitor
import time

def workload():
    time.sleep(5)

def main():
    with Monitor(sample_interval=1.0,
                 sinks=["csv","jsonl"],
                 out_dir="data/sysstats",
                 gpu=True).running() as mon:
        mon.mark("warmup_done")
        workload()
        mon.mark("batch_loop_start", extra={"n_ligands": 30})
        workload()
        mon.mark("sync_back_start")
        workload()
        mon.mark("sync_back_done")

if __name__ == "__main__":
    main()
