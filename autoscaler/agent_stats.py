import logging


class AgentStats:
    def __init__(self, api_client):
        self.api_client = api_client
        self.stats = {}
        self.log = logging.getLogger("autoscale")

    def reset(self):
        """ Drop all cached statistics.
        """
        self.stats = {}

    def get_task_stats(self, agent, task, n=0):
        """ Get the performance metrics of the given task running on
        the specified agent. If the n'th snapshot is cached, it is
        returned, otherwise a request to the agent is made.
        Args:
            task: marathon app task
            agent: agent on which the task is run
            n: statistics snapshot index
        Returns:
            statistics snapshot for the specific task running on the agent
        """
        self.log.debug("Retrieving stats for agent: %s and task: %s" % (agent, task))
        agent_stats = self.stats.get(agent, [])
        assert len(agent_stats) >= n, \
            'n must be one of indexes of snapshots fetched previosly or be ' + \
            'greater by one to fetch a new snapshot'

        agent_detail = self.get_agent_host_and_port(agent)

        if len(agent_stats) > n:
            snapshot = agent_stats[n]
        else:
            # snapshot = self.api_client.dcos_rest(
            #     "get",
            #     '/slaves/' + agent + '/monitor/statistics'
            # )
            snapshot = self.api_client.http_call(
                "get",
                "https",
                agent_detail["hostname"],
                agent_detail["port"],
                "/monitor/statistics"
            )
            self.log.debug("type: %s" % type(snapshot))
            agent_stats.append(snapshot)
            self.stats[agent] = agent_stats

        for i in snapshot:
            executor_id = i['executor_id']
            self.log.debug("executor_id: %s" % executor_id)
            if executor_id == task:
                task_stats = i['statistics']
                self.log.debug("stats for task %s agent %s: %s",
                               executor_id, agent, task_stats)
                return task_stats

    def get_agent_host_and_port(self, agent_id):
        self.log.debug("retreieving host and port for agent_id: %s", agent_id)

        response = self.api_client.dcos_rest(
            "get",
            '/slaves'
        )

        agent = {}

        for i in response["slaves"]:
            if i["id"] == agent_id:
                self.log.debug(i["hostname"])
                self.log.debug(i["port"])
                agent["hostname"] = i["hostname"]
                agent["port"] = i["port"]

        return agent
