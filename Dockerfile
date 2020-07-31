FROM continuumio/miniconda3

ADD environment.yml /environment.yml
ADD marathon_autoscaler.py marathon_autoscaler.py
ADD autoscaler /autoscaler/

RUN conda env create -f /environment.yml
# Pull the environment name out of the environment.yml
ENV PATH /opt/conda/envs/mesos-autoscaler/bin:$PATH
RUN echo "source activate mesos-autoscaler" > ~/.bashrc
#SHELL ["conda", "run", "-n", "mesos-autoscaler", "/bin/bash", "-c"]


# ENTRYPOINT ["conda", "run", "-n", "mesos-autoscaler", "python", "marathon_autoscaler.py"]
ENTRYPOINT ["python", "marathon_autoscaler.py"]