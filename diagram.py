# diagram.py
from diagrams import Cluster, Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Web Service", show=False, direction="TB"):
    #ELB("lb") >> EC2("web") >> RDS("userdb")

    lb = ELB("lb")

    with Cluster("Zookeeper Quorum"):
        zoo_master = EC2("Zoo-Master")
        zoo_group = [EC2("Zoo-Slave"),zoo_master,EC2("Zoo-Slave")]

    with Cluster("Marathon Cluster"):
        marathon_group = [EC2("Marathon-1"),EC2("Marathon-2"),EC2("Marathon-3")]

    with Cluster("Mesos Cluster"):
        mesos_master = EC2("Mesos-Master")
        mesos_group = [mesos_master, EC2("Mesos-Slave"), EC2("Mesos-Slave")]


    marathon_group >> zoo_master
    mesos_group >> zoo_master
