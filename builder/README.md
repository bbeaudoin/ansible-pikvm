= Execution Environments for awx/aap/ansible-navigator

This directory contains what is needed to build a custom execution environment that includes the community.general collection for running the tasks in the role that require it. This is not quite yet in-scope for this project but can be useful for those who wish to run 

== Generating the image build context

This uses the ansible.config in the main subdirectory to configure either galaxy or the private automation hub and creates the Containerfile that will be used to build the image with the collections or other files specified in their respective requirements file. I used the blog at https://www.dbi-services.com/blog/create-and-manage-ansible-execution-environments/ for a quick start on the custom execution environment, requirements, and other commands.

```
[root@cerebus builder]# ansible-builder build --tag ee-test:v1.0
Running command:
  podman build -f context/Containerfile -t ee-test:v1.0 context
Complete! The build context can be found at: /root/ansible-pikvm/builder/context
```

== Building the container image

Once the context has been created, the image may be built. This will not be pushed to a registry, just tagged for localhost. If any Galaxy collections, python modules, etc. have been specified in the execution-environment.yml, they will be specified in the Containerfile and be built into the custom execution environment image.

```
podman build -f context/Containerfile -t ee-test context
```

== Running the playbook with the custom execution environment

Once the image is built, `ansible-navigator` can be used with the `--eei` flag to specify the execution environment image. Here was the test I used to ensure the role and modules defined within the tasks were able to run properly.

```
ansible-navigator run main.yml --eei localhost/ee-test:v1.0 --tags override
```
