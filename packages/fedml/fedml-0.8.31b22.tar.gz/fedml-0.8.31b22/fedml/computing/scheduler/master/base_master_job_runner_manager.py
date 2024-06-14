
import json
import logging
import os
import time
from abc import ABC
from multiprocessing import Process
from .cloud_server_manager import FedMLCloudServerManager
from ..comm_utils.run_process_utils import RunProcessUtils
from ..scheduler_core.scheduler_base_job_runner_manager import FedMLSchedulerBaseJobRunnerManager
from ..scheduler_core.account_manager import FedMLAccountManager


class FedMLBaseMasterJobRunnerManager(FedMLSchedulerBaseJobRunnerManager, ABC):
    def __init__(self):
        FedMLSchedulerBaseJobRunnerManager.__init__(self)
        self.master_server_map = dict()

    # Override
    def start_job_runner(
            self, run_id, request_json, args=None, edge_id=None, is_server_job=False,
            sender_message_queue=None, listener_message_queue=None, status_center_queue=None,
            communication_manager=None, master_server_instance=None, should_start_cloud_server=False,
            use_local_process_as_cloud_server=False, cuda_visible_gpu_ids_str=None
    ):
        if should_start_cloud_server:
            self._start_cloud_server(
                args, run_id, request_json, edge_id=edge_id,
                use_local_process_as_cloud_server=use_local_process_as_cloud_server,
                sender_message_queue=sender_message_queue, listener_message_queue=listener_message_queue,
                status_center_queue=status_center_queue, communication_manager=communication_manager,
                master_server_instance=master_server_instance)
            return

        run_id_str = str(run_id)
        self.job_runners[run_id_str] = self._generate_job_runner_instance(
            args, run_id=run_id, request_json=request_json,
            agent_config=args.agent_config, edge_id=edge_id,
        )
        self.job_runners[run_id_str].start_runner_process(
            run_id, request_json, edge_id=edge_id, is_server_job=is_server_job,
            sender_message_queue=sender_message_queue,
            listener_message_queue=listener_message_queue,
            status_center_queue=status_center_queue
        )

    def stop_job_runner(
            self, run_id, args=None, server_id=None, request_json=None,
            run_as_cloud_agent=False, run_as_cloud_server=False,
            use_local_process_as_cloud_server=False
    ):
        super().stop_job_runner(run_id)

        if run_as_cloud_agent or run_as_cloud_server:
            stopping_process = Process(
                target=FedMLCloudServerManager.stop_cloud_server,
                args=(run_id, server_id, args.agent_config))
            stopping_process.start()

            if self.master_server_map.get(str(run_id), None) is not None:
                self.master_server_map.pop(str(run_id))

            if run_as_cloud_server:
                time.sleep(1)
                RunProcessUtils.kill_process(os.getpid())

    def complete_job_runner(
            self, run_id, args=None, server_id=None, request_json=None,
            run_as_cloud_agent=False, run_as_cloud_server=False,
            use_local_process_as_cloud_server=False
    ):
        super().complete_job_runner(run_id)

        if run_as_cloud_agent or run_as_cloud_server:
            stopping_process = Process(
                target=FedMLCloudServerManager.stop_cloud_server,
                args=(run_id, server_id, args.agent_config))
            stopping_process.start()

            if self.master_server_map.get(str(run_id), None) is not None:
                self.master_server_map.pop(str(run_id))

            if run_as_cloud_server:
                time.sleep(1)
                RunProcessUtils.kill_process(os.getpid())

    def _start_cloud_server(
            self, args, run_id, request_json, edge_id=None,
            use_local_process_as_cloud_server=False,
            sender_message_queue=None, listener_message_queue=None,
            status_center_queue=None, communication_manager=None,
            master_server_instance=None
    ):
        run_id_str = str(run_id)
        cloud_server_mgr = FedMLCloudServerManager(
            args, run_id=run_id, edge_id=edge_id, request_json=request_json,
            agent_config=args.agent_config
        )
        if not use_local_process_as_cloud_server:
            self.cloud_run_process_map[run_id_str] = Process(target=cloud_server_mgr.start_cloud_server_process_entry)
            self.cloud_run_process_map[run_id_str].start()
        else:
            cloud_device_id = request_json.get("cloudServerDeviceId", "0")
            payload = json.dumps(request_json)

            logging.info("start the master server: {}".format(payload))

            self.start_local_master_server(
                args.account_id, args.api_key, args.os_name, args.version,
                cloud_device_id, run_id, payload,
                communication_manager=communication_manager,
                sender_message_queue=sender_message_queue,
                status_center_queue=status_center_queue,
                master_server_instance=master_server_instance)
            time.sleep(1)

    def start_local_master_server(
            self, user, api_key, os_name, version, cloud_device_id, run_id, payload,
            communication_manager=None, sender_message_queue=None, status_center_queue=None,
            master_server_instance=None
    ):
        if master_server_instance is None:
            return
        master_server_instance.login(
            user, api_key=api_key, device_id=cloud_device_id, os_name=os_name,
            role=FedMLAccountManager.ROLE_CLOUD_SERVER,
            communication_manager=communication_manager,
            sender_message_queue=sender_message_queue,
            status_center_queue=status_center_queue)
        master_server_instance.start_master_server_instance(payload)
        self.master_server_map[str(run_id)] = master_server_instance

    def callback_run_logs(self, run_id, topic, payload):
        run_id_str = str(run_id)
        if self.job_runners.get(run_id_str, None) is not None:
            self.job_runners[run_id_str].callback_run_logs(topic, payload)

    def callback_run_metrics(self, run_id, topic, payload):
        run_id_str = str(run_id)
        if self.job_runners.get(run_id_str, None) is not None:
            self.job_runners[run_id_str].callback_run_metrics(topic, payload)
